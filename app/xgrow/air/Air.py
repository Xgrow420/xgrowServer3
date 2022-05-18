
from app.schemas.schemasAir import Air as AirSchema
from app.schemas.schemasAir import AirToModify as AirToModifySchema
from app.utils import stringUtils

class Air():

    def __init__(self):
        super().__init__()

        #self.setObjectName("Air")

        self.xgrowKey = ''

        self.airTemperature = 0
        self.airHumidity = 0

        self.airTemperatureLogList = []
        self.airHumidityLogList = []

        #self.airTemperatureList = []
        #self.airHumidityList = []
        #self.averageMemoryLimit = 30
        #self.__sht30 = sht30

    #def getAirTemperatureFromSensor(self):
    #    '''return air temperature value reading from sensor SHT30'''
    #    self.__airTemperature = self.__sht30.getTemperatureCelsius()
    #    return self.__airTemperature

    #def getAirHumidityFromSensor(self):
    #    self.__airHumidity = self.__sht30.getAirHumidity()
    #    return self.__airHumidity

    def getAirHumidityLogList(self):
        '''this method return humidity logs - logs are used to graph'''
        '''logs is generated every main loop in main by AirModule'''
        return self.airHumidityLogList

    def setAirHumidityLogList(self, logList):
        '''UNUSED this method set humidityLogList to new list '''
        self.airHumidityLogList = logList

    def getAirTemperatureLogList(self):
        '''this method return temperature logs - logs are used to graph'''
        '''logs is generated every main loop in main by AirModule'''
        return self.airTemperatureLogList

    def setAirTemperatureLogList(self, logList):
        '''UNUSED this method set tempLogList to new list '''
        self.airTemperatureLogList = logList

    def getAverageMemoryLimit(self):
        '''return max Average memory limit'''
        return self.averageMemoryLimit

    def setAverageMemoryLimit(self, integer):
        '''set the memory limit for airHum/TempList'''
        self.averageMemoryLimit = integer

    #def humidityAverageUpdate(self):
    #    '''this method append air humidity read from air sensor dht22 to airHumidityList'''
    #    '''lenght limit of this list is equal to averageMemoryLimit'''

    #    self.__airHumidityList.append(self.getAirHumidityFromSensor())
    #    if len(self.__airHumidityList) > self.__averageMemoryLimit:
    #        del self.__airHumidityList[0]

    #def temperatureAverageUpdate(self):
    #    '''this method append air temperature read from air sensor dht22 to airTemperatureList'''
    #    '''lenght limit of this list is equal to averageMemoryLimit'''

    #    self.__airTemperatureList.append(self.getAirTemperatureFromSensor())
    #    if len(self.__airTemperatureList) > self.__averageMemoryLimit:
    #        del self.__airTemperatureList[0]

    '''Do sprawdzenia '''
    def getObjectSchema(self):
        return AirToModifySchema(airHumidity= self.airHumidity,
                           airTemperature= self.airTemperature,
                           airHumidityLogList= utils.convertListToString(self.airHumidityLogList),
                           airTemperatureLogList= utils.convertListToString(self.airTemperatureLogList)
                           )

    def saveObjectFromSchema(self, schema: AirToModifySchema):
        self.airHumidity = schema.airHumidity
        self.airTemperature = schema.airTemperature
        self.airTemperatureLogList = utils.convertStringToList(schema.airTemperatureLogList)
        self.airHumidityLogList = utils.convertStringToList(schema.airHumidityLogList)

