from sqlalchemy.orm import Session, Query

from app.data import models
from app.restApi.repository import timerTrigger, airSensorTrigger
from app.schemas import schemas, schemasFan, schemasCustomDevice
from fastapi import HTTPException, status

from app.utils.currentUserUtils import userUtils
from app.utils.schemasUtils import schemasUtils
from app.websocket.repository.commandManager import getCommandManager

deviceType = "FAN"


def getFans(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    fans: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                       models.CustomDevice.deviceType == deviceType).all()
    return fans


def getFan(index: int, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    fan: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                      models.CustomDevice.deviceType == deviceType,
                                                      models.CustomDevice.index == index).first()

    if not fan:
        # TO Do create mock fan db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Slot with id {index} not found")
    else:
        return fan


async def createFan(request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User, db: Session):
    xgrowKey = await userUtils.asyncGetXgrowKeyForCurrentUser(currentUser)
    userName = await userUtils.asyncGetUserNameForCurrentUser(currentUser)
    customDevice: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                      models.CustomDevice.deviceType == deviceType,
                                                      models.CustomDevice.index == request.index)

    if not customDevice.first():
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
        # ==
        if currentUser.userType:
            await getCommandManager().sendCommandToXgrow(command=f"/download fan {request.index}",
                                                         xgrowKey=xgrowKey,
                                                         userName=userName)
            # await getConnectionManagerXgrow().sendMessageToDevice(f"/download fan {request.index}", xgrowKey)
        else:
            await getCommandManager().sendCommandToFrontend(command=f"[Server] Xgrow was change fan {request.index}",
                                                            xgrowKey=xgrowKey,
                                                            userName=userName)

            # await getConnectionManagerFrontend().sendMessageToDevice(f"[Server] Xgrow was change fan {request.index}", userName)

        return 'created'
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Fan for user {currentUser.name} with index: {request.index} is already exists")


async def updateFan(request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User, db: Session):
    xgrowKey = await userUtils.asyncGetXgrowKeyForCurrentUser(currentUser)
    userName = await userUtils.asyncGetUserNameForCurrentUser(currentUser)
    customDevice: Query = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == xgrowKey,
                                                      models.CustomDevice.deviceType == deviceType,
                                                      models.CustomDevice.index == request.index)

    if not customDevice.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Fan for user {currentUser.name} with index {request.index} not found")

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
            await getCommandManager().sendCommandToXgrow(command=f"/download fan {request.index}",
                                                         xgrowKey=xgrowKey,
                                                         userName=userName)
            # await getConnectionManagerXgrow().sendMessageToDevice(f"/download fan {request.index}", xgrowKey)
        else:
            await getCommandManager().sendCommandToFrontend(command=f"[Server] Xgrow was change fan {request.index}",
                                                            xgrowKey=xgrowKey,
                                                            userName=userName)
            # await getConnectionManagerFrontend().sendMessageToDevice(f"[Server] Xgrow was change pot {request.index}", userName)

        return 'updated'
