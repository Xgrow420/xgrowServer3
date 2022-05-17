from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.blog import schemas, database, models, oauth2
from app.blog.schemas import schemas, schemasCustomDevice
from sqlalchemy.orm import Session
from app.blog.repository import slot

router = APIRouter(
    prefix="/slot",
    tags=['Slot']
)

dataBase = database.getDataBase




@router.get('/', response_model=List[schemasCustomDevice.CustomDeviceToModify])
def getAllSlots(current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return slot.getCustomDevices(current_user, db)

@router.get('/{deviceIndex}', response_model=schemasCustomDevice.CustomDeviceToModify)
def getSlot(deviceIndex: int, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return slot.getCustomDevice(db, deviceIndex, current_user)

@router.post('/', status_code=status.HTTP_202_ACCEPTED)
def setSlotObject(request: schemasCustomDevice.CustomDeviceToModify, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return slot.setCustomDevice(db, request, current_user)

