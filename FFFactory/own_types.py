from abc import ABC
from typing import TypeVar


T = TypeVar('T')


class BasicType(ABC):
    def __init__(self, value):
        self._value = value
        if not self._check_value_valid():
            raise ValueError('Value not valid. %s' % value)

    def _check_value_valid(self) -> bool:
        return True

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    @property
    def value(self):
        return self._value
