from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.data import database
from app.repository import user
from app.schemas import schemas
from app.security import oauth2

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

dataBase = database.getDataBase


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(dataBase)):
    return user.createUser(request, db)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(dataBase)):
    return user.show(id, db)

@router.get('/device', response_model=schemas.User)
def getDeviceData(db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.getCurrentUser)):
    return user.getDeviceData(current_user, db)
