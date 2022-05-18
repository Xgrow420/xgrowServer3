from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.blog import schemas, database, models, oauth2
from app.blog.schemas import schemas, schemasAir
from sqlalchemy.orm import Session
from app.blog.repository import air

router = APIRouter(
    prefix="/air",
    tags=['Air']
)

dataBase = database.getDataBase


@router.get('/', response_model=schemasAir.AirToModify)
def get_air(current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return air.getAir(current_user, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def set_air(request: schemasAir.AirToModify, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(dataBase)):
    return air.setAir(request, current_user, db)
