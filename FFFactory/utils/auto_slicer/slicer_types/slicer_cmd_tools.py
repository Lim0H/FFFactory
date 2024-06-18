import time
from abc import ABC, abstractmethod
from typing import Any

from FFFactory.utils.systems_util import ExistsFileType


class SlicerCmdParserBase(ABC):
    @abstractmethod
    def parse(self, result: str, perf_counter: float, out_dir: str):
        raise NotImplementedError()


class SlicerCmdRunnerBase(ABC):
    def __init__(self, slicer_path: ExistsFileType, cmd_parser: SlicerCmdParserBase):
        self._slicer_path = slicer_path
        self._cmd_parser = cmd_parser

    @property
    def slicer_path(self) -> str:
        return self._slicer_path.value

    @property
    def cmd_parser(self) -> SlicerCmdParserBase:
        return self._cmd_parser

    @abstractmethod
    def _run_cmd(self, cmd: list[str]) -> Any:
        raise NotImplementedError()

    def run(self, cmd: list[str], **kwargs):
        perf_counter = time.perf_counter()
        result = self._run_cmd(cmd)
        return self.cmd_parser.parse(result, perf_counter, **kwargs)
