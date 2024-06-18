import yaml
from abc import ABC, abstractmethod
from typing import Optional, TypedDict
from FFFactory.utils.systems_util import ExistsFileType, ExistsDirType


class ConfigImporterBase(ABC):
    def __init__(self, file_name: ExistsFileType) -> None:
        self._file_name = file_name

    @abstractmethod
    def _import_config(self, yaml_output: Optional[dict]):
        raise NotImplementedError()

    @property
    def file_name(self) -> str:
        return self._file_name.value

    def import_config(self):
        with open(self.file_name, 'r') as stream:
            yaml_output = yaml.safe_load(stream)
        return self._import_config(yaml_output)


class DctModelRenderConfig(TypedDict):
    template_name: str
    output_dir: ExistsDirType
    file_path: ExistsFileType
    file_name: str
    image_name: str
    angle_rotation_z: int
    max_rotation_z: int
    save_as: str
    save_project: bool
    always_rerender: bool
    number_imgs: list[int]


__all__ = [
    'ConfigImporterBase',
    'DctModelRenderConfig',
]
