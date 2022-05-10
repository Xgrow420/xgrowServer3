from sqlalchemy.orm import Session

from app.blog import models
from app.blog.schemas import schemas, schemasFan
from fastapi import HTTPException, status

from app.blog.xgrow.Climate import Climate
from app.blog.xgrow import XgrowInstance


def getFans(currentUser: schemas.User):

    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    schemasList = []
    for fan in xgrow.getFanList():
        schemasList.append(fan.getObjectSchema())

    return schemasList


def getFan(fanSlot: int, currentUser: schemas.User):

    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    return xgrow.getFanList().__getitem__(fanSlot - 1).getObjectSchema()


def setFanObject(request: schemasFan.FanToModify, currentUser: schemas.User):
    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    xgrow.getFanList().__getitem__(request.fanId - 1).saveObjectFromSchema(request)


def createFan(fanId: int, request: schemasFan.FanToModify, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType:
        xgrowKey = currentUser.xgrowKey
        fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.xgrowKey, models.Fan.fanId == fanId).first()
    else:
        xgrowKey = currentUser.name
        fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.name, models.Fan.fanId == fanId).first()

    #checking if pot already exists
    if fan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Fan with the id {fanId} is already exists")

    newFan = models.Fan(
        xgrowKey= xgrowKey,
        #setObjectName = Column(String)
        fanId= fanId,
        isAvailable=request.isAvailable,
        isWorked=request.isWorked,
        normalMode=request.normalMode,
        coldMode=request.coldMode,
        hotMode=request.hotMode,
        tempMax=request.tempMax,
        tempMin=request.tempMin,
        temperatureStatus=request.temperatureStatus  # ENUM <=========
    )
    db.add(newFan)
    db.commit()
    db.refresh(newFan)
    return newFan


def updateFan(fanId: int, request: schemasFan.FanToModify, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType:
        fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.xgrowKey, models.Fan.fanId == fanId)
    else:
        fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.name, models.Fan.fanId == fanId)

    if not fan.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Fan with id {fanId} not found")

    fan.update(request.dict())
    db.commit()
    return 'updated'
