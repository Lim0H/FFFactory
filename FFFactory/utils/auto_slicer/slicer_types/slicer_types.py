from decimal import Decimal
from FFFactory.utils.own_types import BasicType
from FFFactory.utils.systems_util import ExistsFileType


class FlagOptionType(BasicType):
    def __init__(self):
        super().__init__(True)

    @property
    def value(self) -> bool:
        return super().value


class XYOptionsType(BasicType):
    def __init__(self, x: Decimal, y: Decimal):
        super().__init__((x, y))


    @property
    def value(self) -> tuple[Decimal, Decimal]:
        return super().value


class XYZOptionsType(BasicType):
    def __init__(self, x: Decimal, y: Decimal, z: Decimal):
        super().__init__((x, y, z))

    @property
    def value(self) -> tuple[Decimal, Decimal, Decimal]:
        return super().value


class UnsignedXYOptionsType(BasicType):
    def __init__(self, x: Decimal, y: Decimal):
        super().__init__((x, y))

    def _check_value_valid(self) -> bool:
        return self.value[0] >= 0 and self.value[1] >= 0

    @property
    def value(self) -> tuple[Decimal, Decimal]:
        return super().value


class UnsignedXYZOptionsType(BasicType):
    def __init__(self, x: Decimal, y: Decimal, z: Decimal):
        super().__init__((x, y, z))

    def _check_value_valid(self) -> bool:
        return self.value[0] >= 0 and self.value[1] >= 0 and self.value[2] >= 0

    @property
    def value(self) -> tuple[Decimal, Decimal, Decimal]:
        return super().value


class UnsignedNOptionType(BasicType):
    def __init__(self, n: int):
        super().__init__(n)

    def _check_value_valid(self) -> bool:
        return self.value >= 0

    @property
    def value(self) -> int:
        return super().value


class NOptionType(BasicType):
    def __init__(self, n: int):
        super().__init__(n)

    @property
    def value(self) -> int:
        return super().value


class UnsignedXOptionType(BasicType):
    def __init__(self, x: Decimal):
        super().__init__(x)

    def _check_value_valid(self) -> bool:
        return self.value >= 0.0

    @property
    def value(self) -> Decimal:
        return super().value


class XOptionType(BasicType):
    def __init__(self, x: Decimal):
        super().__init__(x)

    @property
    def value(self) -> Decimal:
        return super().value


class FileOptionType(ExistsFileType):
    pass


__all__ = [
    'FlagOptionType',
    'XYOptionsType',
    'XYZOptionsType',
    'UnsignedXYOptionsType',
    'UnsignedXYZOptionsType',
    'UnsignedNOptionType',
    'NOptionType',
    'UnsignedXOptionType',
    'XOptionType',
    'FileOptionType',
]
