from sqlalchemy.orm import Session

from app.blog import models
from app.blog.schemas import schemas, schemasPot
from fastapi import HTTPException, status

from app.blog.xgrow import XgrowInstance
from app.blog.xgrow.Climate import Climate


def getPots(currentUser: schemas.User, db: Session):
    pots = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.xgrowKey).all()
    return pots


def getPot(index: int, currentUser: schemas.User, db: Session):
    pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.xgrowKey,
                                      models.Pot.index == index).first()
    if not pot:
        # TO Do create mock fan db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"pot with id {index} not found")
    else:
        return pot


def setPot(request: schemasPot.PotToModify, currentUser: schemas.User, db: Session):
    pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.xgrowKey,
                                      models.Pot.index == request.index)

    if not pot.first():
        newPot = models.Pot(xgrowKey=currentUser.xgrowKey,
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
        return 'created'

    else:
        pot.update(request.dict())
        db.commit()
        return 'updated'
