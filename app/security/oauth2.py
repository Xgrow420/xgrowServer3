from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.data.database import getDataBase
from fastapi_jwt_auth import AuthJWT

from app.data import models

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def getCurrentUser(db: Session = Depends(getDataBase),
                   authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        user_name = authorize.get_jwt_subject()
        user = getUserModelByName(user_name, db)
    except:
        raise credentials_exception
    return user


def getUserModelByName(username: str, db: Session):
    '''find user model in data by user name'''
    return db.query(models.User).filter(models.User.name == username).first()
