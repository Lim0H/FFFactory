from abc import ABC, abstractmethod, abstractproperty
from functools import cached_property
import pymeshfix
import numpy as np


class MeshRepairerBase(ABC):
    def __init__(self, input_file: str) -> None:
        self._input_file = input_file

    @property
    def input_file(self) -> str:
        return self._input_file

    @abstractproperty
    def array_mesh(self) -> tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError()

    @abstractmethod
    def save_fixed_mesh(self, output_file: str) -> None:
        pass


class MeshRepairer(MeshRepairerBase):
    @cached_property
    def fixed_mesh(self) -> pymeshfix.PyTMesh:
        tin = pymeshfix.PyTMesh()
        tin.load_file(self.input_file)
        tin.fill_small_boundaries()
        tin.remove_smallest_components()
        return tin

    @property
    def array_mesh(self) -> tuple[np.ndarray, np.ndarray]:
        return self.fixed_mesh.return_arrays()

    def save_fixed_mesh(self, output_file: str) -> None:
        self.fixed_mesh.save(output_file)

