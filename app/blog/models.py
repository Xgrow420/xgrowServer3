from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, ARRAY
from app.blog.database import Base
from sqlalchemy.orm import relationship

#DATABASE MODEL

class Air(Base):
    __tablename__ = 'air'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)

    airTemperature = Column(Integer)
    airHumidity = Column(Integer)

    airTemperatureLogList = Column(String)
    airHumidityLogList = Column(String)


class Pot(Base):
    __tablename__ = 'pot'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #setObjectName = Column(String)
    index = Column(Integer)
    active = Column(Boolean, default=False) # bool
    pumpWorkingTimeLimit = Column(Integer)
    autoWateringFunction = Column(Boolean, default=False) # bool
    pumpWorkStatus = Column(Boolean, default=False) # bool
    #lastWateredCycleTime = datetime.now()
    sensorOutput = Column(Integer)
    minimalHumidity = Column(Integer)
    maxSensorHumidityOutput = Column(Integer)
    minSensorHumidityOutput = Column(Integer)
    pumpWorkingTime = Column(Integer)
    wateringCycleTimeInHour = Column(Integer)
    manualWateredInSecond = Column(Integer)

class Fan(Base):
    __tablename__ = 'fan'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    index = Column(Integer)
    active = Column(Boolean, default=False)
    working = Column(Boolean, default=False)
    normalMode = Column(Boolean, default=False)
    coldMode = Column(Boolean, default=False)
    hotMode = Column(Boolean, default=False)
    tempMax = Column(Integer)
    tempMin = Column(Integer)
    temperatureStatus = Column(Integer) #ENUM <=========

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    xgrowKey = Column(String)
    userType = Column(Boolean)
    password = Column(String)

    #PotList = Column(List)


    blogs = relationship('Blog', back_populates="creator")

class CustomDevice(Base):
    __tablename__ = 'customDevice'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    index = Column(Integer)
    active = Column(Boolean)
    deviceFunction = Column(String) #SlotFunction.TIMER  ENUM TO DO
    working = Column(Boolean)

    timerTrigger = relationship('TimerTrigger', back_populates="creator")

    #TO DO timer = Column(Boolean)
    #triggerThreshold =
    #compensation =

class TimerTrigger(Base):
    __tablename__ = 'timerTrigger'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    index = Column(Integer)
    hourStart = Column(Integer)
    minuteStart = Column(Integer)
    hourStop = Column(Integer)
    minuteStop = Column(Integer)
    lightCycle = Column(Integer)

    customDevice_id = Column(Integer, ForeignKey('customDevice.id'))
    creator = relationship('CustomDevice', back_populates="timerTrigger")

class AirSensorTrigger(Base):
    __tablename__ = 'airSensorTrigger'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    index = Column(Integer)
    functionType = Column(String)
    value = Column(Integer)
    compensation = Column(Integer)




