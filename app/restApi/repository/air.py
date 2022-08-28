from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas, schemasAir
from fastapi import HTTPException, status

from app.utils.currentUserUtils import userUtils
from app.websocket.repository.commandManager import getCommandManager
from app.websocket.repository.connectionManagerFrontend import getConnectionManagerFrontend
from app.websocket.repository.connectionManagerXgrow import getConnectionManagerXgrow


def getAir(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    air: Query = db.query(models.Air).filter(models.Air.xgrowKey == xgrowKey).first()
    return air


async def createAir(request: schemasAir.AirToModify, currentUser: schemas.User, db: Session):
    xgrowKey = await userUtils.asyncGetXgrowKeyForCurrentUser(currentUser)
    userName = await userUtils.asyncGetUserNameForCurrentUser(currentUser)
    air: Query = db.query(models.Air).filter(models.Air.xgrowKey == xgrowKey)

    if not air.first():
        newAir = models.Air(xgrowKey=xgrowKey,
                            airTemperature=request.airTemperature,
                            airHumidity=request.airHumidity
                            )
        db.add(newAir)
        db.commit()
        db.refresh(newAir)
        if currentUser.userType:
            await getCommandManager().sendCommandToXgrow(command=f"/download air", xgrowKey=xgrowKey,
                                                         userName=userName)
            # await getConnectionManagerXgrow().sendMessageToDevice(f"/download air", xgrowKey)
        else:
            await getCommandManager().sendCommandToFrontend(command=f"[Server] Xgrow was change air", xgrowKey=xgrowKey,
                                                            userName=userName)
            # await getConnectionManagerFrontend().sendMessageToDevice(f"[Server] Xgrow was change air", userName)
        return 'created'


async def updateAir(request: schemasAir.AirToModify, currentUser: schemas.User, db: Session):
    xgrowKey = await userUtils.asyncGetXgrowKeyForCurrentUser(currentUser)
    userName = await userUtils.asyncGetUserNameForCurrentUser(currentUser)
    air: Query = db.query(models.Air).filter(models.Air.xgrowKey == xgrowKey)

    if not air.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Air for user {currentUser.name} not found")

    else:
        air.update(request.dict())
        db.commit()
        if currentUser.userType:
            await getCommandManager().sendCommandToXgrow(command=f"/download air",
                                                         xgrowKey=xgrowKey,
                                                         userName=userName)
            # await getConnectionManagerXgrow().sendMessageToDevice(f"/download air", xgrowKey)
        else:
            await getCommandManager().sendCommandToFrontend(command=f"[Server] Xgrow was change air",
                                                            xgrowKey=xgrowKey,
                                                            userName=userName)
            # await getConnectionManagerFrontend().sendMessageToDevice(f"[Server] Xgrow was change air", userName)
        return 'updated'
