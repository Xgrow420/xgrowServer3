from typing import List
from fastapi import APIRouter, Depends, status
from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasPreferences
from sqlalchemy.orm import Session
from app.restApi.repository import preferences

router = APIRouter(
    prefix="/preferences",
    tags=['Preferences']
)

dataBase = database.getDataBase


@router.get('/', response_model=List[schemasPreferences.PreferencesToModify])
def getPreferences(current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return preferences.getPreferences(current_user,db)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def createPreferences(request: schemasPreferences.PreferencesToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return preferences.createPreferences(request,current_user,db)

@router.put('/', status_code=status.HTTP_201_CREATED)
async def updatePot(request: schemasPreferences.PreferencesToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return preferences.updatePreferences(request, current_user, db)