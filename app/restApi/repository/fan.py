from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas, schemasFan
from fastapi import HTTPException, status

from app.utils.currentUserUtils import userUtils
from app.websocket.repository.connectionManagerXgrow import getConnectionManagerXgrow


def getFans(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    fans: Query = db.query(models.Fan).filter(models.Fan.xgrowKey == xgrowKey).all()
    return fans


def getFan(index: int, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    fan: Query = db.query(models.Fan).filter(models.Fan.xgrowKey == xgrowKey,
                                      models.Fan.index == index).first()
    if not fan:
        # TO Do create mock fan db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Slot with id {index} not found")
    else:
        return fan


async def createFan(request: schemasFan.FanToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    fan: Query = db.query(models.Fan).filter(models.Fan.xgrowKey == xgrowKey,
                                      models.Fan.index == request.index)

    if not fan.first():
        newFan = models.Fan(xgrowKey=xgrowKey,
                            index=request.index,
                            fanName=request.fanName,
                            active=request.active,
                            working=request.working,
                            normalMode=request.normalMode,
                            coldMode=request.coldMode,
                            hotMode=request.hotMode,
                            tempMax=request.tempMax,
                            tempMin=request.tempMin,
                            temperatureStatus=request.temperatureStatus
                            )
        db.add(newFan)
        db.commit()
        db.refresh(newFan)
        if currentUser.userType:
            await getConnectionManagerXgrow().sendMessageToDevice(f"/download fan {request.index}", xgrowKey)

        return 'created'
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Fan for user {currentUser.name} with index: {request.index} is already exists")


async def updateFan(request: schemasFan.FanToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    fan: Query = db.query(models.Fan).filter(models.Fan.xgrowKey == xgrowKey,
                                      models.Fan.index == request.index)

    if not fan.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Fan for user {currentUser.name} with index {request.index} not found")

    else:
        fan.update(request.dict())
        db.commit()
        if currentUser.userType:
            await getConnectionManagerXgrow().sendMessageToDevice(f"/download fan {request.index}", xgrowKey)
        return 'updated'
