from pydantic import BaseModel


class TimerTrigger(BaseModel):

    xgrowKey: str
    index: int
    hourStart: int
    minuteStart: int
    hourStop: int
    minuteStop: int
    lightCycle: int


    class Config():
        orm_mode = True

class TimerTriggerToModify(BaseModel):

    index: int
    hourStart: int
    minuteStart: int
    hourStop: int
    minuteStop: int
    lightCycle: int

    class Config():
        orm_mode = True

class AirSensorTrigger(BaseModel):


    xgrowKey: str
    index: int
    functionType: str
    value: int
    compensation: int

    class Config():
        orm_mode = True


class AirSensorTriggerToModify(BaseModel):

    index: int
    functionType: str
    value: int
    compensation: int

    class Config():
        orm_mode = True


class CustomDevice(BaseModel):

    xgrowKey: str
    index: int
    active: bool
    deviceFunction: str #SlotFunction.TIMER  ENUM TO DO
    working: bool
    timerTrigger: TimerTrigger
    class Config():
        orm_mode = True


class CustomDeviceToModify(BaseModel):

    index: int
    active: bool
    deviceFunction: str #SlotFunction.TIMER  ENUM TO DO
    working: bool
    timerTrigger: TimerTrigger
    class Config():
        orm_mode = True

    #TO DO timer = Column(Boolean)
    #triggerThreshold =
    #compensation =


