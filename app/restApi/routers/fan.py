from typing import List
from fastapi import APIRouter, Depends, status
from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasCustomDevice
from sqlalchemy.orm import Session
from app.restApi.repository import customDevice

router = APIRouter(
    prefix="/api/fan",
    tags=['Fan']
)

dataBase = database.getDataBase

deviceType = "FAN"

@router.get('/', response_model=List[schemasCustomDevice.CustomDeviceToModify])
def getFans(currentUser: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return customDevice.getCustomDevices(currentUser, deviceType, db)

@router.get('/{index}', response_model=schemasCustomDevice.CustomDeviceToModify)
def getFan(index: int, currentUser: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return customDevice.getCustomDevice(db, index, deviceType, currentUser)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def createFan(request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return await customDevice.createCustomDevice(db, request, currentUser)

@router.put('/', status_code=status.HTTP_201_CREATED)
async def updateFan(request: schemasCustomDevice.CustomDeviceToModify, currentUser: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return await customDevice.updateCustomDevice(db, request, currentUser)
