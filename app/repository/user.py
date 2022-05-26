
from sqlalchemy.orm import Session, Query
from app.data import models
from app import schemas
from app.schemas import schemas
from fastapi import HTTPException, status
from app.security.hashing import Hash


def createUser(request: schemas.User, db: Session):
    user: Query = db.query(models.User).filter(models.User.xgrowKey == request.xgrowKey)
    if not user.first():

        #====== Device profile
        new_device = models.User(
            name=request.xgrowKey, xgrowKey=request.name, password=Hash.bcrypt(request.password), userType=False)
        db.add(new_device)
        db.commit()
        db.refresh(new_device)


        # ====== User profile
        new_user = models.User(
            name=request.name, xgrowKey=request.xgrowKey, password=Hash.bcrypt(request.password), userType=True)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

def getDeviceData(userSchema: schemas.User, db: Session):

    device: Query = db.query(models.User).filter(models.User.name == userSchema.xgrowKey).first()

    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {userSchema.name} do not have device! ERROR")
    return device



def show(id: int, db: Session):
    user: Query = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user

