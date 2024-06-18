from abc import ABC
from typing import Optional

from FFFactory.utils.systems_util import ExistsFileType


class SlicerConfigBase(ABC):
    def __init__(self, slicer_path: str, config_path: Optional[str] = None):
        self._slicer_path = ExistsFileType(slicer_path)
        self._config_path = ExistsFileType(config_path) if config_path is not None else None

    @property
    def slicer_path(self) -> str:
        return self._slicer_path.value

    @property
    def config_path(self) -> Optional[str]:
        return self._config_path.value if self._config_path is not None else None


__all__ = ['SlicerConfigBase']
