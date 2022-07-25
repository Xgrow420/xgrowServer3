from typing import List
from fastapi import APIRouter, Depends, status
from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasCustomDevice
from sqlalchemy.orm import Session
from app.restApi.repository import timerTrigger

router = APIRouter(
    prefix="/api/timerTrigger",
    tags=['TimerTrigger']
)

dataBase = database.getDataBase


@router.get('/', response_model=List[schemasCustomDevice.TimerTriggerToModify])
def getAllTimerTrigger(current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return timerTrigger.getTimerTriggers(current_user, db)

@router.get('/{index}', response_model=schemasCustomDevice.TimerTriggerToModify)
def getTimerTrigger(index: int, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return timerTrigger.getTimerTrigger(index, current_user, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def createTimerTrigger(request: schemasCustomDevice.TimerTriggerToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return timerTrigger.createTimerTrigger(request, current_user, db)

@router.put('/', status_code=status.HTTP_201_CREATED)
def updateTimerTrigger(request: schemasCustomDevice.TimerTriggerToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return timerTrigger.updateTimerTrigger(request, current_user, db)