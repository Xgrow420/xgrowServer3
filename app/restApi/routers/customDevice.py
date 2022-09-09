from typing import List
from fastapi import APIRouter, Depends, status
from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasCustomDevice
from sqlalchemy.orm import Session
from app.restApi.repository import customDevice

router = APIRouter(
    prefix="/api/customDevice",
    tags=['CustomDevice']
)

dataBase = database.getDataBase

deviceType = "CUSTOM_DEVICE"

@router.get('/', response_model=List[schemasCustomDevice.CustomDeviceToModify])
def getAllDevicesForCurrentUser(current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return customDevice.getCustomDevices(current_user, deviceType, db)

@router.get('/{deviceIndex}', response_model=schemasCustomDevice.CustomDeviceToModify)
def getDeviceForCurrentUser(deviceIndex: int, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return customDevice.getCustomDevice(db, deviceIndex, deviceType, current_user)

@router.post('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemasCustomDevice.CustomDeviceToModify)
async def setDeviceForCurrentUser(request: schemasCustomDevice.CustomDeviceToModify, current_user: schemas.User = Depends(
    oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return await customDevice.createCustomDevice(db, request, current_user)

@router.put('/', status_code=status.HTTP_202_ACCEPTED)
async def updateDeviceForCurrentUser(request: schemasCustomDevice.CustomDeviceToModify, current_user: schemas.User = Depends(
    oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return await customDevice.updateCustomDevice(db, request, current_user)

