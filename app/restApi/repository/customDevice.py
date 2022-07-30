from fastapi import HTTPException, status
from sqlalchemy.orm import Session, Query

from app.data import models
from app.restApi.repository import timerTrigger, airSensorTrigger
from app.schemas import schemas, schemasCustomDevice
from app.utils.currentUserUtils import userUtils

from app.utils.schemasUtils import schemasUtils


def getCustomDevices(currentUser: schemas.User, db: Session):
    # if currentUser.userType
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    devices: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey).all()
    return devices


def getCustomDevice(db: Session, index: int, currentUser: schemas.User):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    device: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                  models.CustomDevice.index == index).first()
    if not device:
        # TO Do create mock slot db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"CustomDevice with id {index} not found")
    else:
        return device


def createCustomDevice(db: Session, request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    device: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                  models.CustomDevice.index == request.index)

    if device.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"CustomDevice for user {currentUser.name} with index {request.index} already exists")

    else:
        newCustomDevice = models.CustomDevice(xgrowKey=currentUser.xgrowKey,
                                              index=request.index,
                                              deviceFunction=request.deviceFunction,
                                              working=request.working,
                                              active=request.active)

        db.add(newCustomDevice)
        db.commit()
        db.refresh(newCustomDevice)

        '''auto create timerTrigger'''
        request.timerTrigger.index = request.index
        timerTrigger.createTimerTrigger(request.timerTrigger, currentUser, db)

        request.airSensorTrigger.index = request.index
        airSensorTrigger.createAirSensorTrigger(request.airSensorTrigger, currentUser, db)

        return newCustomDevice


def updateCustomDevice(db: Session, request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    customDevice: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                        models.CustomDevice.index == request.index)

    if not customDevice.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"TimerTrigger with index {request.index} not found")
    else:
        customDevice.update(schemasUtils.filterUnableToSave(request.dict()))

        '''auto update timerTrigger'''
        request.timerTrigger.index = request.index
        timerTrigger.updateTimerTrigger(request.timerTrigger, currentUser, db)

        request.airSensorTrigger.index = request.index
        airSensorTrigger.updateAirSensorTrigger(request.airSensorTrigger, currentUser, db)

        db.commit()
        return 'updated'
