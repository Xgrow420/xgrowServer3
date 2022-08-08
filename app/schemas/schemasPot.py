from typing import List, Optional
from pydantic import BaseModel


class Pot(BaseModel):

    xgrowKey: str
    # setObjectName = Column(String)
    index: int
    potName: str
    active: bool  # bool
    manualWateringTimeLimit: int
    autoWateringFunction: bool  # bool
    pumpWorkStatus: bool  # bool
    lastWateredCycleTime: int
    currentSoilMoisture: int
    minMoisture: int
    maxSensorMoistureOutput: int
    minSensorMoistureOutput: int
    automaticWateringTime: int
    automaticWateringCycleDuration: int
    manualWateringTime: int

    class Config():
        orm_mode = True

class PotToModify(BaseModel):

    # xgrowKey: str
    # setObjectName = Column(String)
    index: int
    potName: str
    active: bool  # bool
    manualWateringTimeLimit: int
    autoWateringFunction: bool  # bool
    pumpWorkStatus: bool  # bool
    lastWateredCycleTime: int
    currentSoilMoisture: int
    minMoisture: int
    maxSensorMoistureOutput: int
    minSensorMoistureOutput: int
    automaticWateringTime: int
    automaticWateringCycleDuration: int
    manualWateringTime: int

    class Config():
        orm_mode = True

