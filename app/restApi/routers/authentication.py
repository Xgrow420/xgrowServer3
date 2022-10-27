from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT

from app.data import database, models
from app.security import token
from app.security.hashing import Hash
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/api",
    tags=['Authentication']
)



@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.getDataBase), Authorize: AuthJWT = Depends()):
    user = db.query(models.User).filter(models.User.name == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.name})
    accessWebSocketToken = Authorize.create_access_token(subject=user.name, fresh=True, expires_time=False)
    refreshWebSocketToken = Authorize.create_refresh_token(subject=user.name)

    Authorize.set_access_cookies(accessWebSocketToken)
    Authorize.set_refresh_cookies(refreshWebSocketToken)

    return {"access_token": access_token, "token_type": "bearer"}
