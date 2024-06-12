from decimal import Decimal
import os
from FFFactory.auto_slicer.utils.slicer.prusa_slicer import PrusaSlicer, PrusaSlicerConfig

path = r'c:\PrusaSlicer-2.7.4+win64-202404050928'

slicer_path = os.path.join(path, 'prusa-slicer-console.exe')

file_path = os.path.join(path, '1V8engine.stl')

# prusa_slicer = PrusaSlicer(PrusaSlicerConfig(slicer_path + '1'))

prusa_slicer = PrusaSlicer(slicer_path)

prusa_slicer.set_repair()
prusa_slicer.set_scale(Decimal(0.5))
prusa_slicer.set_duplicate(5)

w = prusa_slicer.export_gcode(file_path, os.getcwd())

print(w)