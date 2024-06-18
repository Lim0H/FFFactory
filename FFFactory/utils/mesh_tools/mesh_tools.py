import glob
from typing import Type
from pymeshfix import PyTMesh

from FFFactory.utils.systems_util import ExistsFileType

from .mesh_types import MeshProcessorBase
from .tweaker import FileHandler, Tweak


class MeshRepairer(MeshProcessorBase):
    _PREFIX_OPERATION = 'repair_'

    def _save_processed_mesh(self, processed_mesh: PyTMesh, output_file: str) -> str:
        processed_mesh.save_file(output_file)
        return glob.glob(output_file)[0]

    def _process_mesh(self) -> PyTMesh:
        tin = PyTMesh(False)  # verbose = False
        tin.load_file(self.input_file)
        tin.fill_small_boundaries()
        tin.remove_smallest_components()
        return tin


class MeshTweaker(MeshProcessorBase):
    _PREFIX_OPERATION = 'tweak_'

    def __init__(
        self,
        input_file: ExistsFileType,
        *mesh_operation: Type[MeshProcessorBase]
    ) -> None:
        super().__init__(input_file, *mesh_operation)
        self._file_handler = FileHandler()

    @property
    def file_handler(self) -> FileHandler:
        return self._file_handler

    def _save_processed_mesh(self, processed_mesh: tuple[dict, dict], output_file: str) -> str:
        loaded_mesh, info_about_mesh = processed_mesh
        lst_files = self.file_handler.write_mesh(
            loaded_mesh, info_about_mesh, output_file
        )
        return lst_files[0]

    def _process_mesh(self) -> tuple[dict, dict]:
        loaded_mesh = self.file_handler.load_mesh(self.input_file)
        info_about_mesh = {}
        for part, content in loaded_mesh.items():
            info_about_mesh[part] = {
                'matrix': Tweak(content['mesh'], verbose=False).matrix
            }
        return loaded_mesh, info_about_mesh


__all__ = [
    'MeshRepairer',
    'MeshTweaker'
]
