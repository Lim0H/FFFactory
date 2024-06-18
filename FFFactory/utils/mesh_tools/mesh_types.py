import os

from abc import ABC, abstractmethod
from functools import cached_property
from typing import Type

from FFFactory.utils.systems_util import ExistsDirType, ExistsFileType


class MeshProcessorBase(ABC):
    _PREFIX_OPERATION = 'op_'

    def __init__(
        self,
        input_file: ExistsFileType,
        *decorators: Type['MeshProcessorBase']
    ) -> None:
        if isinstance(input_file, ExistsFileType):
            self._input_file = input_file
        else:
            raise TypeError(f"Unknown type for input_file: {type(input_file)}")
        self._decorators = decorators

    @property
    def input_file(self) -> str:
        return self._input_file.value

    @abstractmethod
    def _save_processed_mesh(self, processed_mesh, output_file: str) -> str:
        raise NotImplementedError()

    def save_processed_mesh(self, output_dir: ExistsDirType) -> str:
        for decorator in self._decorators:
            result_decorator = decorator(
                self._input_file
            ).save_processed_mesh(output_dir)
            self._input_file = ExistsFileType(result_decorator)

        base_name = os.path.basename(self.input_file)
        output_file = os.path.join(output_dir.value, self._PREFIX_OPERATION + base_name)
        if os.path.exists(output_file):
            return output_file
        return self._save_processed_mesh(self.processed_mesh, output_file)

    @abstractmethod
    def _process_mesh(self):
        raise NotImplementedError()

    @cached_property
    def processed_mesh(self):
        return self._process_mesh()
