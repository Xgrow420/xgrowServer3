from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.blog import schemas, database, models, token
from app.blog.hashing import Hash
from sqlalchemy.orm import Session

from app.blog.xgrow import XgrowInstance

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.getDataBase)):
    user = db.query(models.User).filter(models.User.name == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}
