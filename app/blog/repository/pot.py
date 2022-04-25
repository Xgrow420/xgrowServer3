from sqlalchemy.orm import Session

from app.blog import models
from app.blog.schemas import schemas, schemasPot
from fastapi import HTTPException, status

def getPots(db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType.__contains__('user'):
        pots = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.xgrowKey).all()
    else:
        pots = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.name).all()

    potList = []
    for pot in pots:
        pot = schemasPot.Pot(
            xgrowKey= pot.xgrowKey,
            #setObjectName = Column(String)
            potID= pot.potID,
            isAvailable= pot.isAvailable,
            pumpWorkingTimeLimit= pot.pumpWorkingTimeLimit,
            autoWateringFunction= pot.autoWateringFunction,
            pumpWorkStatus= pot.pumpWorkStatus,
            #lastWateredCycleTime = datetime.now()
            sensorOutput= pot.sensorOutput,
            minimalHumidity= pot.minimalHumidity,
            maxSensorHumidityOutput= pot.maxSensorHumidityOutput,
            minSensorHumidityOutput= pot.minSensorHumidityOutput,
            pumpWorkingTime= pot.pumpWorkingTime,
            wateringCycleTimeInHour= pot.wateringCycleTimeInHour,
            manualWateredInSecond= pot.manualWateredInSecond
        )
        potList.append(pot)
    return potList

def createPot(potId: int, request: schemasPot.PotToModify, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType.__contains__('user'):
        xgrowKey = currentUser.xgrowKey
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.xgrowKey, models.Pot.potID == potId).first()
    else:
        xgrowKey = currentUser.name
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.name, models.Pot.potID == potId).first()

    #checking if pot already exists
    if pot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pot with the id {potId} is already exists")

    newPot = models.Pot(
        xgrowKey= xgrowKey,
        #setObjectName = Column(String)
        potID= potId,
        isAvailable= request.isAvailable,
        pumpWorkingTimeLimit= request.pumpWorkingTimeLimit,
        autoWateringFunction= request.autoWateringFunction,
        pumpWorkStatus= request.pumpWorkStatus,
        #lastWateredCycleTime = datetime.now()
        sensorOutput= request.sensorOutput,
        minimalHumidity= request.minimalHumidity,
        maxSensorHumidityOutput= request.maxSensorHumidityOutput,
        minSensorHumidityOutput= request.minSensorHumidityOutput,
        pumpWorkingTime= request.pumpWorkingTime,
        wateringCycleTimeInHour= request.wateringCycleTimeInHour,
        manualWateredInSecond= request.manualWateredInSecond
    )
    db.add(newPot)
    db.commit()
    db.refresh(newPot)
    return newPot

def getPot(potId: int, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType.__contains__('user'):
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.xgrowKey, models.Pot.potID == potId).first()
    else:
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.name, models.Pot.potID == potId).first()


    pot = schemasPot.Pot(
        xgrowKey= pot.xgrowKey,
        #setObjectName = Column(String)
        potID= pot.potID,
        isAvailable= pot.isAvailable,
        pumpWorkingTimeLimit= pot.pumpWorkingTimeLimit,
        autoWateringFunction= pot.autoWateringFunction,
        pumpWorkStatus= pot.pumpWorkStatus,
        #lastWateredCycleTime = datetime.now()
        sensorOutput= pot.sensorOutput,
        minimalHumidity= pot.minimalHumidity,
        maxSensorHumidityOutput= pot.maxSensorHumidityOutput,
        minSensorHumidityOutput= pot.minSensorHumidityOutput,
        pumpWorkingTime= pot.pumpWorkingTime,
        wateringCycleTimeInHour= pot.wateringCycleTimeInHour,
        manualWateredInSecond= pot.manualWateredInSecond
    )
    if not pot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pot with the id {potId} is not available")
    return pot

def updatePot(potId: int, request: schemasPot.PotToModify, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType.__contains__('user'):
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.xgrowKey, models.Pot.potID == potId)
    else:
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.name, models.Pot.potID == potId)

    if not pot.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pot with id {potId} not found")

    pot.update(request.dict())
    db.commit()
    return 'updated'
