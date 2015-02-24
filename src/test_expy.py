#!/usr/bin/python

from msml.frontend import App

import os

os.chdir("/home/weigl/workspace/msml/examples/BunnyExample/")

app = App()
alphabet = app.alphabet

memory = {}
memory['gen_1_'] = 'False'
memory['gen_5_'] = 'elements'
memory['gen_6_'] = '1000.0'
memory['input_vol_mesh'] = 'bunnyVolumeMesh.vtk'
memory['gen_2_'] = '[-0.1, 0.03, -0.07, 0.07, 0.035, 0.06]'
memory['ym'] = '80000.0'
memory['pr'] = '0.49'
memory['gen_3_'] = 'points'
memory['gen_4_'] = '[-0.1, -0.03, -0.07, 0.06, 0.19, 0.06]'
memory['input_surf_mesh'] = 'Bunny6000Surface.vtk'
converter_MSMLFloat_MSMLInt = alphabet.get('converter_MSMLFloat_MSMLInt')
memory['converter_task_1'] = converter_MSMLFloat_MSMLInt(i = memory['ym'])

converter_VTK_VTK = alphabet.get('converter_VTK_VTK')
memory['converter_task_2'] = converter_VTK_VTK(i = memory['input_surf_mesh'])

TetgenCreateVolumeMesh = alphabet.get('TetgenCreateVolumeMesh')
memory['bunnyVolumeMesher'] = TetgenCreateVolumeMesh(surfaceMesh = memory['converter_task_2']['converter_VTK_VTK'], preserveBoundary = memory['gen_1_'])

converter_VTK_VTK = alphabet.get('converter_VTK_VTK')
memory['converter_task_3'] = converter_VTK_VTK(i = memory['bunnyVolumeMesher']['TetgenCreateVolumeMesh'])

converter_VTK_VTK = alphabet.get('converter_VTK_VTK')
memory['converter_task_4'] = converter_VTK_VTK(i = memory['bunnyVolumeMesher']['TetgenCreateVolumeMesh'])

ComputeIndicesFromBoxROI = alphabet.get('ComputeIndicesFromBoxROI')
memory['bottomToIndexGroup'] = ComputeIndicesFromBoxROI(box = memory['gen_2_'], mesh = memory['converter_task_3']['converter_VTK_VTK'], select = memory['gen_3_'])

ComputeIndicesFromBoxROI = alphabet.get('ComputeIndicesFromBoxROI')
memory['bodyToIndexGroup'] = ComputeIndicesFromBoxROI(box = memory['gen_4_'], mesh = memory['converter_task_4']['converter_VTK_VTK'], select = memory['gen_5_'])

converter_MSMLListI_MSMLListI = alphabet.get('converter_MSMLListI_MSMLListI')
memory['converter_task_7'] = converter_MSMLListI_MSMLListI(i = memory['bodyToIndexGroup']['ComputeIndicesFromBoxROI'])

converter_MSMLListI_MSMLListI = alphabet.get('converter_MSMLListI_MSMLListI')
memory['converter_task_6'] = converter_MSMLListI_MSMLListI(i = memory['bottomToIndexGroup']['ComputeIndicesFromBoxROI'])

converter_MSMLListI_MSMLListI = alphabet.get('converter_MSMLListI_MSMLListI')
memory['converter_task_5'] = converter_MSMLListI_MSMLListI(i = memory['bottomToIndexGroup']['ComputeIndicesFromBoxROI'])

_exporter_clazz = msml.exporter.get_exporter('sofa')
msml_file = msml.xml.load_msml_file('/home/weigl/workspace/msml/examples/BunnyExample/bunny.msml.xml')
_exporter = _exporter_clazz(msml_file)
_exporter._memory = memory
