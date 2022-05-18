from typing import List, Optional
from pydantic import BaseModel


class Pot(BaseModel):

    xgrowKey: str
    # setObjectName = Column(String)
    index: int
    active: bool  # bool
    pumpWorkingTimeLimit: int
    autoWateringFunction: bool  # bool
    pumpWorkStatus: bool  # bool
    # lastWateredCycleTime = datetime.now()
    sensorOutput: int
    minimalHumidity: int
    maxSensorHumidityOutput: int
    minSensorHumidityOutput: int
    pumpWorkingTime: int
    wateringCycleTimeInHour: int
    manualWateredInSecond: int

    class Config():
        orm_mode = True

class PotToModify(BaseModel):

    # xgrowKey: str
    # setObjectName = Column(String)
    index: int
    active: bool  # bool
    pumpWorkingTimeLimit: int
    autoWateringFunction: bool  # bool
    pumpWorkStatus: bool  # bool
    # lastWateredCycleTime = datetime.now()
    sensorOutput: int
    minimalHumidity: int
    maxSensorHumidityOutput: int
    minSensorHumidityOutput: int
    pumpWorkingTime: int
    wateringCycleTimeInHour: int
    manualWateredInSecond: int

    class Config():
        orm_mode = True

