from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas, schemasCustomDevice
from fastapi import HTTPException, status
from app.restApi.repository import customDevice
from app.utils.currentUserUtils import userUtils


def getAirSensorTriggers(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    airSensorTrigger: Query = db.query(models.AirSensorTrigger).filter(models.AirSensorTrigger.xgrowKey == xgrowKey).all()
    return airSensorTrigger


def getAirSensorTrigger(index: int, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    airSensorTrigger: Query = db.query(models.AirSensorTrigger).filter(
        models.AirSensorTrigger.xgrowKey == xgrowKey,
        models.AirSensorTrigger.index == index).first()
    if not airSensorTrigger:
        # TO Do create mock fan db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"timerTrigger with index {index} not found")
    else:
        return airSensorTrigger


def createAirSensorTrigger(request: schemasCustomDevice.AirSensorTriggerToModify, currentUser: schemas.User,
                           db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    airSensorTrigger: Query = db.query(models.AirSensorTrigger).filter(
        models.AirSensorTrigger.xgrowKey == xgrowKey,
        models.AirSensorTrigger.index == request.index)

    cD = customDevice.getCustomDevice(db, request.index, currentUser)
    if cD:
        if not airSensorTrigger.first():
            newAirSensorTrigger = models.AirSensorTrigger(
                xgrowKey=xgrowKey,
                index=request.index,
                functionType=request.functionType,
                value=request.value,
                compensation=request.compensation,
                customDevice_id=cD.id)
            db.add(newAirSensorTrigger)
            db.commit()
            db.refresh(newAirSensorTrigger)
            return newAirSensorTrigger
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"[!] airSensorTrigger with index: {request.index} is already exists")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] first create a CustomDevice with index: {request.index} to be able to create linked airSensorTrigger")


def updateAirSensorTrigger(request: schemasCustomDevice.AirSensorTriggerToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    airSensorTrigger: Query = db.query(models.AirSensorTrigger).filter(models.AirSensorTrigger.xgrowKey == xgrowKey,
                                                               models.AirSensorTrigger.index == request.index)

    if not airSensorTrigger.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"AirSensorTrigger with index {request.index} not found")
    else:
        airSensorTrigger.update(request.dict())
        db.commit()
        return 'updated'
