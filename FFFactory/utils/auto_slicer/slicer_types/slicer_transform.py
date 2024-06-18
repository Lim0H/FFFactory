

from abc import ABC
from decimal import Decimal

from .slicer_config import SlicerConfigBase


class SlicerTransformBase(ABC):

    def __init__(self, config: SlicerConfigBase):
        self._config = config

    @property
    def config_transform(self) -> SlicerConfigBase:
        return self._config

    def set_align_xy(self, x: Decimal, y: Decimal) -> None:
        raise NotImplementedError()

    def set_center(self, x: Decimal, y: Decimal) -> None:
        raise NotImplementedError()

    def set_cut(self, z: Decimal) -> None:
        raise NotImplementedError()

    def set_delete_after_load(self, path: str) -> None:
        raise NotImplementedError()

    def set_dont_arrange(self) -> None:
        raise NotImplementedError()

    def set_duplicate(self, n: int) -> None:
        raise NotImplementedError()

    def set_duplicate_grid(self, x: Decimal, y: Decimal) -> None:
        raise NotImplementedError()

    def set_ensure_on_bed(self) -> None:
        raise NotImplementedError()

    def set_merge(self) -> None:
        raise NotImplementedError()

    def set_repair(self) -> None:
        raise NotImplementedError()

    def set_rotate(self, angle: Decimal) -> None:
        raise NotImplementedError()

    def set_rotate_x(self, angle: Decimal) -> None:
        raise NotImplementedError()

    def set_rotate_y(self, angle: Decimal) -> None:
        raise NotImplementedError()

    def set_scale(self, scale: Decimal) -> None:
        raise NotImplementedError()

    def set_scale_to_fit(self, x: Decimal, y: Decimal, z: Decimal) -> None:
        raise NotImplementedError()

    def set_split(self) -> None:
        raise NotImplementedError()


__all__ = ["SlicerTransformBase"]
