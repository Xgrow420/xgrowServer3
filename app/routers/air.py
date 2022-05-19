from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.data import database, models
from app.security import oauth2
from app import schemas
from app.schemas import schemas, schemasAir
from sqlalchemy.orm import Session
from app.repository import air

router = APIRouter(
    prefix="/air",
    tags=['Air']
)

dataBase = database.getDataBase


@router.get('/', response_model=schemasAir.AirToModify)
def get_air(current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return air.getAir(current_user, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_air(request: schemasAir.AirToModify, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return air.createAir(request, current_user, db)

@router.put('/', status_code=status.HTTP_202_ACCEPTED)
def update_air(request: schemasAir.AirToModify, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return air.updateAir(request, current_user, db)
