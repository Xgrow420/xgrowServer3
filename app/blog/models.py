from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum
from app.blog.database import Base
from sqlalchemy.orm import relationship

#DATABASE MODEL
class Pot(Base):
    __tablename__ = 'pot'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #setObjectName = Column(String)
    potID = Column(Integer)
    isAvailable = Column(Boolean, default=False) # bool
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
    fanId = Column(Integer)
    isAvailable = Column(Boolean, default=False)
    isWorked = Column(Boolean, default=False)
    normalMode = Column(Boolean, default=False)
    coldMode = Column(Boolean, default=False)
    hotMode = Column(Boolean, default=False)
    tempMax = Column(Integer)
    tempMin = Column(Integer)
    temperatureStatus = Column(String) #ENUM <=========

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
    userType = Column(String)
    password = Column(String)

    #PotList = Column(List)


    blogs = relationship('Blog', back_populates="creator")

