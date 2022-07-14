from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas, schemasSensors
from fastapi import HTTPException, status
from app.websocket.routers.webSocketConnection import getConnectionManager

from app.utils.currentUserUtils import userUtils


def getSensors(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)

    sensors: Query = db.query(models.Sensors).filter(models.Sensors.xgrowKey == xgrowKey).first()
    if not sensors:
        # TO Do create mock fan db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sensors not found")
    else:
        return sensors


async def createSensors(request: schemasSensors.SensorsToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)

    sensors: Query = db.query(models.Sensors).filter(models.Sensors.xgrowKey == xgrowKey)

    if not sensors.first():
        newSensors = models.Sensors(xgrowKey=xgrowKey,
                                    airTemperature=request.airTemperature,
                                    airHumidity=request.airHumidity,
                                    potsMoistureList=request.potsMoistureList,
                                    camera=request.camera
                                    )
        db.add(newSensors)
        db.commit()
        db.refresh(newSensors)

        return 'created'
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Sensors already exists!")


async def updateSensors(request: schemasSensors.SensorsToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)

    sensors: Query = db.query(models.Sensors).filter(models.Sensors.xgrowKey == xgrowKey)

    if not sensors.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Sensors not found")

    else:
        sensors.update(request.dict())
        db.commit()

        return 'updated'
