from enum import Enum
from typing import Any, Optional

from FFFactory.utils.systems_util import ExistsDirNameType, ExistsDirType, ExistsFileType

from ..slicer_types import (
    SlicerCommandsOptionsBase,
    SelfClearingSlicerCommandsOptionsBase,
    FlagOptionType,
    XYOptionsType,
    XYZOptionsType,
    UnsignedXYOptionsType,
    UnsignedXYZOptionsType,
    UnsignedNOptionType,
    NOptionType,
    UnsignedXOptionType,
    XOptionType,
)


class PrusaSlicerPriorityOptions(Enum):
    """
        Usage: prusa-slicer [ ACTIONS ] [ TRANSFORM ] [ OPTIONS ] [ file.stl ... ]
    """
    ACTIONS = 0
    TRANSFORM = 1
    OTHER_OPTIONS = 2
    OPTIONS = 3
    OTHER = 4

    def __str__(self):
        return self.name.lower()


class SerializerOptions(object):

    def __init__(self) -> None:
        self._SERIALIZE_OPTIONS = {
            FlagOptionType: lambda k, v: [self._replace_option_name(k)],
            XYOptionsType: lambda k, v: [self._replace_option_name(k), ','.join(map(str, v.value))],
            XYZOptionsType: lambda k, v: [self._replace_option_name(k), ','.join(map(str, v.value))],
            UnsignedXYOptionsType: lambda k, v: [self._replace_option_name(k), ','.join(map(str, v.value))],
            UnsignedXYZOptionsType: lambda k, v: [self._replace_option_name(k), ','.join(map(str, v.value))],
            UnsignedNOptionType: lambda k, v: [self._replace_option_name(k), str(v)],
            NOptionType: lambda k, v: [self._replace_option_name(k), str(v)],
            UnsignedXOptionType: lambda k, v: [self._replace_option_name(k), str(v)],
            XOptionType: lambda k, v: [self._replace_option_name(k), str(v)],
            ExistsDirNameType: lambda k, v: [self._replace_option_name(k), f'"{v}"'],
            ExistsDirType: lambda k, v: [self._replace_option_name(k), f'"{v}"'],
            ExistsFileType: lambda k, v: [self._replace_option_name(k), f'"{v}"'],
            str: lambda k, v: [self._replace_option_name(k), f'"{v}"'],
        }

    def _replace_option_name(self, option_name: str) -> str:
        return '--' + option_name.replace('_', '-')

    def _serialize_option(self, key: str, value: Any) -> list[str]:
        for option_type, func in self._SERIALIZE_OPTIONS.items():
            if isinstance(value, option_type):
                return func(key, value)
        raise TypeError(f"Unknown option type: {type(value)}")

    def _get_serialized_options(self, dct_options: dict[str, Any]) -> list[str]:
        attrs = []
        for k, v in dct_options.items():
            is_valid_type = any((isinstance(v, t) for t in self._SERIALIZE_OPTIONS.keys()))
            is_none = v is None
            if not is_valid_type and not is_none:
                raise ValueError(f"Option {k} has invalid type: {type(v)}")
            attrs.extend(self._serialize_option(k, v))
        return attrs


class PrusaCommandsOptionsBase(SerializerOptions, SlicerCommandsOptionsBase):
    _PRIORITY: Optional[PrusaSlicerPriorityOptions] = None

    def _get_all_options(self) -> list[str]:
        return self._get_serialized_options(self._get_dct_options())

    @property
    def priority(self) -> PrusaSlicerPriorityOptions:
        return super().priority


class PrusaSelfClearingCommandsOptionsBase(SerializerOptions, SelfClearingSlicerCommandsOptionsBase):
    _PRIORITY: Optional[PrusaSlicerPriorityOptions] = None

    def _get_all_options(self) -> list[str]:
        return self._get_serialized_options(self._get_dct_options())

    @property
    def priority(self) -> PrusaSlicerPriorityOptions:
        return super().priority


class PrusaActionsOptionsBase(PrusaSelfClearingCommandsOptionsBase):
    _PRIORITY = PrusaSlicerPriorityOptions.ACTIONS


class PrusaTransformOptionsBase(PrusaSelfClearingCommandsOptionsBase):
    _PRIORITY = PrusaSlicerPriorityOptions.TRANSFORM


class PrusaOtherOptionsBase(PrusaCommandsOptionsBase):
    _PRIORITY = PrusaSlicerPriorityOptions.OTHER_OPTIONS


class PrusaSlicedOptionsBase(PrusaCommandsOptionsBase):
    _PRIORITY = PrusaSlicerPriorityOptions.OPTIONS


class PrusaFileOptions(PrusaSelfClearingCommandsOptionsBase):
    _PRIORITY = PrusaSlicerPriorityOptions.OTHER

    def __init__(self):
        super().__init__()
        self.__lst_files: list[str] = []

    def _clear_attr(self) -> None:
        self.__lst_files = []

    def add_files(self, *files: str) -> None:
        self.__lst_files.extend(files)

    @property
    def all_options(self) -> list[str]:
        return self.__lst_files[:]


__all__ = [
    'PrusaActionsOptionsBase',
    'PrusaTransformOptionsBase',
    'PrusaSlicedOptionsBase',
    'PrusaOtherOptionsBase',
    'PrusaFileOptions',
]
