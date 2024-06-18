import os
import re
import tomllib
from time import perf_counter
from typing import Generator, TypedDict
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
    def parse(self, result: str, pc: float, output_dir: str, **kwargs) -> DctExportGcode:  # type: ignore
        stop_perf_counter = perf_counter() - pc
        slicing_result = re.findall(r'^Slicing result exported to (.*)\b', result)
        if not slicing_result:
            raise Exception('Slicing result not found in output: \n%s' % result)
        output_file_name: str = slicing_result[0].replace(os.path.join(output_dir, ''), '')

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
        return super().run(cmd, output_dir=output_dir)


class DctInfoAboutModel(TypedDict):
    file_name: str
    size_x: float
    size_y: float
    size_z: float
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float
    number_of_facets: int
    manifold: bool
    open_edges: int
    facets_reversed: int
    backwards_edges: int
    number_of_parts: int
    volume: float


class PrusaGetInfoAboutModelParser(SlicerCmdParserBase):

    @staticmethod
    def _replace_manifold(cmd_result: str) -> str:
        result = cmd_result
        result = result.replace('manifold = no', 'manifold = false')
        result = result.replace('manifold = yes', 'manifold = true')
        return result

    @staticmethod
    def _replace_table_name(cmd_result: str) -> str:
        result = cmd_result
        found_table_name = re.findall(r'\[(.*)\]', result)
        for table_name in found_table_name:
            table_name_to_replace: str = table_name
            for symbol in [' ', '.']:
                table_name_to_replace = table_name_to_replace.replace(symbol, '_')
            result = result.replace(table_name, table_name_to_replace)
        return result

    @staticmethod
    def _generate_info_table(cmd_result: str) -> Generator[str, None, None]:
        accumulate_result = ''
        for line in cmd_result.split('\n'):
            if line.startswith('[') and accumulate_result:
                yield accumulate_result
                accumulate_result = ''
            accumulate_result += line + '\n'
        yield accumulate_result

    def parse(self, cmd_result: str, pc: float, **kwargs) -> list[DctInfoAboutModel]:  # type: ignore
        for replacer in [self._replace_manifold, self._replace_table_name]:
            cmd_result = replacer(cmd_result)
        result: list[DctInfoAboutModel] = []
        for r in self._generate_info_table(cmd_result):
            for k, v in tomllib.loads(r).items():
                result.append(DctInfoAboutModel(
                    file_name=k,
                    size_x=v['size_x'],
                    size_y=v['size_y'],
                    size_z=v['size_z'],
                    min_x=v['min_x'],
                    min_y=v['min_y'],
                    min_z=v['min_z'],
                    max_x=v['max_x'],
                    max_y=v['max_y'],
                    max_z=v['max_z'],
                    number_of_facets=v['number_of_facets'],
                    manifold=v['manifold'],
                    open_edges=v['open_edges'],
                    facets_reversed=v['facets_reversed'],
                    backwards_edges=v['backwards_edges'],
                    number_of_parts=v['number_of_parts'],
                    volume=v['volume']
                ))
        return result


class PrusaGetInfoAboutModelCmdRunner(PrusaSlicerCmdRunnerBase):
    def __init__(self, slicer_path: str):
        super().__init__(ExistsFileType(slicer_path), PrusaGetInfoAboutModelParser())

    def run(self, cmd: list[str], **kwargs) -> list[DctInfoAboutModel]:
        return super().run(cmd)


__all__ = [
    'PrusaExportGcodeCmdRunner',
    'PrusaGetInfoAboutModelCmdRunner',
]
