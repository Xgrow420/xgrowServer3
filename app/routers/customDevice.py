from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.data import database, models
from app.security import oauth2
from app import schemas
from app.schemas import schemas, schemasCustomDevice
from sqlalchemy.orm import Session
from app.repository import customDevice

router = APIRouter(
    prefix="/customDevice",
    tags=['CustomDevice']
)

dataBase = database.getDataBase


@router.get('/', response_model=List[schemasCustomDevice.CustomDeviceToModify])
def getAllDevicesForCurrentUser(current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return customDevice.getCustomDevices(current_user, db)

@router.get('/{deviceIndex}', response_model=schemasCustomDevice.CustomDeviceToModify)
def getDeviceForCurrentUser(deviceIndex: int, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return customDevice.getCustomDevice(db, deviceIndex, current_user)

@router.post('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemasCustomDevice.CustomDeviceToModify)
def setDeviceForCurrentUser(request: schemasCustomDevice.CustomDeviceToModify, current_user: schemas.User = Depends(
    oauth2.get_current_user), db: Session = Depends(dataBase)):
    return customDevice.createCustomDevice(db, request, current_user)

@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemasCustomDevice.CustomDeviceToModify)
def updateDeviceForCurrentUser(request: schemasCustomDevice.CustomDeviceToModify, current_user: schemas.User = Depends(
    oauth2.get_current_user), db: Session = Depends(dataBase)):
    return customDevice.updateCustomDevice(db, request, current_user)

