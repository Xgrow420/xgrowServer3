from typing import List

from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas, schemasPot

from app.utils.currentUserUtils import userUtils


async def getPots(currentUser: schemas.User, db: Session):
    pots: Query = db.query(models.Pot).filter(models.Pot.xgrowKey == userUtils.asyncGetXgrowKeyForCurrentUser(currentUser)).all()
    return pots

async def setPots(request: List[schemasPot.PotToModify], currentUser: schemas.User, db: Session):
    for pot in request:
        #FIXME: check if statment to filter create/update pot
        if await updatePot(pot, currentUser, db):
            print(f"Pot {pot.index} updated")
        else:
            await createPot(pot, currentUser, db)
            print(f"Pot {pot.index} created")

async def getPot(index: int, currentUser: schemas.User, db: Session):
    pot: Query = db.query(models.Pot).filter(models.Pot.xgrowKey == userUtils.asyncGetXgrowKeyForCurrentUser(currentUser),
                                      models.Pot.index == index).first()
    if not pot:
        print(f"pot with id {index} not found")
    else:
        return pot


async def createPot(request: schemasPot.PotToModify, currentUser: schemas.User, db: Session):
    pot: Query = db.query(models.Pot).filter(models.Pot.xgrowKey == userUtils.asyncGetXgrowKeyForCurrentUser(currentUser),
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
        return False
        #print(f"[!] Pot for user {currentUser.name} with index {request.index} already exists!")


async def updatePot(request: schemasPot.PotToModify, currentUser: schemas.User, db: Session):
    pot: Query = db.query(models.Pot).filter(models.Pot.xgrowKey == userUtils.asyncGetXgrowKeyForCurrentUser(currentUser),
                                      models.Pot.index == request.index)

    if not pot.first():
        return False
        #print(f"[!] Pot for user {currentUser.name} with index {request.index} not found")

    else:
        pot.update(request.dict())
        db.commit()
        return 'updated'
