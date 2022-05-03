from enum import Enum


class SlotFunction(Enum):

    TIMER = 1
    TEMPERATURE_MIN = 2
    TEMPERATURE_MAX = 3
    HUMIDITY_MIN = 4
    HUMIDITY_MAX = 5
    NULL = 6