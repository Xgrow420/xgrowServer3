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
def getAirObject(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return air.getAirObject(current_user)

@router.post('/', status_code=status.HTTP_201_CREATED)
def setAirObject(request: schemasAir.AirToModify, currentUser: schemas.User = Depends(oauth2.get_current_user)):
    air.setAirObject(request, currentUser)

#@router.post('/{potId}', status_code=status.HTTP_201_CREATED,)
#def create(potId: int, request: schemasPot.PotToModify, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
#    return air.createPot(potId, request, db, current_user)


#@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
#def destroy(id: int, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
#    return air.destroy(id, db)


#@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
#def update(id: int, request: schemasPot.PotToModify, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
#    return air.updatePot(id, request, db, current_user)


#@router.get('/{id}', status_code=200, response_model=schemasPot.Pot)
#def show(id: int, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
#    return air.getPot(id, db, current_user)
