from typing import List
from fastapi import APIRouter, Depends, status
from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasLogs
from sqlalchemy.orm import Session
from app.restApi.repository import logs

router = APIRouter(
    prefix="/api/logs",
    tags=['Logs']
)

dataBase = database.getDataBase


@router.get('/', response_model=schemasLogs.LogsToModify)
def getSensors(current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return logs.getLogs(current_user,db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def createSensors(request: schemasLogs.LogsToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return logs.createLogs(request,current_user,db)

@router.put('/', status_code=status.HTTP_201_CREATED)
def updateSensors(request: schemasLogs.LogsToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return logs.updateLogs(request, current_user, db)