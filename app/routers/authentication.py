from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette import status

from app.data import models, database
from app.security.hashing import Hash

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.getDataBase),
          authorize: AuthJWT = Depends()):

    user = db.query(models.User).filter(models.User.name == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    # subject identifier for who this token is for example id or username from database
    access_token = authorize.create_access_token(subject=user.name, fresh=True)
    refresh_token = authorize.create_refresh_token(subject=user.name)

    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)

    return {"access_token": access_token, "token_type": "bearer"}
