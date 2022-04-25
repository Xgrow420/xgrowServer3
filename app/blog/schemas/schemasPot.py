from typing import List, Optional
from pydantic import BaseModel


class Pot(BaseModel):

    xgrowKey: str
    # setObjectName = Column(String)
    potID: int
    isAvailable: bool  # bool
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

class PotToModify(BaseModel):

    # xgrowKey: str
    # setObjectName = Column(String)
    # potID: int
    isAvailable: bool  # bool
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

class PotToShow(BaseModel):

    # xgrowKey: str
    # setObjectName = Column(String)
    potID: int
    isAvailable: bool  # bool
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
