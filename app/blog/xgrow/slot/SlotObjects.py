from app.blog.schemas.schemasCustomDevice import CustomDeviceToModify, TimerToModify, TemperatureMaxToModify, TemperatureMinToModify, \
    HumidityMaxToModify, HumidityMinToModify
from app.blog.xgrow.slot.CustomDeviceFunction import CustomDeviceFunction


class SlotObject():

    def __init__(self, slotID):
        super().__init__()

        # self.setObjectName(f"Slot:{slotID}")

        # self.__gpio = gpio
        self.xgrowKey = ''

        self.__slotId = slotID
        self.__slotFunction = CustomDeviceFunction.TIMER
        self.__slotWorkMode = False
        self.__workReversal = False

        self.__timerObject = Timer(slotID)
        self.__temperatureMax = TemperatureMax(slotID)
        self.__temperatureMin = TemperatureMin(slotID)
        self.__humidityMax = HumidityMax(slotID)
        self.__humidityMin = HumidityMin(slotID)

    def getSlotID(self):
        return self.__slotId

    def getSlotFunction(self):
        return self.__slotFunction

    def setSlotFunction(self, slotFunction: CustomDeviceFunction):
        self.__slotFunction = slotFunction

    def getSlotWorkMode(self):
        return self.__slotWorkMode

    def setSlotWorkMode(self, boolean):
        self.__slotWorkMode = boolean

    def isWorkReversal(self):
        return self.__workReversal

    def setWorkReversal(self, boolean):
        self.__workReversal = boolean

    def getTimerObject(self):
        return self.__timerObject

    def getMaxTemperatureObject(self):
        return self.__temperatureMax

    def getMinTemperatureObject(self):
        return self.__temperatureMin

    def getMaxHumidityObject(self):
        return self.__humidityMax

    def getMinHumidityObject(self):
        return self.__humidityMin

    def getObjectSchema(self):
        return CustomDeviceToModify(slotId=self.__slotId,
                                    slotFunction=self.__slotFunction,
                                    slotWorkMode=self.__slotWorkMode,
                                    workReversal=self.__workReversal
                                    )

    def saveObjectFromSchema(self, schema: CustomDeviceToModify):
        self.__slotId = schema.slotId
        self.__slotFunction = schema.slotFunction
        self.__slotWorkMode = schema.slotWorkMode
        self.__workReversal = schema.workReversal


class Timer():
    def __init__(self, slotID):
        super().__init__()

        # self.setObjectName(f"Timer:{slotID}")
        self.xgrowKey = ''
        self.__slotId = slotID
        self.__hourStart = 12
        self.__minuteStart = 56
        self.__hourStop = 13
        self.__minuteStop = 0
        self.__lightCycle = 12

    def getStartHour(self):
        return self.__hourStart

    def setStartHour(self, integer):
        if integer > 0 & integer <= 24:
            self.__hourStart = integer

    def getStartMinute(self):
        return self.__minuteStart

    def setStartMinute(self, integer):
        if integer > 0 & integer <= 60:
            self.__minuteStart = integer

    def getStopHour(self):
        return self.__hourStop

    def setStopHour(self, integer):
        if integer > 0 & integer <= 24:
            self.__hourStop = integer

    def getStopMinute(self):
        return self.__minuteStop

    def setStopMinute(self, integer):
        if integer > 0 & integer <= 60:
            self.__minuteStop = integer

    def getLightCycle(self):
        return self.__lightCycle

    def setLightCycle(self, integer):
        if integer > 0 & integer <= 24:
            self.__lightCycle = integer

    def getObjectSchema(self):
        return TimerToModify(slotId=self.__slotId,
                             hourStart=self.__hourStart,
                             minuteStart=self.__minuteStart,
                             hourStop=self.__hourStop,
                             minuteStop=self.__minuteStop,
                             lightCycle=self.__lightCycle
                             )

    def saveObjectFromSchema(self, schema: TimerToModify):
        self.__slotId = schema.slotId
        self.__hourStart = schema.hourStart
        self.__minuteStart = schema.minuteStart
        self.__hourStop = schema.hourStop
        self.__minuteStop = schema.minuteStop
        self.__lightCycle = schema.lightCycle


class TemperatureMax():
    def __init__(self, slotID):
        super().__init__()

        # self.setObjectName(f"TemperatureMax:{slotID}")
        self.xgrowKey = ''
        self.__tempMax = 30
        self.__compensation = 0
        self.__workFlag = False

    def getMaxTemperature(self):
        return self.__tempMax

    def setMaxTemperature(self, integer):
        self.__tempMax = integer

    def getCompensation(self):
        return self.__compensation

    def setCompensation(self, integer):
        if integer >= 0:
            self.__compensation = integer

    def isSlotWorking(self):
        return self.__workFlag

    def setSlotWorking(self, boolean):
        self.__workFlag = boolean

    def getObjectSchema(self):
        return TemperatureMaxToModify(tempMax=self.__tempMax,
                                      compensation=self.__compensation,
                                      workFlag=self.__workFlag
                                      )

    def saveObjectFromSchema(self, schema: TemperatureMaxToModify):
        self.__tempMax = schema.tempMax
        self.__compensation = schema.compensation
        self.__workFlag = schema.workFlag



class TemperatureMin():
    def __init__(self, slotID):
        super().__init__()

        # self.setObjectName(f"TemperatureMin:{slotID}")
        self.xgrowKey = ''
        self.__tempMin = 15
        self.__compensation = 0
        self.__workFlag = False

    def getMinTemperature(self):
        return self.__tempMin

    def setMinTemperature(self, double):
        if double >= 0:
            self.__tempMin = double

    def getCompensation(self):
        return self.__compensation

    def setCompensation(self, double):
        if double >= 0:
            self.__compensation = double

    def isSlotWorking(self):
        return self.__workFlag

    def setSlotWorking(self, boolean):
        self.__workFlag = boolean

    def getObjectSchema(self):
        return TemperatureMinToModify(
        )

    def saveObjectFromSchema(self, schema: TemperatureMinToModify):

        pass


class HumidityMax():
    def __init__(self, slotID):
        super().__init__()

        # self.setObjectName(f"HumidityMax:{slotID}")
        self.xgrowKey = ''
        self.__humidityMax = 85
        self.__compensation = 0
        self.__workFlag = False

    def getMaxHumidity(self):
        return self.__humidityMax

    def setMaxHumidity(self, double):
        if double >= 0:
            self.__humidityMax = double

    def getCompensation(self):
        return self.__compensation

    def setCompensation(self, integer):
        if integer >= 0:
            self.__compensation = integer

    def isSlotWorking(self):
        return self.__workFlag

    def setSlotWorking(self, boolean):
        self.__workFlag = boolean

    def getObjectSchema(self):
        return HumidityMaxToModify(
        )

    def saveObjectFromSchema(self, schema: HumidityMaxToModify):
        pass


class HumidityMin():
    def __init__(self, slotID):
        super().__init__()

        # self.setObjectName(f"HumidityMin:{slotID}")
        self.xgrowKey = ''
        self.__humidityMin = 25
        self.__compensation = 0
        self.__workFlag = False

    def getMinHumidity(self):
        return self.__humidityMin

    def setMinHumidity(self, double):
        if double >= 0:
            self.__humidityMin = double

    def getCompensation(self):
        return self.__compensation

    def setCompensation(self, integer):
        if integer >= 0:
            self.__compensation = integer

    def isSlotWorking(self):
        return self.__workFlag

    def setSlotWorking(self, boolean):
        self.__workFlag = boolean

    def getObjectSchema(self):
        return HumidityMinToModify(
        )

    def saveObjectFromSchema(self, schema: HumidityMinToModify):
        pass
