from pydantic import BaseModel


class CustomDevice(BaseModel):

    xgrowKey: str
    index: int
    active: bool
    deviceFunction: str #SlotFunction.TIMER  ENUM TO DO
    working: bool


class CustomDeviceToModify(BaseModel):

    index: int
    active: bool
    deviceFunction: str #SlotFunction.TIMER  ENUM TO DO
    working: bool

    #TO DO timer = Column(Boolean)
    #triggerThreshold =
    #compensation =

class Timer(BaseModel):

    xgrowKey: str
    index: int
    hourStart: int
    minuteStart: int
    hourStop: int
    minuteStop: int
    lightCycle: int

class TimerToModify(BaseModel):

    index: int
    hourStart: int
    minuteStart: int
    hourStop: int
    minuteStop: int
    lightCycle: int

class TemperatureMax(BaseModel):

    xgrowKey: str
    index: int
    tempMax: int
    compensation: int
    workFlag: bool


class TemperatureMaxToModify(BaseModel):

    index: int
    tempMax: int
    compensation: int
    workFlag: bool

class TemperatureMin(BaseModel):

    xgrowKey: str
    index: int
    tempMin: int
    compensation: int
    workFlag: bool

class TemperatureMinToModify(BaseModel):

    index: int
    tempMin: int
    compensation: int
    workFlag: bool

class HumidityMax(BaseModel):

    xgrowKey: str
    index: int
    humidityMax: int
    compensation: int
    workFlag: bool


class HumidityMaxToModify(BaseModel):

    index: int
    humidityMax: int
    compensation: int
    workFlag: bool

class HumidityMin(BaseModel):

    xgrowKey: str
    index: int
    humidityMin: int
    compensation: int
    workFlag: bool

class HumidityMinToModify(BaseModel):

    index: int
    humidityMin: int
    compensation: int
    workFlag: bool