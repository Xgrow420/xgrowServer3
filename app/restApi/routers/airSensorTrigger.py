
from fastapi import APIRouter, Depends, status
from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasCustomDevice
from sqlalchemy.orm import Session
from app.restApi.repository import airSensorTrigger

router = APIRouter(
    prefix="/api/airSensorTrigger",
    tags=['AirSensorTrigger']
)

dataBase = database.getDataBase


# @router.get('/', response_model=List[schemasCustomDevice.AirSensorTriggerToModify])
# def getAllAirSensorTrigger(current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
#     return airSensorTrigger.getAirSensorTriggers(current_user, db)
#
# @router.get('/{index}', response_model=schemasCustomDevice.AirSensorTriggerToModify)
# def getAirSensorTrigger(index: int, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
#     return airSensorTrigger.getAirSensorTrigger(index, current_user, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def createAirSensorTrigger(request: schemasCustomDevice.AirSensorTriggerToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return airSensorTrigger.createAirSensorTrigger(request, current_user, db)

@router.put('/', status_code=status.HTTP_201_CREATED)
def updateAirSensorTrigger(request: schemasCustomDevice.AirSensorTriggerToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return airSensorTrigger.updateAirSensorTrigger(request, current_user, db)