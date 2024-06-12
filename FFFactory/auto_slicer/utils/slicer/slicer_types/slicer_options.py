from abc import ABC, abstractmethod
from typing import Optional, Any


class SlicerCommandsOptionsBase(ABC):
    _PRIORITY: Optional[Any] = None

    @property
    def priority(self) -> Any:
        if self._PRIORITY is None:
            raise ValueError("Priority not set.")
        return self._PRIORITY

    def _get_dct_options(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            result[key] = value
        return result

    @abstractmethod
    def _get_all_options(self) -> list[str]:
        raise NotImplementedError()

    @property
    def all_options(self) -> list[str]:
        return self._get_all_options()

    def __repr__(self):
        return f"""Priority: {self.priority}
Options: {self._get_dct_options()}
            """


class SelfClearingSlicerCommandsOptionsBase(SlicerCommandsOptionsBase):

    def _clear_attr(self) -> None:
        for key in self._get_dct_options().keys():
            setattr(self, key, None)

    @property
    def all_options(self) -> list[str]:
        result = super().all_options
        self._clear_attr()
        return result


__all__ = [
    'SlicerCommandsOptionsBase',
    'SelfClearingSlicerCommandsOptionsBase',
]
