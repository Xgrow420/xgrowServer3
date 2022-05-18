from sqlalchemy.orm import Session

from app.blog import models
from app.blog.schemas import schemas, schemasCustomDevice
from fastapi import HTTPException, status

from app.blog.schemas.schemasCustomDevice import TimerTriggerToModify, TimerTrigger
from app.blog.xgrow import XgrowInstance
from app.blog.xgrow.Climate import Climate


def getCustomDevices(currentUser: schemas.User, db: Session):
    # if currentUser.userType
    devices = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == currentUser.xgrowKey).all()
    return devices


def getCustomDevice(db: Session, index: int, currentUser: schemas.User):
    device = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == currentUser.xgrowKey,
                                                  models.CustomDevice.index == index).first()
    if not device:
        # TO Do create mock slot db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Slot with id {index} not found")
    else:
        return device


def setCustomDevice(db: Session, request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User):
    device = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == currentUser.xgrowKey,
                                                  models.CustomDevice.index == request.index)


    if device.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Slot for user {currentUser.xgrowKey} and index {request.index} already exists")

    else:
        newCustomDevice = models.CustomDevice(xgrowKey=currentUser.xgrowKey,
                                              index=request.index,
                                              deviceFunction=request.deviceFunction,
                                              working=request.working,
                                              active=request.active)

        db.add(newCustomDevice)
        db.commit()
        db.refresh(newCustomDevice)

        timerTrigger = models.TimerTrigger(
            xgrowKey=currentUser.xgrowKey,
            index=request.timerTrigger.index,
            hourStart=request.timerTrigger.hourStart,
            minuteStart=request.timerTrigger.minuteStart,
            hourStop=request.timerTrigger.hourStop,
            minuteStop=request.timerTrigger.minuteStop,
            lightCycle=request.timerTrigger.lightCycle,
            customDevice_id=newCustomDevice.id)

        db.add(timerTrigger)
        db.commit()
        db.refresh(newCustomDevice)

        print(newCustomDevice)

        return newCustomDevice
