from sqlalchemy.orm import Session

from app.blog import models
from app.blog.schemas import schemas, schemasFan
from fastapi import HTTPException, status

def getFans(db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType.__contains__('user'):
        fans = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.xgrowKey).all()
    else:
        fans = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.name).all()

    fanList = []
    for fan in fans:
        fan = schemasFan.Fan(
            xgrowKey= fan.xgrowKey,
            fanId= fan.fanId,
            isAvailable= fan.isAvailable,
            isWorked= fan.isWorked,
            normalMode= fan.normalMode,
            coldMode= fan.coldMode,
            hotMode= fan.hotMode,
            tempMax= fan.tempMax,
            tempMin= fan.tempMin,
            temperatureStatus= fan.temperatureStatus  # ENUM <=========
        )
        fanList.append(fan)
    return fanList

def createFan(fanId: int, request: schemasFan.FanToModify, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType.__contains__('user'):
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

def getFan(fanId: int, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType.__contains__('user'):
        fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.xgrowKey, models.Fan.fanId == fanId).first()
    else:
        fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.name, models.Fan.fanId == fanId).first()

    fan = schemasFan.Fan(
        xgrowKey=fan.xgrowKey,
        fanId=fan.fanId,
        isAvailable=fan.isAvailable,
        isWorked=fan.isWorked,
        normalMode=fan.normalMode,
        coldMode=fan.coldMode,
        hotMode=fan.hotMode,
        tempMax=fan.tempMax,
        tempMin=fan.tempMin,
        temperatureStatus=fan.temperatureStatus  # ENUM <=========
    )
    if not fan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Fan with the id {fanId} is not available")
    return fan

def updateFan(fanId: int, request: schemasFan.FanToModify, db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType.__contains__('user'):
        fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.xgrowKey, models.Fan.fanId == fanId)
    else:
        fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.name, models.Fan.fanId == fanId)

    if not fan.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Fan with id {fanId} not found")

    fan.update(request.dict())
    db.commit()
    return 'updated'
