import os
from dotenv import load_dotenv

from FFFactory.utils.systems_util import ExistsDirType

load_dotenv()


class RenderConfig():
    TEMPLATES_DIR: ExistsDirType = ExistsDirType(os.getenv('TEMPLATES_DIR'))


class CalculateConfig():
    DEFAULT_OUTPUT_DIR: ExistsDirType = ExistsDirType(os.getenv('DEFAULT_OUTPUT_DIR'))


__all__ = [
    'RenderConfig',
    'CalculateConfig',
]
