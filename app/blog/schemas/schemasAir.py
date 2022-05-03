from typing import List, Optional
from pydantic import BaseModel


class Air(BaseModel):

    xgrowKey: str

    airTemperature: int
    airHumidity: int

    airTemperatureLogList: str
    airHumidityLogList: str

class AirToModify(BaseModel):

    airTemperature: int
    airHumidity: int

    airTemperatureLogList: str
    airHumidityLogList: str

class AirToShow(BaseModel):

    airTemperature: int
    airHumidity: int

    airTemperatureLogList: str
    airHumidityLogList: str