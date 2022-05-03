from app.blog.xgrow.fan.FanStatus import TemperatureStatus

class Fan():
    ''' All fan variable & method '''

    def __init__(self, fan_id):
        super().__init__()

        #self.setNonSaveObject(['_Fan__air'])
        #self.setObjectName(f"Fan:{fan_id}")

        #self.__air = air
        #self.__gpio = gpio

        self.xgrowKey = ''

        self.fanId = fan_id
        self.isAvailable = False
        self.isWorked = False
        self.normalMode = False
        self.coldMode = False
        self.hotMode = False

        self.tempMax = 25
        self.tempMin = 20

        self.temperatureStatus = TemperatureStatus.NORMAL

        self.tempRangeMax = 50
        self.tempRangeMin = 5


    #@classmethod
    #def fromDTO(cls, fanDTO):
    #    return cls(fanDTO.fan_id)

    def getFanID(self):
        return self.fanId

    def getStatus(self):
        return self.temperatureStatus

    def setStatus(self, status: TemperatureStatus):
        self.temperatureStatus = status


    def isWorked(self):
        '''TO DO add if statement: GPIO fan-pin read'''
        '''work_mode variable auto update'''
        return self.isWorked

    def setWork(self, boolean: bool):
        self.isWorked = boolean

    def isAvailable(self):
        return self.isAvailable

    def setAvailable(self, boolean: bool):
        self.isAvailable = boolean

    def hasNormalWorkMode(self):
        return self.normalMode

    def setNormalWorkMode(self, boolean: bool):
        self.normalMode = boolean

    def hasColdWorkMode(self):
        return self.coldMode

    def setColdWorkMode(self, boolean: bool):
        self.coldMode = boolean

    def hasHotWorkMode(self):
        return self.hotMode

    def setHotWorkMode(self, bolean: bool):
        self.hotMode = bolean

    #def fanWorkUpdate(self):
    #    if self.__isWorked == True:
    #        '''TO DO add GPIO pinout run'''
    #        print(f"fan work mode: {self.__isWorked}")
    #    else:
    #        '''TO DO add GPIO pinout run'''
    #        print(f"fan work mode: {self.__isWorked}")

    def getTempMax(self):
        return self.tempMax
    def setTempMax(self):
        return self.tempMax

    def getTempMin(self):
        return self.tempMin
    def setTempMin(self):
        return self.tempMin

    #def getFanTemperatureStatus(self):

    #    airTemperature = self.__air.getTemperatureAverage()

    #    if airTemperature > self.__tempMax:
    #        self.__temperatureStatus = TemperatureStatus.HOT

    #    elif airTemperature < self.__tempMin:
    #        self.__temperatureStatus = TemperatureStatus.COLD

    #    else:
    #        self.__temperatureStatus = TemperatureStatus.NORMAL

    #    return self.__temperatureStatus


    def addToTempMax(self, value):

        if self.tempMax + value <= self.tempRangeMax:
            self.tempMax += value
        else:
            return Exception

    def subtractFromTempMax(self, value):

        if self.tempMax - value > self.tempRangeMin:
            self.tempMax -= value
        else:
            return Exception

    def addToTempMin(self, value):

        if self.tempMin + value < self.tempRangeMax:
            self.tempMin += value
        else:
            return Exception

    def subtractFromTempMin(self, value):

        if self.tempMin - value >= self.tempRangeMin:
            self.tempMin -= value
        else:
            return Exception