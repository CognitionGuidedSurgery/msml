#include "IsoContourOperator.h"

namespace MSML
	{
	namespace IsoContourOperator
	{
			std::vector<std::string> IsoContourOperator(const std::string data_directory, const std::string initial_position, const std::string final_position, const std::string weight_table)
		{
			//print information about the inputs
			std::cout << "data directory : " << data_directory << std::endl;			
			std::cout << "initial position : " << initial_position << std::endl;
			std::cout << "final positions : " << final_position << std::endl;
			std::cout << "weight table : " << weight_table << std::endl;

			//geting the dirctory and name of files
			std::string file_dir = data_directory;
			std::string file_init = std::string(data_directory) + std::string(initial_position);
			std::string file_deform = std::string(data_directory) + std::string(final_position);
			std::string file_weight = std::string(data_directory) + std::string(weight_table);

			//define vtufile and weightfile for reading stream
			ifstream vtufile(file_deform.c_str());
			ifstream weightfile(file_weight.c_str());

			//vtulist and weightlist for store the name and weight for vtu files
			std::vector<std::string> vtulist;
			std::vector<float> weightlist;

			//reading stream helper
			std::string line;

			//read the names of vtu files from vtufile into vtulist
			if (vtufile.is_open()) {
				while(getline(vtufile, line)) {
					vtulist.push_back(line);
				}
				vtufile.close();
			}

			//read the weights from weightfile into weightlist	
			if (weightfile.is_open()) {
				while(getline(weightfile, line)) {
					weightlist.push_back(atof(line.c_str()));
				}
				weightfile.close();
			}	

			//checking the size of vtulist and wegithlist is equal
			if (vtulist.size() != weightlist.size()) {
				//abort program if initial vtu and deformed vtu are not same size
				std::cout << "\ninitial position file are not same size as deformed position" << std::endl;
				abort();

			}


			//unstrcturedgrid for initial position (from file_init)	
			vtkSmartPointer<vtkUnstructuredGrid> ugrid_init =  vtkSmartPointer<vtkUnstructuredGrid>::New();

			//unstructuredgrid reader for initial position (from file_init)	
			vtkSmartPointer<vtkXMLUnstructuredGridReader> reader_init = vtkSmartPointer<vtkXMLUnstructuredGridReader>::New();

			//unstructuredwriter for writing the result vtu file
			vtkSmartPointer<vtkXMLUnstructuredGridWriter> writer =  vtkSmartPointer<vtkXMLUnstructuredGridWriter>::New();

			//polydatawriter for writing the contour data
			vtkSmartPointer<vtkXMLPolyDataWriter> polywriter = vtkSmartPointer<vtkXMLPolyDataWriter>::New();

			//vtk surface filter
			vtkSmartPointer<vtkDataSetSurfaceFilter> surfacefilter = vtkSmartPointer<vtkDataSetSurfaceFilter>::New();

			//vtkpoints to store and modify the points form surface
			vtkSmartPointer<vtkPoints> points_mean = vtkSmartPointer<vtkPoints>::New();
			vtkSmartPointer<vtkPoints> points_outer = vtkSmartPointer<vtkPoints>::New();	
			vtkSmartPointer<vtkPoints> points_inner = vtkSmartPointer<vtkPoints>::New();
			vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();

			//vtkfloatarray to store the normals
			vtkSmartPointer<vtkFloatArray> normals = vtkSmartPointer<vtkFloatArray>::New();

			//vtkPolydata to store extracted surface
			vtkSmartPointer<vtkPolyData> surface_init = vtkSmartPointer<vtkPolyData>::New();
			vtkSmartPointer<vtkPolyData> contour_mean = vtkSmartPointer<vtkPolyData>::New();
			vtkSmartPointer<vtkPolyData> contour_outer = vtkSmartPointer<vtkPolyData>::New();
			vtkSmartPointer<vtkPolyData> contour_inner = vtkSmartPointer<vtkPolyData>::New();

			//normal generator
			vtkSmartPointer<vtkPolyDataNormals> normal_generator = vtkSmartPointer<vtkPolyDataNormals>::New();

			//read the initial vtu file
			reader_init->SetFileName(file_init.c_str());
			reader_init->Update();

			//pass the vtu information to unstructuredgrid
			ugrid_init = reader_init->GetOutput();

			//filtering the surface
			surfacefilter->SetInputData(ugrid_init);
			surfacefilter->Update();

			//getting extracted surface information
			surface_init = surfacefilter->GetOutput();

			//writing the initial surface
			polywriter->SetFileName("initial_countour.vtp");
			polywriter->SetInputData(surface_init);
			polywriter->SetDataModeToAscii();
			polywriter->Write();

			//copy polydata from initial surface
			contour_mean->DeepCopy(surface_init);
			contour_outer->DeepCopy(surface_init);
			contour_inner->DeepCopy(surface_init);

			//get only the points' information from initial surface
			points_mean = contour_mean->GetPoints();
			points_outer = contour_outer->GetPoints();
			points_inner = contour_inner->GetPoints();
			points = surface_init->GetPoints();

			//creat vectors with dimension numberofpoinst * 3 
			std::vector< std::vector<double> > mean_calculator(ugrid_init->GetNumberOfPoints(), std::vector<double>(3));
			std::vector< float > mean(surface_init->GetNumberOfPoints(), 0.0);
			std::vector< float > std_dev(surface_init->GetNumberOfPoints(), 0.0);
			std::vector< float > std_dev_helper(surface_init->GetNumberOfPoints(), 0.0);

			//compute the mean of the distance of the displacement , sum of u_i*w_i , and sum of u_i*u_i*w_i is defined as std_dev_helper, ps: u : displacement, w : weight
			for (int i = 0; i < vtulist.size(); ++i) {
				//unstructuredgrid reader for deform position (from vtulist)
				vtkSmartPointer<vtkXMLUnstructuredGridReader> reader_deform = vtkSmartPointer<vtkXMLUnstructuredGridReader>::New();

				//used for get unstructuredgrid for each deformed position (from vtulist)
				vtkSmartPointer<vtkUnstructuredGrid> ugrid =  vtkSmartPointer<vtkUnstructuredGrid>::New();

				//get surface info for each vtu file
				vtkSmartPointer<vtkPolyData> surface_deform = vtkSmartPointer<vtkPolyData>::New();

				//vtk surface filter
				vtkSmartPointer<vtkDataSetSurfaceFilter> surfacefilter_deform = vtkSmartPointer<vtkDataSetSurfaceFilter>::New();

				//create the path + name for vtu file	
				std::string name = std::string(data_directory) + std::string(vtulist[i]);

				//read vtu file into unstructuredgrid
				reader_deform->SetFileName(name.c_str());
				reader_deform->Update();

				//get vtu information into unstructuredgrid
				ugrid = reader_deform->GetOutput();

				//filtering the surface
				surfacefilter_deform->SetInputData(ugrid);
				surfacefilter_deform->Update();

				//set surface info to surface deform
				surface_deform = surfacefilter_deform->GetOutput();

				//need to check whether initial position vtu file are same size as deformed position vtu file
				if (surface_init->GetNumberOfPoints() == surface_deform->GetNumberOfPoints()) {
					for (int j = 0; j < surface_init->GetNumberOfPoints(); ++j) {
						//compute the mean calculator
						mean_calculator[j][0] += (surface_deform->GetPoint(j)[0] - surface_init->GetPoint(j)[0]) * weightlist[i];
						mean_calculator[j][1] += (surface_deform->GetPoint(j)[1] - surface_init->GetPoint(j)[1]) * weightlist[i];
						mean_calculator[j][2] += (surface_deform->GetPoint(j)[2] - surface_init->GetPoint(j)[2]) * weightlist[i];
						float x, y, z;
						x = surface_deform->GetPoint(j)[0] - surface_init->GetPoint(j)[0];
						y = surface_deform->GetPoint(j)[1] - surface_init->GetPoint(j)[1];
						z = surface_deform->GetPoint(j)[2] - surface_init->GetPoint(j)[2];
						mean[j] += std::sqrt(x*x + y*y + z*z) * weightlist[i];
						std_dev_helper[j] += (x*x + y*y + z*z) * weightlist[i];
					}
				} else {
					//abort program if initial vtu and deformed vtu are not same size
					std::cout << "\ninitial position file are not same size as deformed position" << std::endl;
					abort();
				}

			}

			//calculating the mean surface
			for (int i = 0; i < surface_init->GetNumberOfPoints(); ++i) {
				float x, y, z;

				x = surface_init->GetPoint(i)[0] + mean_calculator[i][0];
				y = surface_init->GetPoint(i)[1] + mean_calculator[i][1];
				z = surface_init->GetPoint(i)[2] + mean_calculator[i][2];
				points_mean->SetPoint(i, x, y, z);

			}

			//compute normal
			normal_generator->SetInputData(contour_mean);
			normal_generator->ComputePointNormalsOn();
			normal_generator->ComputeCellNormalsOff();
			normal_generator->SetSplitting(0);
			normal_generator->Update();
			//contour_mean = normal_generator->GetOutput();

			//writing the mean surface
			polywriter->SetFileName("countour_mean.vtp");
			polywriter->SetInputData(contour_mean);
			polywriter->SetDataModeToAscii();
			polywriter->Write();

			//get normals
			normals = vtkFloatArray::SafeDownCast(normal_generator->GetOutput()->GetPointData()->GetArray("Normals"));

			//calculating sqrt(sum of we_i*u_i*u_i - mean*mean) -->standard deviation
			for (int i = 0; i < surface_init->GetNumberOfPoints(); ++i) {
				if ((std_dev_helper[i] - mean[i]*mean[i]) < 0.0) {
					std_dev[i] = 0.0;
				} else {
					std_dev[i] = std::sqrt(std_dev_helper[i] - mean[i]*mean[i]);
				}

			}


			//+/- 2*std_dev to each point for 95% probability
			for (int i = 0; i < surface_init->GetNumberOfPoints(); ++i) {
				float x_outer, y_outer, z_outer, x_inner, y_inner, z_inner;

				x_outer = contour_mean->GetPoint(i)[0] + std_dev[i] * 2 * normals->GetTuple(i)[0];
				y_outer = contour_mean->GetPoint(i)[1] + std_dev[i] * 2 * normals->GetTuple(i)[1];
				z_outer = contour_mean->GetPoint(i)[2] + std_dev[i] * 2 * normals->GetTuple(i)[2];

				x_inner = contour_mean->GetPoint(i)[0] - std_dev[i] * 2 * normals->GetTuple(i)[0];
				y_inner = contour_mean->GetPoint(i)[1] - std_dev[i] * 2 * normals->GetTuple(i)[1];
				z_inner = contour_mean->GetPoint(i)[2] - std_dev[i] * 2 * normals->GetTuple(i)[2];

				float test = normals->GetTuple(i)[0];
				if (test != test) {
					std::cout << "cao" << std::endl;
				}

				points_outer->SetPoint(i, x_outer, y_outer, z_outer);
				points_inner->SetPoint(i, x_inner, y_inner, z_inner);
			}

			//writing outer contour
			polywriter->SetFileName("contour_outer.vtp");
			polywriter->SetInputData(contour_outer);
			polywriter->SetDataModeToAscii();
			polywriter->Write();

			//writing inner contour
			polywriter->SetFileName("contour_inner.vtp");
			polywriter->SetInputData(contour_inner);
			polywriter->SetDataModeToAscii();
			polywriter->Write();

			
			std::vector<std::string> output_file_name;
			output_file_name.push_back("contour_outer.vtp");
			output_file_name.push_back("contour_inner.vtp");

			return output_file_name;

		}	

	}
	}
