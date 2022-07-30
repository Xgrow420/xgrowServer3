from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas, schemasCustomDevice
from fastapi import HTTPException, status
from app.restApi.repository import customDevice
from app.utils.currentUserUtils import userUtils


def getTimerTriggers(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    timerTriggers: Query = db.query(models.TimerTrigger).filter(models.TimerTrigger.xgrowKey == xgrowKey).all()
    return timerTriggers


def getTimerTrigger(index: int, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    timerTrigger: Query = db.query(models.TimerTrigger).filter(models.TimerTrigger.xgrowKey == xgrowKey,
                                      models.TimerTrigger.index == index).first()
    if not timerTrigger:
        # TO Do create mock fan db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"timerTrigger with index {index} not found")
    else:
        return timerTrigger


def createTimerTrigger(request: schemasCustomDevice.TimerTriggerToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    timerTrigger: Query = db.query(models.TimerTrigger).filter(models.TimerTrigger.xgrowKey == xgrowKey,
                                      models.TimerTrigger.index == request.index)

    cD = customDevice.getCustomDevice(db, request.index, currentUser)
    if cD:
        if not timerTrigger.first():
            newTimerTrigger = models.TimerTrigger(
                xgrowKey=currentUser.xgrowKey,
                index=request.index,
                hourStart=request.hourStart,
                minuteStart=request.minuteStart,
                hourStop=request.hourStop,
                minuteStop=request.minuteStop,
                lightCycle=request.lightCycle,
                timerType=request.timerType,
                customDevice_id=cD.id)
            db.add(newTimerTrigger)
            db.commit()
            db.refresh(newTimerTrigger)
            return newTimerTrigger
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"[!] timerTrigger with index: {request.index} is already exists")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] first create a CustomDevice with index: {request.index} to be able to create linked timerTrigger")

def updateTimerTrigger(request: schemasCustomDevice.TimerTriggerToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    timerTrigger: Query = db.query(models.TimerTrigger).filter(models.TimerTrigger.xgrowKey == xgrowKey,
                                      models.TimerTrigger.index == request.index)

    if not timerTrigger.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"TimerTrigger with index {request.index} not found")
    else:
        timerTrigger.update(request.dict())
        db.commit()
        return 'updated'
