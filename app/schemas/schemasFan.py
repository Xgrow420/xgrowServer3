import enum
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class TemperatureStatus(Enum):

    HOT = 1
    COLD = 2
    NORMAL = 3


class Fan(BaseModel):

    xgrowKey: str
    index: int
    fanName: str
    active: bool
    working: bool
    normalMode: bool
    coldMode: bool
    hotMode: bool
    tempMax: int
    tempMin: int
    temperatureStatus: int #ENUM <=========

    class Config():
        orm_mode = True

class FanToModify(BaseModel):

    index: int
    fanName: str
    active: bool
    working: bool
    normalMode: bool
    coldMode: bool
    hotMode: bool
    tempMax: int
    tempMin: int
    temperatureStatus: int #ENUM <=========

    class Config():
        orm_mode = True
