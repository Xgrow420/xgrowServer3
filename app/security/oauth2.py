from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.data.database import getDataBase

from app.data import models
from app.security import token
from app.schemas.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def getCurrentUser(data: str = Depends(oauth2_scheme), db: Session = Depends(getDataBase)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    tokenData: TokenData = token.verify_token(data, credentials_exception)

    user = getUserModelByName(tokenData.name, db)
    if user is None:
        raise credentials_exception
    return user

def getUserModelByName(username: str, db: Session):
    '''find user model in data by user name'''
    return db.query(models.User).filter(models.User.name == username).first()



