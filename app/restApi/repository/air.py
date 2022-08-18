from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas, schemasAir
from fastapi import HTTPException, status

from app.utils.currentUserUtils import userUtils
from app.websocket.repository.connectionManagerXgrow import getConnectionManagerXgrow


def getAir(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    air: Query = db.query(models.Air).filter(models.Air.xgrowKey == xgrowKey).first()
    return air


async def createAir(request: schemasAir.AirToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
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
            await getConnectionManagerXgrow().sendMessageToDevice(f"/download air", xgrowKey)
        return 'created'


async def updateAir(request: schemasAir.AirToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    air: Query = db.query(models.Air).filter(models.Air.xgrowKey == xgrowKey)

    if not air.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Air for user {currentUser.name} not found")

    else:
        air.update(request.dict())
        db.commit()
        if currentUser.userType:
            await getConnectionManagerXgrow().sendMessageToDevice(f"/download air", xgrowKey)
        return 'updated'
