from .prusa_cmd_tools import DctExportGcode, DctInfoAboutModel, PrusaExportGcodeCmdRunner, PrusaGetInfoAboutModelCmdRunner
from ..slicer_types import FlagOptionType
from FFFactory.utils.systems_util import ExistsDirType
from ..slicer_types import SlicerActionsRunnerBase
from .prusa_config import PrusaSlicerConfig
from .prusa_types import PrusaOutputFilenameFormatFdm as OutPutFdm


class PrusaActionsRunner(SlicerActionsRunnerBase):
    _output_file_format = f'{OutPutFdm.INPUT_FILENAME_BASE}___T{OutPutFdm.PRINT_TIME}'

    def __init__(self, config: PrusaSlicerConfig):
        super().__init__(config)

    @property
    def config(self) -> PrusaSlicerConfig:
        return self._config  # type: ignore

    def export_gcode(self, input_file: str, output_dir: str) -> DctExportGcode:
        cmd_runner = PrusaExportGcodeCmdRunner(self.config.slicer_path)
        self.config.actions_options.export_gcode = FlagOptionType()
        self.config.sliced_options['other_options'].output = ExistsDirType(output_dir)
        self.config.sliced_options['misc_options'].output_filename_format = self.output_file_format
        self.config.files_options.add_files(input_file)
        return cmd_runner.run(self.config.all_options, output_dir)

    def export_3mf(self, input_file: str, output_dir: str) -> str:
        pass

    def export_amf(self, input_file: str, output_dir: str) -> str:
        pass

    def export_stl(self, input_file: str, output_dir: str) -> str:
        pass

    def export_obj(self, input_file: str, output_dir: str) -> str:
        pass

    def export_sla(self, input_file: str, output_dir: str) -> str:
        pass

    def save_config_file(self, output_file: str) -> str:
        pass

    def get_info(self, input_file: str) -> list[DctInfoAboutModel]:
        cmd_runner = PrusaGetInfoAboutModelCmdRunner(self.config.slicer_path)
        self.config.actions_options.info = FlagOptionType()
        self.config.files_options.add_files(input_file)
        return cmd_runner.run(self.config.all_options)
