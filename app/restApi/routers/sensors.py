from typing import List
from fastapi import APIRouter, Depends, status
from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasSensors
from sqlalchemy.orm import Session
from app.restApi.repository import sensors

router = APIRouter(
    prefix="/sensors",
    tags=['Sensors']
)

dataBase = database.getDataBase


@router.get('/', response_model=List[schemasSensors.SensorsToModify])
def getSensors(current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return sensors.getSensors(current_user,db)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def createSensors(request: schemasSensors.SensorsToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return sensors.createSensors(request,current_user,db)

@router.put('/', status_code=status.HTTP_201_CREATED)
async def updateSensors(request: schemasSensors.SensorsToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return sensors.updateSensors(request, current_user, db)