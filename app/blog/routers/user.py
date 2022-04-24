from fastapi import APIRouter
from app.blog import database, oauth2
from app.blog.schemas import schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from app.blog.repository import user

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

@router.post('/getdevice', response_model=schemas.User)
def getDeviceData(db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.getDeviceData(current_user, db)
