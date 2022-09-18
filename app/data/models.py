from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, ARRAY
from sqlalchemy.orm import relationship
from typing import List

from app.data.database import Base


# DATABASE MODEL

class Air(Base):
    __tablename__ = 'air'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #device Section
    airTemperature = Column(Integer)
    airHumidity = Column(Integer)

    airTemperatureLogList = Column(String)
    airHumidityLogList = Column(String)


class Pot(Base):
    __tablename__ = 'pot'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    # setObjectName = Column(String)
    #device Section
    index = Column(Integer)
    potName = Column(String)
    active = Column(Boolean, default=False)  # bool
    manualWateringTimeLimit = Column(Integer)
    autoWateringFunction = Column(Boolean, default=False)  # bool
    pumpWorkStatus = Column(Boolean, default=False)  # bool
    lastWateredCycleTime = Column(Integer) #timestamp int
    currentSoilMoisture = Column(Integer)
    minMoisture = Column(Integer)
    maxSensorMoistureOutput = Column(Integer)
    minSensorMoistureOutput = Column(Integer)
    automaticWateringTime = Column(Integer)
    automaticWateringCycleDuration = Column(Integer)
    manualWateringTime = Column(Integer)


class Preferences(Base):
    __tablename__ = 'preferences'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)

    language = Column(String)
    temperatureFormat = Column(String)
    dateFormat = Column(String)

    #user_id = Column(Integer, ForeignKey('users.id'))
    #creator = relationship("User", back_populates="preferences")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    xgrowKey = Column(String)
    userType = Column(Boolean)
    password = Column(String)

    # PotList = Column(List)

    #preferences = relationship("Preferences", back_populates="creator")


class CustomDevice(Base):
    __tablename__ = "customDevice"

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #device Section
    index = Column(Integer)
    icon = Column(String)
    deviceName = Column(String)
    active = Column(Boolean)
    deviceFunction = Column(String)  # SlotFunction.TIMER  ENUM TO DO
    working = Column(Boolean)
    reversal = Column(Boolean)
    deviceType = Column(String)  # enum

    timerTrigger = relationship("TimerTrigger", back_populates="linkedDevice", uselist=False)
    airSensorTrigger = relationship("AirSensorTrigger", back_populates="linkedDevice", uselist=False)

    # TO DO timer = Column(Boolean)
    # triggerThreshold =
    # compensation =


class TimerTrigger(Base):
    __tablename__ = 'timerTrigger'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #device Section
    index = Column(Integer)
    hourStart = Column(Integer)
    minuteStart = Column(Integer)
    hourStop = Column(Integer)
    minuteStop = Column(Integer)
    lightCycle = Column(Integer)
    timerType = Column(String) #Enum
    deviceType = Column(String)

    customDevice_id = Column(Integer, ForeignKey('customDevice.id'))
    linkedDevice = relationship('CustomDevice', back_populates="timerTrigger")


class AirSensorTrigger(Base):
    __tablename__ = 'airSensorTrigger'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #device Section
    index = Column(Integer)
    functionType = Column(String)
    value = Column(Integer)
    maxValue = Column(Integer)
    minValue = Column(Integer)
    compensation = Column(Integer)
    deviceType = Column(String)

    customDevice_id = Column(Integer, ForeignKey('customDevice.id'))
    linkedDevice = relationship('CustomDevice', back_populates="airSensorTrigger")
    #end

class Sensors(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #device Section
    airTemperature = Column(Integer)
    airHumidity = Column(Integer)
    potsMoistureList = Column(String)
    camera = Column(String)



class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #device Section

    airTemperatureLogList = Column(String)
    airHumidityLogList = Column(String)
    events = Column(String)

    pot0MoistureLogList = Column(String)
    pot1MoistureLogList = Column(String)
    pot2MoistureLogList = Column(String)
    pot3MoistureLogList = Column(String)
    pot4MoistureLogList = Column(String)
    pot5MoistureLogList = Column(String)
    pot6MoistureLogList = Column(String)
    pot7MoistureLogList = Column(String)

