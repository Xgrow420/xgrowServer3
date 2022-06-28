from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas, schemasPot
from fastapi import HTTPException, status
from app.websocket.routers.webSocketConnection import getConnectionManager

from app.utils.currentUserUtils import userUtils


def getPots(currentUser: schemas.User, db: Session):
    pots: Query = db.query(models.Pot).filter(models.Pot.xgrowKey == userUtils.getXgrowKeyForCurrentUser(currentUser)).all()
    return pots


def getPot(index: int, currentUser: schemas.User, db: Session):
    pot: Query = db.query(models.Pot).filter(models.Pot.xgrowKey == userUtils.getXgrowKeyForCurrentUser(currentUser),
                                      models.Pot.index == index).first()
    if not pot:
        # TO Do create mock fan db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"pot with id {index} not found")
    else:
        return pot


async def createPot(request: schemasPot.PotToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    pot: Query = db.query(models.Pot).filter(models.Pot.xgrowKey == xgrowKey,
                                      models.Pot.index == request.index)

    if not pot.first():
        newPot = models.Pot(xgrowKey=xgrowKey,
                            index=request.index,
                            active=request.active,
                            pumpWorkingTimeLimit=request.pumpWorkingTimeLimit,
                            autoWateringFunction=request.autoWateringFunction,
                            pumpWorkStatus=request.pumpWorkStatus,
                            # lastWateredCycleTime = datetime.now()
                            sensorOutput=request.sensorOutput,
                            minimalHumidity=request.minimalHumidity,
                            maxSensorHumidityOutput=request.maxSensorHumidityOutput,
                            minSensorHumidityOutput=request.minSensorHumidityOutput,
                            pumpWorkingTime=request.pumpWorkingTime,
                            wateringCycleTimeInHour=request.wateringCycleTimeInHour,
                            manualWateredInSecond=request.manualWateredInSecond
                            )
        db.add(newPot)
        db.commit()
        db.refresh(newPot)
        await getConnectionManager().sendMessageToDevice("Pobierz Pot", xgrowKey)
        return 'created'
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Pot for user {currentUser.name} with index {request.index} already exists!")


async def updatePot(request: schemasPot.PotToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    pot: Query = db.query(models.Pot).filter(models.Pot.xgrowKey == xgrowKey,
                                      models.Pot.index == request.index)

    if not pot.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Pot for user {currentUser.name} with index {request.index} not found")

    else:
        pot.update(request.dict())
        db.commit()
        await getConnectionManager().sendMessageToDevice("Pobierz Pot", xgrowKey)
        return 'updated'
