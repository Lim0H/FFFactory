import os
from FFFactory.own_types import BasicType


def remove_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


class ExistsPathType(BasicType):
    def __init__(self, value: str):
        super().__init__(value)

    def _check_value_valid(self) -> bool:
        return os.path.exists(self.value)


class ExistsDirType(ExistsPathType):
    def _check_value_valid(self) -> bool:
        return os.path.isdir(self.value)


class ExistsDirNameType(ExistsPathType):
    def _check_value_valid(self) -> bool:
        return os.path.exists(
            os.path.dirname(self.value)
        )


class ExistsFileType(ExistsPathType):
    def _check_value_valid(self) -> bool:
        return os.path.isfile(self.value)
