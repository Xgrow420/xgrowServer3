from pydantic import BaseModel


class Slot(BaseModel):

    xgrowKey: str
    slotId: int
    slotFunction: str #SlotFunction.TIMER  ENUM TO DO
    slotWorkMode: bool
    workReversal: bool


class SlotToModify(BaseModel):

    slotId: int
    slotFunction: str #SlotFunction.TIMER  ENUM TO DO
    slotWorkMode: bool
    workReversal: bool

class Timer(BaseModel):

    xgrowKey: str
    slotId: int
    hourStart: int
    minuteStart: int
    hourStop: int
    minuteStop: int
    lightCycle: int

class TimerToModify(BaseModel):

    slotId: int
    hourStart: int
    minuteStart: int
    hourStop: int
    minuteStop: int
    lightCycle: int

class TemperatureMax(BaseModel):

    xgrowKey: str
    slotId: int
    tempMax: int
    compensation: int
    workFlag: bool


class TemperatureMaxToModify(BaseModel):

    slotId: int
    tempMax: int
    compensation: int
    workFlag: bool

class TemperatureMin(BaseModel):

    xgrowKey: str
    slotId: int
    tempMin: int
    compensation: int
    workFlag: bool

class TemperatureMinToModify(BaseModel):

    slotId: int
    tempMin: int
    compensation: int
    workFlag: bool

class HumidityMax(BaseModel):

    xgrowKey: str
    slotId: int
    humidityMax: int
    compensation: int
    workFlag: bool


class HumidityMaxToModify(BaseModel):

    slotId: int
    humidityMax: int
    compensation: int
    workFlag: bool

class HumidityMin(BaseModel):

    xgrowKey: str
    slotId: int
    humidityMin: int
    compensation: int
    workFlag: bool

class HumidityMinToModify(BaseModel):

    slotId: int
    humidityMin: int
    compensation: int
    workFlag: bool