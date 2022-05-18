from sqlalchemy.orm import Session

from app.blog import models
from app.blog.schemas import schemas, schemasFan
from fastapi import HTTPException, status

from app.blog.xgrow.Climate import Climate
from app.blog.xgrow import XgrowInstance


def getFans(currentUser: schemas.User, db: Session):
    fans = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.xgrowKey).all()
    return fans


def getFan(index: int, currentUser: schemas.User, db: Session):
    fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.xgrowKey,
                                      models.Fan.index == index).first()
    if not fan:
        # TO Do create mock fan db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Slot with id {index} not found")
    else:
        return fan


def setFan(request: schemasFan.FanToModify, currentUser: schemas.User, db: Session):
    fan = db.query(models.Fan).filter(models.Fan.xgrowKey == currentUser.xgrowKey,
                                      models.Fan.index == request.index)

    if not fan.first():
        newFan = models.Fan(xgrowKey=currentUser.xgrowKey,
                            index=request.index,
                            active=request.active,
                            working=request.working,
                            normalMode=request.normalMode,
                            coldMode=request.coldMode,
                            hotMode=request.hotMode,
                            tempMax=request.tempMax,
                            tempMin=request.tempMin,
                            temperatureStatus=request.temperatureStatus
                            )
        db.add(newFan)
        db.commit()
        db.refresh(newFan)
        return 'created'

    else:
        fan.update(request.dict())
        db.commit()
        return 'updated'

