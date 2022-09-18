from pydantic import BaseModel


class TimerTrigger(BaseModel):

    xgrowKey: str
    index: int
    hourStart: int
    minuteStart: int
    hourStop: int
    minuteStop: int
    lightCycle: int
    timerType: str
    deviceType: str  # enum


    class Config():
        orm_mode = True

class TimerTriggerToModify(BaseModel):

    index: int
    hourStart: int
    minuteStart: int
    hourStop: int
    minuteStop: int
    lightCycle: int
    timerType: str
    deviceType: str  # enum

    class Config():
        orm_mode = True

class AirSensorTrigger(BaseModel):


    xgrowKey: str
    index: int
    functionType: str
    value: int
    maxValue: int
    minValue: int
    compensation: int
    deviceType: str  # enum

    class Config():
        orm_mode = True


class AirSensorTriggerToModify(BaseModel):

    index: int
    functionType: str
    value: int
    maxValue: int
    minValue: int
    compensation: int
    deviceType: str  # enum

    class Config():
        orm_mode = True

class RawCustomDevice(BaseModel):
    xgrowKey: str
    index: int
    active: bool
    deviceFunction: str #SlotFunction.TIMER  ENUM TO DO
    working: bool
    deviceType: str  # enum
    class Config():
        orm_mode = True

class CustomDevice(BaseModel):


    xgrowKey: str
    index: int
    icon: str
    deviceName: str
    active: bool
    deviceFunction: str #SlotFunction.TIMER  ENUM TO DO
    working: bool
    reversal: bool
    deviceType: str  # enum
    timerTrigger: TimerTriggerToModify
    airSensorTrigger: AirSensorTriggerToModify
    class Config():
        orm_mode = True


class CustomDeviceToModify(BaseModel):

    index: int
    icon: str
    deviceName: str
    active: bool
    deviceFunction: str #SlotFunction.TIMER  ENUM TO DO
    working: bool
    reversal: bool
    deviceType: str  # enum
    timerTrigger: TimerTriggerToModify
    airSensorTrigger: AirSensorTriggerToModify
    class Config():
        orm_mode = True

    #TO DO timer = Column(Boolean)
    #triggerThreshold =
    #compensation =


