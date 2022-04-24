from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from app.blog.database import Base
from sqlalchemy.orm import relationship

#DATABASE MODEL
class Pot(Base):
    __tablename__ = 'pot'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #setObjectName = Column(String)
    potID = Column(Integer)
    isAvailable = Column(String) # bool
    pumpWorkingTimeLimit = Column(Integer)
    autoWateringFunction = Column(String) # bool
    pumpWorkStatus = Column(String) # bool
    #lastWateredCycleTime = datetime.now()
    sensorOutput = Column(Integer)
    minimalHumidity = Column(Integer)
    maxSensorHumidityOutput = Column(Integer)
    minSensorHumidityOutput = Column(Integer)
    pumpWorkingTime = Column(Integer)
    wateringCycleTimeInHour = Column(Integer)
    manualWateredInSecond = Column(Integer)



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

