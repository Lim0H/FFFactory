from typing import Optional, Union

from .prusa_actions import PrusaActionsRunner
from .prusa_config import PrusaSlicerConfig
from .prusa_transform import PrusaTransform


class PrusaSlicer(PrusaActionsRunner, PrusaTransform):

    def __init__(self, arg: Union[str, PrusaSlicerConfig], config_path: Optional[str] = None) -> None:
        if isinstance(arg, str):
            config = PrusaSlicerConfig(arg, config_path)  # type: ignore
            self._initialize_from_config(config)
        else:
            raise TypeError(f"Unsupported type for argument: {type(arg)}")

    def _from_config_obj(self, config: PrusaSlicerConfig):
        self._initialize_from_config(config)

    def _initialize_from_config(self, config: PrusaSlicerConfig):
        self._config = config
        self._config_transform = config.transform_options
