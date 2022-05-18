from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.data import database, models
from app.security import oauth2
from app import schemas
from app.schemas import schemas, schemasPot
from sqlalchemy.orm import Session
from app.repository import pot

router = APIRouter(
    prefix="/pot",
    tags=['Pot']
)

dataBase = database.getDataBase


@router.get('/', response_model=List[schemasPot.PotToModify])
def getAllPots(current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return pot.getPots(current_user, db)

@router.get('/{index}', response_model=schemasPot.PotToModify)
def getPot(index: int, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return pot.getPot(index, current_user, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def setPot(request: schemasPot.PotToModify, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return pot.setPot(request, current_user, db)
