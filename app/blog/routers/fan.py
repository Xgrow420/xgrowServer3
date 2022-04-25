from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.blog import schemas, database, models, oauth2
from app.blog.schemas import schemas, schemasFan
from sqlalchemy.orm import Session
from app.blog.repository import fan

router = APIRouter(
    prefix="/fan",
    tags=['Fan']
)

dataBase = database.getDataBase


@router.get('/', response_model=List[schemasFan.Fan])
def all(db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return fan.getFans(db, current_user)


@router.post('/{fanId}', status_code=status.HTTP_201_CREATED,)
def create(fanId: int, request: schemasFan.FanToModify, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return fan.createFan(fanId, request, db, current_user)


@router.delete('/{fanId}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return fan.destroy(id, db)


@router.put('/{fanId}', status_code=status.HTTP_202_ACCEPTED)
def update(fanId: int, request: schemasFan.FanToModify, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return fan.updateFan(fanId, request, db, current_user)


@router.get('/{fanId}', status_code=200, response_model=schemasFan.Fan)
def show(fanId: int, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return fan.getFan(fanId, db, current_user)
