from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.data import database, models
from app.security import oauth2
from app import schemas
from app.schemas import schemas, schemasFan
from sqlalchemy.orm import Session
from app.repository import fan

router = APIRouter(
    prefix="/fan",
    tags=['Fan']
)

dataBase = database.getDataBase


@router.get('/', response_model=List[schemasFan.FanToModify])
def getFans(currentUser: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return fan.getFans(currentUser, db)

@router.get('/{index}', response_model=schemasFan.FanToModify)
def getFan(index: int, currentUser: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return fan.getFan(index, currentUser, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def setFan(request: schemasFan.FanToModify, currentUser: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    fan.setFan(request, currentUser, db)

