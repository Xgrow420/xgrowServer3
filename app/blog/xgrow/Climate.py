import app.blog.xgrow.fan.Fan as fan
import app.blog.xgrow.pot.Pot as pot
import app.blog.xgrow.air.Air as air
import app.blog.xgrow.time.Time as time
import app.blog.xgrow.slot.SlotObjects as slot
from app.blog.schemas import schemas
from app.blog.xgrow.slot.SlotFunction import SlotFunction

fileName = 'climateObject.json'

climateObiect = ''

class Climate():


    def __init__(self, currentUser: schemas.User, potAmount, fanAmount, slotAmount):
        super().__init__()

        #self.setObjectName("Climate")

        #self.__simulator = SensorSimulator()
        '''hardware Chip object'''
        #self.__mcp23017 = Mcp23017()
        #self.__mcp3008 = Mcp3008(self.__simulator)
        #self.__eeprom = EEPROM()
        #self.__sht30 = SHT30(self.__simulator)

        #self.__gpio = XgrowGPIO(self.__mcp23017)

        self.__air = air.Air()

        potObjectList = self.__generate_potClassList(potAmount)
        fanObjectList = self.__generate_fanClassList(fanAmount)
        slotList = self.__generate_slotList(slotAmount)

        '''climate'''
        self.potList = potObjectList
        self.fanList = fanObjectList
        self.slotList = slotList
        self.time = time.CurrentTime()
        self.mechanicsSleepMode = []
        self.lightSleepMode = []

        '''User'''
        self.xgrowKey = currentUser.xgrowKey
        self.userName = currentUser.name


    def getPotList(self):
        '''
        :return: pot object list (Pot)
        '''
        return self.potList

    def getFanList(self):
        return self.fanList

    def getSlotList(self):
        return self.slotList

    def getAir(self):
        return self.__air

    def getTime(self):
        return self.time

    #def getGPIOExpander(self):
    #    return self.__mcp23017

    #def getAnalogGPIO(self):
    #    return self.__mcp3008

    #def getEEPROM(self):
    #    return self.__eeprom

    #def getAirSensor(self):
    #    return self.__sht30

    #def getSensorSimulator(self):
    #    '''return sensor Simulator object'''
    #    return self.__simulator


    def __generate_fanClassList(self, fanAmount):

        fan_list = []

        for val in range(1, fanAmount + 1):
            fanObject = fan.Fan(val)
            fan_list.append(fanObject)
        return fan_list

    def __generate_potClassList(self, potAmount):

        pot_list = []

        for val in range(1, potAmount + 1):
            potObject = pot.Pot(val)
            pot_list.append(potObject)
        return pot_list

    def __generate_slotList(self, slotAmount):

        slotList = []

        for val in range(1, slotAmount + 1):

            obj = slot.SlotObject(val)

            '''generate MOCK object'''
            if val == 1 | val == 2:
                obj.setSlotFunction(SlotFunction.TIMER)
            if val == 3:
                obj.setSlotFunction(SlotFunction.TEMPERATURE_MAX)
            if val == 4:
                obj.setSlotFunction(SlotFunction.TEMPERATURE_MIN)
            if val == 5:
                obj.setSlotFunction(SlotFunction.HUMIDITY_MAX)
            if val == 6:
                obj.setSlotFunction(SlotFunction.HUMIDITY_MIN)
            if val > 6:
                obj.setSlotFunction(SlotFunction.NULL)

            slotList.append(obj)
        return slotList

