from abc import ABC
from typing import Optional, Any

from .slicer_config import SlicerConfigBase


class SlicerActionsRunnerBase(ABC):
    """Base class for all slicer actions runners"""
    _output_file_format: Optional[str] = None

    def __init__(self, config: SlicerConfigBase):
        self._config = config

    @property
    def config(self) -> SlicerConfigBase:
        return self._config

    @property
    def output_file_format(self) -> str:
        if self._output_file_format is None:
            raise ValueError("Output file format not set.")
        return self._output_file_format

    @output_file_format.setter
    def output_file_format(self, value: str):
        self._output_file_format = value

    def export_gcode(self, input_file: str, output_dir: str) -> Any:
        """Method for exporting gcode

        :param input_file: input file
        :param output_dir: output dir
        :return: output file
        """
        raise NotImplementedError()

    def export_3mf(self, input_file: str, output_dir: str) -> Any:
        """Method for exporting 3mf

        :param input_file: input file
        :param output_dir: output dir
        :return: output file
        """
        raise NotImplementedError()

    def export_amf(self, input_file: str, output_dir: str) -> Any:
        """Method for exporting amf

        :param input_file: input file
        :param output_dir: output dir
        :return: output file
        """
        raise NotImplementedError()

    def export_stl(self, input_file: str, output_dir: str) -> Any:
        """Method for exporting stl

        :param input_file: input file
        :param output_dir: output dir
        :return: output file
        """
        raise NotImplementedError()

    def export_obj(self, input_file: str, output_dir: str) -> Any:
        """Method for exporting obj

        :param input_file: input file
        :param output_dir: output dir
        :return: output file
        """
        raise NotImplementedError()

    def export_sla(self, input_file: str, output_dir: str) -> Any:
        """Method for exporting sla

        :param input_file: input file
        :param output_dir: output dir
        :return: output file
        """
        raise NotImplementedError()

    def get_info(self, input_file: str) -> Any:
        """Method for getting information about the input file

        :param input_file: input file
        :return: information about the input file
        """
        raise NotImplementedError()

    def save_config_file(self, output_file: str) -> Any:
        """Method for saving config file

        :param output_file: output file
        :return: output file
        """
        raise NotImplementedError()


__all__ = [
    "SlicerActionsRunnerBase"
]
