from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import getDataBase

from app.blog import token, models
from app.blog.schemas.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def get_current_user(data: str = Depends(oauth2_scheme), db: Session = Depends(getDataBase)):
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
    '''find user model in database by user name'''
    return db.query(models.User).filter(models.User.name == username).first()



