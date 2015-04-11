__author__ = 'Alexander Weig'

import inspect

import msml.exporter.visitor
from msml.exporter.visitor import *


def f(*args):
    print inspect.stack()[1][3]

class _Printer(object):
    def __init__(self):
        self.level = 0

    def __getattr__(self, item):
        lvl = self.level

        if item.endswith("begin"):
            self.level +=1
        elif item.endswith("end"):
            self.level -=1
            lvl -= 1

        def p(*args):
            print "  " * lvl, " *", item
        return p
Printer = _Printer()


class PrintVisitor(msml.exporter.visitor.Visitor):
    def scene_end(self, _msml, _scene, scene):
        Printer.scene_end(_msml, _scene, scene)

    def object_constraints_begin(self, _msml, _scene, _object, constraints):
        Printer.object_constraints_begin(_msml, _scene, _object, constraints)

    def object_end(self, _msml, _scene, _object, sceneobject):
        Printer.object_end(_msml, _scene, _object, sceneobject)

    def object_constraint_element(self, _msml, _scene, _object, _constraints, _constraint, element):
        Printer.object_constraint_element(_msml, _scene, _object, _constraints, _constraint, element)

    def object_material_begin(self, _msml, _scene, _object, materials):
        Printer.object_material_begin(_msml, _scene, _object, materials)

    def environment_solver(self, _msml, _environment, solver):
        Printer.environment_solver(_msml, _environment, solver)

    def object_output_begin(self, _msml, _scene, _object, outputs):
        Printer.object_output_begin(_msml, _scene, _object, outputs)

    def msml_end(self, _msml):
        Printer.msml_end(_msml)

    def write_export_file(self, msml_file_path, product):
        Printer.write_export_file(msml_file_path, product)

    def object_sets_nodes(self, _msml, _scene, _object, _object_sets, node):
        Printer.object_sets_nodes(_msml, _scene, _object, _object_sets, node)

    def scene_begin(self, _msml, scene):
        Printer.scene_begin(_msml, scene)

    def environment_end(self, _msml, _environment, environment):
        Printer.environment_end(_msml, _environment, environment)

    def object_material_region_begin(self, _msml, _scene, _object, _material, region):
        Printer.object_material_region_begin(_msml, _scene, _object, _material, region)

    def object_constraint_begin(self, _msml, _scene, _object, _constraints, constraint):
        Printer.object_constraint_begin(_msml, _scene, _object, _constraints, constraint)

    def object_constraint_end(self, _msml, _scene, _object, _constraints, _constraint, constraint):
        Printer.object_constraint_end(_msml, _scene, _object, _constraints, _constraint, constraint)

    def object_constraints_end(self, _msml, _scene, _object, _constraints, constraints):
        Printer.object_constraints_end(_msml, _scene, _object, _constraints, constraints)

    def object_begin(self, _msml, _scene, object):
        Printer.object_begin(_msml, _scene, object)

    def object_material_region_end(self, _msml, _scene, _object, _material, _region, region):
        Printer.object_material_region_end(_msml, _scene, _object, _material, _region, region)

    def msml_begin(self, msml_file):
        Printer.msml_begin(msml_file)

    def object_material_end(self, _msml, _scene, _object, _material, material):
        Printer.object_material_end(_msml, _scene, _object, _material)

    def object_sets_end(self, _msml, _scene, _object):
        Printer.object_sets_end(_msml, _scene, _object)

    def object_sets_elements(self, _msml, _scene, _object, _object_sets, element):
        Printer.object_sets_elements(_msml, _scene, _object, _object_sets, element)

    def object_mesh(self, _msml, _scene, _object, mesh):
        Printer.object_mesh(_msml, _scene, _object, mesh)

    def object_output_element(self, _msml, _scene, _object, _output, output):
        Printer.object_output_element(_msml, _scene, _object, _output, output)

    def environment_begin(self, _msml, env):
        Printer.environment_begin(_msml, env)

    def object_sets_surfaces(self, _msml, _scene, _object, _object_sets, surface):
        Printer.object_sets_surfaces(_msml, _scene, _object, _object_sets, surface)

    def environment_simulation(self, _msml, _environment, simulation):
        Printer.environment_simulation(_msml, _environment, simulation)

    def object_material_region_element(self, _msml, _scene, _object, _material, _region, element):
        Printer.object_material_region_element(_msml, _scene, _object, _material, _region, element)

    def object_output_end(self, _msml, _scene, _object, _output,o):
        Printer.object_output_end(_msml, _scene, _object, _output,o)

    def object_sets_begin(self, _msml, _scene, _object, sets):
        Printer.object_sets_begin(_msml, _scene, _object, sets)


class PrintVisitorDisp(VisitorDispatchable, PrintVisitor):
    @disp_constraint('fixedConstraint')
    def object_constraint_element_fixedConstraint(self, _msml, _scene, _object, _constraints, _constraint, element):
        Printer.object_constraint_element_fixedConstraint(self, _msml, _scene, _object, _constraints, _constraint, element)

    @disp_mesh("linearTet")
    def object_mesh_linearTet(self, _msml, _scene, _object, mesh):
        Printer.object_mesh_linearTet(self, _msml, _scene, _object, mesh)

    @disp_material("mass")
    def object_material_region_element_mass(self, _msml, _scene, _object, _material, _region, element):
        Printer.object_material_region_element_mass(self, _msml, _scene, _object, _material, _region, element)

    @disp_material('linearElastic')
    def object_material_region_element_linearElastic(self, _msml, _scene, _object, _material, _region, element):
        Printer.object_material_region_element_linearElastic(self, _msml, _scene, _object, _material, _region, element)

    @disp_material('indexgroup')
    def object_material_region_element_indexgroup(self, _msml, _scene, _object, _material, _region, element):
        Printer.object_material_region_element_indexgroup(self, _msml, _scene, _object, _material, _region, element)

    @disp_output('displacement')
    def object_output_element_displacement(self, _msml, _scene, _object, _output, output):
        Printer.object_output_element_displacement(self, _msml, _scene, _object, _output, output)

import msml.xml
def main():
    msml_file = msml.xml.load_msml_file("/home/weigl/workspace/msml/examples/BunnyExample/bunny.msml.msml_xml")


    exporter = msml.exporter.visitor.VisitorExporterFramework(msml_file, PrintVisitor)
    exporter.render()


    exporter = msml.exporter.visitor.VisitorExporterFramework(msml_file, PrintVisitorDisp)
    exporter.render()


if __name__ == "__main__":
    main()
