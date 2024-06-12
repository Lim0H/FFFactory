

from enum import Enum


class PrusaOutputFilenameFormatFdm(Enum):
    """
    The macro language can be used in Output filename format field available in Print Settings -> Output options.
    In this context you can use all the configuration placeholders plus the following:
    https://help.prusa3d.com/article/list-of-placeholders_205643
    """

    DAY = '{day}'
    EXTRUDED_VOLUME = '{extruded_volume}'
    FILAMENT_PRESET = '{filament_preset}'
    HOUR = '{hour}'
    INITIAL_EXTRUDER = '{initial_extruder}'
    INITIAL_FILAMENT_TYPE = '{initial_filament_type}'
    INITIAL_TOOL = '{initial_tool}'
    INPUT_FILENAME_BASE = '{input_filename_base}'
    MINUTE = '{minute}'
    MONTH = '{month}'
    NORMAL_PRINT_TIME = '{normal_print_time}'
    NUM_EXTRUDERS = '{num_extruders}'
    NUM_INSTANCES = '{num_instances}'
    NUM_OBJECTS = '{num_objects}'
    NUM_PRINTING_EXTRUDERS = '{num_printing_extruders}'
    PHYSICAL_PRINTER_PRESET = '{physical_printer_preset}'
    PRINT_PRESET = '{print_preset}'
    PRINT_TIME = '{print_time}'
    PRINTER_PRESET = '{printer_preset}'
    PRINTING_FILAMENT_TYPES = '{printing_filament_types}'
    SCALE = '{scale}'
    SECOND = '{second}'
    SILENT_PRINT_TIME = '{silent_print_time}'
    TIMESTAMP = '{timestamp}'
    TOTAL_COST = '{total_cost}'
    TOTAL_TOOLCHANGES = '{total_toolchanges}'
    TOTAL_WEIGHT = '{total_weight}'
    TOTAL_WIPE_TOWER_COST = '{total_wipe_tower_cost}'
    TOTAL_WIPE_TOWER_FILAMENT = '{total_wipe_tower_filament}'
    USED_FILAMENT = '{used_filament}'
    VERSION = '{version}'
    YEAR = '{year}'

    def __str__(self):
        return self.value


class LogLevelEnum(Enum):
    FATAL = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4
    TRACE = 5


__all__ = [
    'PrusaOutputFilenameFormatFdm',
    'LogLevelEnum',
]
