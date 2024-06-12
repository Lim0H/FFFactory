import os
import re
from glob import glob
from time import perf_counter
from typing import TypedDict
from FFFactory.utils.systems_util import ExistsFileType
from ..slicer_types import SlicerCmdRunnerBase, SlicerCmdParserBase


class PrusaSlicerCmdRunnerBase(SlicerCmdRunnerBase):
    def _run_cmd(self, cmd: list[str]) -> str:
        print(' '.join(cmd))
        result = os.popen(' '.join(cmd)).read()
        return result


class DctExportGcode(TypedDict):
    output_file_name: str
    output_file_path: ExistsFileType
    print_warning: bool
    time_slice_sec: int


class PrusaExportGcodeParser(SlicerCmdParserBase):
    def __init__(self):
        super().__init__()

    def parse(self, result: str, pc: float, out_dir: str) -> DctExportGcode:
        print(result, pc)
        stop_perf_counter = perf_counter() - pc
        slicing_result = re.findall(r'^Slicing result exported to (.*)\b', result)
        if not slicing_result:
            raise Exception('Slicing result not found in output: \n%s' % result)
        output_file_name: str = slicing_result[0].replace(os.path.join(out_dir, ''), '')

        return DctExportGcode(
            output_file_name=output_file_name,
            time_slice_sec=int(stop_perf_counter),
            print_warning='print warning:' in result,
            output_file_path=ExistsFileType(slicing_result[0])
        )


class PrusaExportGcodeCmdRunner(PrusaSlicerCmdRunnerBase):
    def __init__(self, slicer_path: str):
        super().__init__(ExistsFileType(slicer_path), PrusaExportGcodeParser())

    def run(self, cmd: list[str], output_dir: str) -> DctExportGcode:  # type: ignore
        return super().run(cmd, output_dir)  # type: ignore


class DctInfoAboutModel(TypedDict):
    model_name: str
    model_path: ExistsFileType


class PrusaGetInfoAboutModelParser(SlicerCmdParserBase):
    def __init__(self):
        super().__init__()

    def parse(self, result: str) -> list[DctExportGcode]:
        pass


class PrusaGetInfoAboutModelCmdRunner(PrusaSlicerCmdRunnerBase):
    def __init__(self, slicer_path: str):
        super().__init__(ExistsFileType(slicer_path), PrusaGetInfoAboutModelParser())

    def run(self, cmd: list[str]) -> list[DctInfoAboutModel]:
        return super().run(cmd)


__all__ = [
    'PrusaExportGcodeCmdRunner',
    'PrusaGetInfoAboutModelCmdRunner',
]
