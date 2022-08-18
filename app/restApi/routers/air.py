from fastapi import APIRouter, Depends, status
from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasAir
from sqlalchemy.orm import Session
from app.restApi.repository import air

router = APIRouter(
    prefix="/api/air",
    tags=['Air']
)

dataBase = database.getDataBase


@router.get('/', response_model=schemasAir.AirToModify)
def get_air(current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return air.getAir(current_user, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_air(request: schemasAir.AirToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return await air.createAir(request, current_user, db)

@router.put('/', status_code=status.HTTP_202_ACCEPTED)
async def update_air(request: schemasAir.AirToModify, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    return await air.updateAir(request, current_user, db)
