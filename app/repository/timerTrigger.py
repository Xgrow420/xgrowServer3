from sqlalchemy.orm import Session

from app.data import models
from app.schemas import schemas, schemasPot, schemasCustomDevice
from fastapi import HTTPException, status
from app.repository import customDevice



def getTimerTriggers(currentUser: schemas.User, db: Session):
    timerTriggers = db.query(models.TimerTrigger).filter(models.TimerTrigger.xgrowKey == currentUser.xgrowKey).all()
    return timerTriggers


def getTimerTrigger(index: int, currentUser: schemas.User, db: Session):
    timerTrigger = db.query(models.TimerTrigger).filter(models.TimerTrigger.xgrowKey == currentUser.xgrowKey,
                                      models.TimerTrigger.index == index).first()
    if not timerTrigger:
        # TO Do create mock fan db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"timerTrigger with index {index} not found")
    else:
        return timerTrigger


def createTimerTrigger(request: schemasCustomDevice.TimerTriggerToModify, currentUser: schemas.User, db: Session):
    timerTrigger = db.query(models.TimerTrigger).filter(models.TimerTrigger.xgrowKey == currentUser.xgrowKey,
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
    timerTrigger = db.query(models.TimerTrigger).filter(models.TimerTrigger.xgrowKey == currentUser.xgrowKey,
                                      models.TimerTrigger.index == request.index)

    if not timerTrigger.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"TimerTrigger with index {request.index} not found")
    else:
        timerTrigger.update(request.dict())
        db.commit()
        return 'updated'
