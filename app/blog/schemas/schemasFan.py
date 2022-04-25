from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class TemperatureStatus(Enum):

    HOT = 1
    COLD = 2
    NORMAL = 3


class Fan(BaseModel):

    xgrowKey: str
    fanId: int
    isAvailable: bool
    isWorked: bool
    normalMode: bool
    coldMode: bool
    hotMode: bool
    tempMax: int
    tempMin: int
    temperatureStatus: str #ENUM <=========

class FanToModify(BaseModel):

    isAvailable: bool
    isWorked: bool
    normalMode: bool
    coldMode: bool
    hotMode: bool
    tempMax: int
    tempMin: int
    temperatureStatus: str #ENUM <=========

class FanToShow(BaseModel):

    fanId: int
    isAvailable: bool
    isWorked: bool
    normalMode: bool
    coldMode: bool
    hotMode: bool
    tempMax: int
    tempMin: int
    temperatureStatus: str #ENUM <=========