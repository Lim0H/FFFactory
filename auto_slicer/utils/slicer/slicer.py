import os
import subprocess
import tempfile

import numpy as np
from stl import Mesh

from auto_slicer.utils.string_tools import clean_name


class AutoSlicer:
    # Select slicer parameters based on unprintability > treshold
    treshold_supports = 1.0
    treshold_brim = 2.0

    def __init__(self, slicer_path, config_path):
        """Initialize AutoSlicer.

        Keyword arguments:
        slicer_path -- location of PrusaSlicer executable. Should be .AppImage or prusa-slicer-console.exe
        config_path -- location of printer config file
        """
        self.slicer = slicer_path
        self.config = config_path

    def __tweakFile(self, input_file, tmpdir):
        # Runs Tweaker.py from https://github.com/ChristophSchranz/Tweaker-3

        try:
            output_file = os.path.join(tmpdir, "tweaked.stl")
            print(output_file)
            curr_path = os.path.dirname(os.path.abspath(__file__))
            if os.name == "nt":
                python_path = os.path.join(curr_path, "venv", "Scripts", "python")
            else:
                python_path = os.path.join(curr_path, "venv", "bin", "python")
            tweaker_path = os.path.join(curr_path, "Tweaker-3/Tweaker.py")
            result = subprocess.run([python_path, tweaker_path, "-i", input_file, "-o", output_file, "-x", "-vb"],
                                    capture_output=True, text=True).stdout
            # Get "unprintability" from stdout
            _, temp = result.splitlines()[-5].split(":")
            unprintability = str(round(float(temp.strip()), 2))
            print("Unprintability: " + unprintability)
            print(output_file)
            return output_file, unprintability
        except Exception:
            print("Couldn't run tweaker on file " + self.input_file)

    def __adjustHeight(self, input_file, tmpdir):
        # Move STL coordinates so Zmin = 0
        # This avoids errors in PrusaSlicer if Z is above/below the build plate
        try:
            output_file = os.path.join(tmpdir, "translated.stl")
            my_mesh = Mesh.from_file(input_file)
            print("Z min:", my_mesh.z.min())
            print("Z max:", my_mesh.z.max())
            translation = np.array([0, 0, -my_mesh.z.min()])
            my_mesh.translate(translation)
            print("Translated, new Z min:", my_mesh.z.min())
            my_mesh.save(output_file)
            return output_file
        except Exception:
            print("Couldn't adjust height of file " + self.input_file)

    def __runSlicer(self, input, output_path, unprintability):
        # Run PrusaSlicer
        # Get filename with mostly alphanumeric characters
        # Avoids errors with octopi upload due to invalid characters in filename
        filename, _ = os.path.basename(self.input_file).rsplit(".", 1)
        filename = clean_name(filename)

        output_file = os.path.join(
            output_path,
            (filename + "_U" + str(unprintability) + "_{print_time}" ".gcode")
        )

        # Form command to run
        # Example: prusa-slicer-console.exe --load MK3Sconfig.ini -g -o outputFiles/sliced.gcode inputFiles/input.gcode
        cmd = [self.slicer, "--load", self.config]

        if float(unprintability) > self.treshold_brim:
            cmd.extend(["--brim-width", "5", "--skirt-distance", "6"])
        if float(unprintability) > self.treshold_supports:
            cmd.append("--support-material")

        cmd.extend(["-g", "-o", output_file, input])
        print(cmd)
        try:
            subprocess.run(cmd)
        except Exception:
            print("Couldn't slice file " + self.input_file)

    def slice(self, input, output):
        """Rotates and slices file in optimal orientation

        Keyword arguments:
        input -- file to slice (STL or 3MF)
        output -- path to place output GCODE
        """
        self.input_file = input
        with tempfile.TemporaryDirectory() as temp_directory:
            print("Temp. dir:", temp_directory)
            tweaked_file, unprintability = self.__tweakFile(self.input_file, temp_directory)
            translatedFile = self.__adjustHeight(tweaked_file, temp_directory)
            self.__runSlicer(translatedFile, output, unprintability)
