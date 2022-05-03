from datetime import datetime


class Pot():
    '''All pots variable & method'''

    def __init__(self, pot_id, data=None):
        super().__init__()

        #self.setObjectName(f"Pot:{pot_id}")

        self.xgrowKey = ''

        self.potID = pot_id
        self.isAvailable = False
        self.pumpWorkingTimeLimit = 600
        self.autoWateringFunction = False
        self.pumpWorkStatus = False
        self.lastWateredCycleTime = datetime.now()
        self.sensorOutput = 0
        self.minimalHumidity = 50
        self.maxSensorHumidityOutput = 750
        self.minSensorHumidityOutput = 0
        self.pumpWorkingTime = 10
        self.wateringCycleTimeInHour = 1
        self.manualWateredInSecond = 0
        #self._mcp3008 = mcp3008
        #self.__gpio = gpio

        self._potHumidityLogList = []
        self._potHumidityList = []
        self._averageMemoryLimit = 30


        if data is not None:
            self.__dict__ = data


    def getPotId(self):
        '''return ID of current Pot object'''
        return self.potID

    def isAvailable(self):
        '''return boolean: True if Pot is available'''
        return self.isAvailable

    def setAvailable(self, boolean: bool):
        '''set Pot to Available'''
        self.isAvailable = boolean

    #def getHumiditySensorOutput(self):
    #    '''Read analog signal from the mcp3008 sensor (soil moisture)'''
    #    self._sensorOutput = self._mcp3008.analogRead(self._potID - 1)
    #    return self._sensorOutput

    def getMaxHumidity(self):
        '''return maxHumidity'''
        return self.maxSensorHumidityOutput

    def setMaxHumidity(self, integer):
        if integer > self.minSensorHumidityOutput:
            self.maxSensorHumidityOutput = integer

    def getMinHumidity(self):
        return self.minSensorHumidityOutput

    def setMinHumidity(self, integer):
        if integer < self.maxSensorHumidityOutput:
            self.minSensorHumidityOutput = integer

    def getPumpWorkingTime(self):
        return self.pumpWorkingTime

    def setPumpWorkingTime(self, integer):
        if integer >= 0:
            if integer <= self.pumpWorkingTimeLimit:
                self.pumpWorkingTime = integer

    def getWateringCycleTime(self):
        return self.wateringCycleTimeInHour

    def setPumpCycleLoop(self, integer):
        if integer > 0:
            self.wateringCycleTimeInHour = integer

    def isAutoWatering(self):
        return self.autoWateringFunction

    def setAutoWatering(self, boolean):
        self.autoWateringFunction = boolean

    def getLastWateredCycleTime(self):
        return self.lastWateredCycleTime

    def setLastWateredCycleTime(self):
        self.lastWateredCycleTime = datetime.now()

    def isPumpWorking(self):
        return self.pumpWorkStatus

    #def setPumpWorking(self, boolean):
    #    '''method set PumpWorking to boolean and run GPIO pin '''
    #    if boolean:
    #        self.__gpio.getGPIOExpander().setGpio(self.getPotId(), True)
    #    else:
    #        self.__gpio.getGPIOExpander().setGpio(self.getPotId(),
    #                                              False)

    #    self._pumpWorkStatus = boolean

    def getMinimalHumidity(self):
        return self.minimalHumidity

    def setMinimalHumidity(self, integer):
        self.minimalHumidity = integer

    def getHumidityLogList(self):
        return self._potHumidityLogList

    def setHumidityLogList(self, logList):
        self._potHumidityLogList = logList

    def getAverageMemoryLimit(self):
        return self._averageMemoryLimit

    def setAverageMemoryLimit(self, integer):
        self._averageMemoryLimit = integer

    #def humidityAverageUpdate(self):
    #    '''this method append soil moisture read from air sensor Mcp3008 to potHumidityList'''
    #    '''lenght limit of this list is equal to averageMemoryLimit'''

    #    self._potHumidityList.append(self.getHumiditySensorOutput())
    #    if len(self._potHumidityList) > self._averageMemoryLimit:
    #        del self._potHumidityList[0]

    def getHumidityAverage(self):
        '''This method return Average '''
        humidity = 0
        for val in self._potHumidityList:
            humidity += val
        try:
            humidity = humidity / len(self._potHumidityList)
            return humidity
        except ZeroDivisionError:
            return 0

