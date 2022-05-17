from enum import Enum


class SlotFunction(Enum):

    TIMER = 1
    TEMPERATURE_MIN = 2
    TEMPERATURE_MAX = 3
    HUMIDITY_MIN = 4
    HUMIDITY_MAX = 5
    NULL = 6

#SlotFunction.TIMER
#    @staticmethod
#    def fromString(input: str):
#        match input:
#            case 'TIMER':
#                return SlotFunction.TIMER
#            case 'b':
#                return SlotFunction.TEMPERATURE_MIN
#            case _:
#                return 'rip'

    @staticmethod
    def toString(self):
        pass