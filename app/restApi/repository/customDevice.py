from fastapi import HTTPException, status
from sqlalchemy.orm import Session, Query

from app.data import models
from app.restApi.repository import timerTrigger, airSensorTrigger
from app.schemas import schemas, schemasCustomDevice
from app.utils.currentUserUtils import userUtils

from app.utils.schemasUtils import schemasUtils
from app.websocket.repository.commandManager import getCommandManager

deviceType = "CUSTOM_DEVICE"


def getCustomDevices(currentUser: schemas.User, _deviceType: str, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    devices: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                          models.CustomDevice.deviceType == _deviceType).all()

    return devices


def getCustomDevice(db: Session, index: int, _deviceType: str, currentUser: schemas.User):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    device: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                         models.CustomDevice.deviceType == _deviceType,
                                                         models.CustomDevice.index == index).first()

    if not device:
        # TO Do create mock slot db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"CustomDevice with id {index} not found")
    else:
        return device


async def createCustomDevice(db: Session, request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User):
    xgrowKey = await userUtils.asyncGetXgrowKeyForCurrentUser(currentUser)
    userName = await userUtils.asyncGetUserNameForCurrentUser(currentUser)
    device: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                         models.CustomDevice.deviceType == deviceType,
                                                         models.CustomDevice.index == request.index)

    if device.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"CustomDevice for user {currentUser.name} with index {request.index} already exists")

    else:
        newCustomDevice = models.CustomDevice(xgrowKey=xgrowKey,
                                              index=request.index,
                                              deviceName=request.deviceName,
                                              deviceFunction=request.deviceFunction,
                                              working=request.working,
                                              reversal=request.reversal,
                                              active=request.active,
                                              deviceType=request.deviceType)

        db.add(newCustomDevice)
        db.commit()
        db.refresh(newCustomDevice)

        '''auto create timerTrigger'''
        request.timerTrigger.index = request.index
        request.timerTrigger.deviceType = request.deviceType
        timerTrigger.createTimerTrigger(request.timerTrigger, currentUser, db)

        request.airSensorTrigger.index = request.index
        request.airSensorTrigger.deviceType = request.deviceType
        airSensorTrigger.createAirSensorTrigger(request.airSensorTrigger, currentUser, db)

        if currentUser.userType:
            await getCommandManager().sendCommandToXgrow(command=f"/download customdevice {request.index}",
                                                         xgrowKey=xgrowKey,
                                                         userName=userName)
            # await getConnectionManagerXgrow().sendMessageToDevice(f"/download customdevice {request.index}", xgrowKey)
        else:
            await getCommandManager().sendCommandToFrontend(
                command=f"[Server] Xgrow was change customdevice {request.index}",
                xgrowKey=xgrowKey,
                userName=userName)
            # await getConnectionManagerFrontend().sendMessageToDevice(f"[Server] Xgrow was change customdevice {request.index}", userName)
        return newCustomDevice


async def updateCustomDevice(db: Session, request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User):
    xgrowKey = await userUtils.asyncGetXgrowKeyForCurrentUser(currentUser)
    userName = await userUtils.asyncGetUserNameForCurrentUser(currentUser)
    customDevice: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                               models.CustomDevice.deviceType == deviceType,
                                                               models.CustomDevice.index == request.index)

    if not customDevice.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"TimerTrigger with index {request.index} not found")
    else:
        customDevice.update(schemasUtils.filterUnableToSave(request.dict()))

        '''auto update timerTrigger'''
        request.timerTrigger.index = request.index
        request.timerTrigger.deviceType = request.deviceType
        timerTrigger.updateTimerTrigger(request.timerTrigger, currentUser, db)

        request.airSensorTrigger.index = request.index
        request.airSensorTrigger.deviceType = request.deviceType
        airSensorTrigger.updateAirSensorTrigger(request.airSensorTrigger, currentUser, db)

        db.commit()

        if currentUser.userType:
            await getCommandManager().sendCommandToXgrow(command=f"/download customdevice {request.index}",
                                                         xgrowKey=xgrowKey,
                                                         userName=userName)
            # await getConnectionManagerXgrow().sendMessageToDevice(f"/download customdevice {request.index}", xgrowKey)
        else:
            await getCommandManager().sendCommandToFrontend(
                command=f"[Server] Xgrow was change customdevice {request.index}",
                xgrowKey=xgrowKey,
                userName=userName)
            # await getConnectionManagerFrontend().sendMessageToDevice(f"[Server] Xgrow was change customdevice {request.index}", userName)
        return 'updated'
