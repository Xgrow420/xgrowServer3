from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas, schemasAir
from fastapi import HTTPException, status

from app.utils.currentUserUtils import userUtils


def getAir(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    air: Query = db.query(models.Air).filter(models.Air.xgrowKey == xgrowKey).first()
    return air


def createAir(request: schemasAir.AirToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    air: Query = db.query(models.Air).filter(models.Air.xgrowKey == xgrowKey)

    if not air.first():
        newAir = models.Air(xgrowKey=currentUser.xgrowKey,
                            airTemperature=request.airTemperature,
                            airHumidity=request.airHumidity
                            )
        db.add(newAir)
        db.commit()
        db.refresh(newAir)
        return 'created'


def updateAir(request: schemasAir.AirToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    air: Query = db.query(models.Air).filter(models.Air.xgrowKey == xgrowKey)

    if not air.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"[!] Air for user {currentUser.name} not found")

    else:
        air.update(request.dict())
        db.commit()
        return 'updated'
