from sqlalchemy.orm import Session

from app.blog import models
from app.blog.schemas import schemas, schemasCustomDevice
from fastapi import HTTPException, status

from app.blog.xgrow import XgrowInstance
from app.blog.xgrow.Climate import Climate


def getCustomDevices(currentUser: schemas.User, db: Session):
    # if currentUser.userType
    device = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == currentUser.xgrowKey).all()

    return device


def getCustomDevice(db: Session, index: int, currentUser: schemas.User):
    device = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == currentUser.xgrowKey,
                                                  models.CustomDevice.index == index)

    print(device.first())
    print(type(device))
    if not device.first():
        # TO Do create mock slot db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Slot with id {index} not found")
    else:
        return device


def setCustomDevice(db: Session, request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User):
    device = db.query(models.CustomDevice).filter(models.CustomDevice.xgrowKey == currentUser.xgrowKey,
                                                  models.CustomDevice.index == request.index)

    if not device.first():
        newCustomDevice = models.CustomDevice(xgrowKey=currentUser.xgrowKey,
                                              index=request.index,
                                              deviceFunction=request.deviceFunction,  # SlotFunction.TIMER  ENUM TO DO
                                              working=request.working,
                                              active=request.active
                                              )
        db.add(newCustomDevice)
        db.commit()
        db.refresh(newCustomDevice)
        return 'created'

    else:
        device.update(request.dict())
        db.commit()
        return 'updated'
