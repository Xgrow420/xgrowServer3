from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasXgrowKeys
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.restApi.repository import user

router = APIRouter(
    prefix="/api/user",
    tags=['Users']
)

dataBase = database.getDataBase

#TODO: usunac showUser bo po co maja to widziec
@router.post('/')
def create_user(request: schemas.User, db: Session = Depends(dataBase)):
    return user.createUser(request, db)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(dataBase)):
    return user.show(id, db)

@router.get('/getdevice/', response_model=schemasXgrowKeys.XgrowKeyToShow)
def getDeviceData(db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.getCurrentUser)):
    return user.getXgrowDevice(current_user, db)
