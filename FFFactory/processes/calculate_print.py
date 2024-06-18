

from abc import ABC, abstractmethod
from decimal import Decimal
from functools import reduce
import re
import shutil
import os
from tempfile import TemporaryDirectory
from typing import Generator, Optional

from FFFactory.config import RenderConfig
from FFFactory.utils.auto_render import BlenderConfigImporter
from FFFactory.utils.auto_render.blender.blender_tools import RenderTemplate, get_render_templates
from FFFactory.utils.auto_slicer import PrusaSlicer, PrusaOutputFilenameFormatFdm as OutPutFdm
from FFFactory.utils.csv_tools import CsvWriter
from FFFactory.utils.mesh_tools import MeshTweaker, MeshRepairer
from FFFactory.utils.mesh_tools.mesh_types import MeshProcessorBase
from FFFactory.utils.systems_util import ExistsDirType, ExistsFileType


OBJS = 'objs'
BLEND = 'blend'
RENDER_CONFIG = 'render_config'

FILES_TO_SEARCH = {
    OBJS: ('model.stl', 'model.3mf', 'model.obj'),
    BLEND: ('model.blend',),
    RENDER_CONFIG: ('render_config.yaml',)
}

SCALE_CM = [
    10,
    15,
    20,
    25,
    30,
    35,
    40,
    45,
    50,
    75,
    100,
    120
]

CSV_FILE = 'calulate_print.csv'

CSV_HEADER = ['Model', 'Scale Z [mm]', 'Print Time [sec]', 'Total Weight [g]', 'Price']


class ScannerFolderBase(ABC):
    def __init__(self, input_dir: ExistsDirType):
        self._input_dir = input_dir

    @property
    def input_dir(self) -> str:
        return self._input_dir.value

    @abstractmethod
    def _scan_folder(self) -> Optional[ExistsFileType]:
        raise NotImplementedError()

    def scan_folder(self) -> ExistsFileType:
        result = self._scan_folder()
        if result is None:
            raise Exception('File not found in %s' % self.input_dir)
        return result


class ScannerObjs(ScannerFolderBase):

    def _scan_folder(self) -> Optional[ExistsFileType]:
        path = os.path.join(self.input_dir, OBJS)
        for file in FILES_TO_SEARCH[OBJS]:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                return ExistsFileType(file_path)
        return None


class ScannerBlend(ScannerFolderBase):

    def _scan_folder(self) -> Optional[ExistsFileType]:
        path = os.path.join(self.input_dir, BLEND)
        for file in FILES_TO_SEARCH[BLEND]:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                return ExistsFileType(file_path)
        return None


class ScalerGroupBase(ABC):
    def __init__(self, model: ExistsFileType, prusa_slicer: PrusaSlicer):
        self._prusa_slicer = prusa_slicer
        self._model = model

    @property
    def prusa_slicer(self) -> PrusaSlicer:
        return self._prusa_slicer

    @property
    def model(self) -> str:
        return self._model.value

    def _fix_mesh(self) -> None:
        mesh_operations: list[type[MeshProcessorBase]] = [
            MeshTweaker
        ]
        info_about_model = self.prusa_slicer.get_info(self.model)
        if info_about_model[0]['manifold'] is False:
            mesh_operations.append(MeshRepairer)
        mesh_operations.reverse()

        path_to_fixed_model = mesh_operations[0](
            self._model,
            *info_about_model[1:]
        ).save_processed_mesh(
            ExistsDirType(os.path.basename(self.model))
        )
        self._model = ExistsFileType(path_to_fixed_model)

    @abstractmethod
    def _scale(self) -> Generator[Optional[tuple[Decimal, Decimal, Decimal]], None, None]:
        raise NotImplementedError()

    def scale(self) -> Generator[Optional[tuple[Decimal, Decimal, Decimal]], None, None]:
        self._fix_mesh()
        return self._scale()


class ScalerGroup(ScalerGroupBase):

    def _scale(self) -> Generator[Optional[tuple[Decimal, Decimal, Decimal]], None, None]:
        info_model = self.prusa_slicer.get_info(self.model)[0]
        for scale_z_cm in SCALE_CM:
            size_z_mm = info_model['size_z']
            factor_mm = (scale_z_cm * 10) / size_z_mm
            yield (
                Decimal(info_model['size_x'] * factor_mm),
                Decimal(info_model['size_y'] * factor_mm),
                Decimal(size_z_mm * factor_mm)
            )


class NotScalerGroup(ScalerGroupBase):

    def _scale(self) -> Generator[Optional[tuple[Decimal, Decimal, Decimal]], None, None]:
        info_model = self.prusa_slicer.get_info(self.model)[0]
        for _ in range(1):
            yield (
                Decimal(info_model['size_x']),
                Decimal(info_model['size_y']),
                Decimal(info_model['size_z'])
            )


class ScannerRenderConfig(ScannerFolderBase):

    def _scan_folder(self) -> Optional[ExistsFileType]:
        path = os.path.join(self.input_dir, RENDER_CONFIG)
        for file in FILES_TO_SEARCH[RENDER_CONFIG]:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                return ExistsFileType(file_path)
        return None


def print_time_to_minutes(print_time: str) -> int:
    result_1 = re.findall(r'^(\d*)h(\d*)m$', print_time)
    result_2 = re.findall(r'^(\d*)m$', print_time)
    result_3 = re.findall(r'^(\d*)d(\d*)h(\d*)m$', print_time)
    if result_1:
        h = result_1[0][0]
        m = result_1[0][1]
        return int(h) * 60 + int(m)
    elif result_2:
        m = result_2[0]
        return int(m)
    elif result_3:
        d = result_3[0][0]
        h = result_3[0][1]
        m = result_3[0][2]
        return int(d) * 24 * 60 + int(h) * 60 + int(m)
    return 0


class CalculatePrint:
    def __init__(
        self,
        input_dir: ExistsDirType,
        output_dir: ExistsDirType,
        writer: CsvWriter
    ):
        self.__input_dir = input_dir
        self.__output_dir = output_dir
        self.__writter = writer

    @property
    def input_dir(self) -> ExistsDirType:
        return self.__input_dir

    @property
    def output_dir(self) -> ExistsDirType:
        return self.__output_dir

    @property
    def writter(self) -> CsvWriter:
        return self.__writter

    def render(self):
        model = ScannerRenderConfig(self.input_dir).scan_folder()
        lst_render_templates = get_render_templates(
            RenderConfig.TEMPLATES_DIR
        )
        for render_template in lst_render_templates:
            render_template.render_image(model)

    def slice(self, config_file: ExistsFileType, scaler_group: ScalerGroupBase):
        model = ScannerObjs(self.input_dir).scan_folder()
        prusa_slicer = PrusaSlicer(config_file.value)
        prusa_slicer.output_file_format = f'{OutPutFdm.INPUT_FILENAME_BASE}___T{OutPutFdm.PRINT_TIME}__W{OutPutFdm.TOTAL_WEIGHT}'
        with TemporaryDirectory() as temp_dir:
            for size_x, size_y, size_z in scaler_group.scale():
                prusa_slicer.set_scale_to_fit(size_x, size_y, size_z)
                info_about_export = prusa_slicer.export_gcode(model.value, temp_dir)
                print_time = re.findall(r'__T(.*)__W', info_about_export['output_file_name'])[0]
                total_weight = re.findall(r'__W(.*)', info_about_export['output_file_name'])[0]
                self.writter.writerow({
                    CSV_HEADER[0]: os.path.basename(self.input_dir.value),
                    CSV_HEADER[1]: size_z,
                    CSV_HEADER[2]: print_time_to_minutes(print_time),
                    CSV_HEADER[3]: Decimal(total_weight),
                    CSV_HEADER[4]: Decimal(
                        4.5 * (
                            total_weight / 100.0 * 8.0 + (
                                print_time_to_minutes(print_time) / 60 * 0.75
                            )
                        )
                    )
                })

    def move(self):
        dir_name = os.path.dirname(self.input_dir)
        path_to = os.path.join(self.output_dir, dir_name)
        os.makedirs(path_to, exist_ok=True)
        shutil.move(self.input_dir, path_to)
