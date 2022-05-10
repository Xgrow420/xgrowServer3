from sqlalchemy.orm import Session

from app.blog import models
from app.blog.schemas import schemas, schemasPot
from fastapi import HTTPException, status

from app.blog.xgrow import XgrowInstance
from app.blog.xgrow.Climate import Climate


def getPots(currentUser: schemas.User):

    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    schemasList = []
    for pot in xgrow.getPotList():
        schemasList.append(pot.getObjectSchema())

    return schemasList


def getPot(potSlot: int, currentUser: schemas.User):

    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    return xgrow.getPotList().__getitem__(potSlot - 1).getObjectSchema()


def setPotObject(request: schemasPot.PotToModify, currentUser: schemas.User):
    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    xgrow.getPotList().__getitem__(request.potID - 1).saveObjectFromSchema(request)


def createPot(potId: int, request: schemasPot.PotToModify, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType:
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

def updatePot(potId: int, request: schemasPot.PotToModify, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType:
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.xgrowKey, models.Pot.potID == potId)
    else:
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.name, models.Pot.potID == potId)

    if not pot.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pot with id {potId} not found")

    pot.update(request.dict())
    db.commit()
    return 'updated'
