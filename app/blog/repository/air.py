from sqlalchemy.orm import Session

from app.blog.xgrow import XgrowInstance
from app.blog import models
from app.blog.schemas import schemas, schemasAir
from fastapi import HTTPException, status

from app.blog.xgrow.Climate import Climate


def getAir(currentUser: schemas.User, db: Session):
    air = db.query(models.Air).filter(models.Air.xgrowKey == currentUser.xgrowKey).first()
    return air


def setAir(request: schemasAir.AirToModify, currentUser: schemas.User, db: Session):
    air = db.query(models.Air).filter(models.Air.xgrowKey == currentUser.xgrowKey)

    if not air.first():
        newAir = models.Air(xgrowKey=currentUser.xgrowKey,
                            airTemperature=request.airTemperature,
                            airHumidity=request.airHumidity
                            )
        db.add(newAir)
        db.commit()
        db.refresh(newAir)
        return 'created'

    else:
        air.update(request.dict())
        db.commit()
        return 'updated'
