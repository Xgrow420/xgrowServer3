from starlette import status

from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasXgrowKeys
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.restApi.repository import subscription

router = APIRouter(
    prefix="/api/subscription",
    tags=['Subscription']
)

dataBase = database.getDataBase


@router.post('/{key}', status_code=status.HTTP_202_ACCEPTED)
def send_subscriptionKey(key: str, current_user: schemas.User = Depends(oauth2.getCurrentUser), db: Session = Depends(dataBase)):
    print("hit send_subscriptionKey endpoint!")
    return subscription.subscriptionKey(current_user, key, db)
