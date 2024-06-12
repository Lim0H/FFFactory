from decimal import Decimal

from FFFactory.utils.systems_util import ExistsDirType
from .prusa_config import PrusaTransformOptions
from ..slicer_types import (
    SlicerTransformBase,
    FlagOptionType,
    UnsignedXYOptionsType,
    UnsignedNOptionType,
    UnsignedXOptionType,
    UnsignedXYZOptionsType,
    XYOptionsType,
    XOptionType,
)


class PrusaTransform(SlicerTransformBase):

    def __init__(self, config_transform: PrusaTransformOptions):
        self._config_transform = config_transform  # type: ignore

    @property
    def config_transform(self) -> PrusaTransformOptions:  # type: ignore
        return self._config_transform  # type: ignore

    def set_align_xy(self, x: Decimal, y: Decimal) -> None:
        self.config_transform.align_xy = XYOptionsType(x, y)

    def set_center(self, x: Decimal, y: Decimal) -> None:
        self.config_transform.center = XYOptionsType(x, y)

    def set_cut(self, z: Decimal) -> None:
        self.config_transform.cut = XOptionType(z)

    def set_delete_after_load(self, path: str) -> None:
        self.config_transform.delete_after_load = ExistsDirType(path)

    def set_dont_arrange(self) -> None:
        self.config_transform.dont_arrange = FlagOptionType()

    def set_duplicate(self, n: int) -> None:
        self.config_transform.duplicate = UnsignedNOptionType(n)

    def set_duplicate_grid(self, x: Decimal, y: Decimal) -> None:
        self.config_transform.duplicate_grid = UnsignedXYOptionsType(x, y)

    def set_ensure_on_bed(self) -> None:
        self.config_transform.ensure_on_bed = FlagOptionType()

    def set_merge(self) -> None:
        self.config_transform.merge = FlagOptionType()

    def set_repair(self) -> None:
        self.config_transform.repair = FlagOptionType()

    def set_rotate(self, angle: Decimal) -> None:
        self.config_transform.rotate = XOptionType(angle)

    def set_rotate_x(self, angle: Decimal) -> None:
        self.config_transform.rotate_x = XOptionType(angle)

    def set_rotate_y(self, angle: Decimal) -> None:
        self.config_transform.rotate_y = XOptionType(angle)

    def set_scale(self, scale: Decimal) -> None:
        self.config_transform.scale = UnsignedXOptionType(scale)

    def set_scale_to_fit(self, x: Decimal, y: Decimal, z: Decimal) -> None:
        self.config_transform.scale_to_fit = UnsignedXYZOptionsType(x, y, z)

    def set_split(self) -> None:
        self.config_transform.split = FlagOptionType()


__all__ = ["PrusaTransform"]
