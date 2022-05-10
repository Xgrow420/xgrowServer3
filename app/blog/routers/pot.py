from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.blog import schemas, database, models, oauth2
from app.blog.schemas import schemas, schemasPot
from sqlalchemy.orm import Session
from app.blog.repository import pot

router = APIRouter(
    prefix="/pot",
    tags=['Pot']
)

dataBase = database.getDataBase


@router.get('/', response_model=List[schemasPot.PotToModify])
def getAllPots(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pot.getPots(current_user)

@router.get('/{potId}', response_model=schemasPot.PotToModify)
def getPot(potId: int, current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pot.getPot(potId, current_user)

@router.post('/', response_model=schemasPot.PotToModify)
def setPotObject(request: schemasPot.PotToModify, current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pot.setPotObject(request, current_user)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pot.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasPot.PotToModify, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pot.updatePot(id, request, db, current_user)


@router.get('/{id}', status_code=200, response_model=schemasPot.Pot)
def show(id: int, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pot.getPot(id, db, current_user)
