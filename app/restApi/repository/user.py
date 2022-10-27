
from sqlalchemy.orm import Session, Query
from app.data import models
from app.schemas import schemas, schemasXgrowKeys
from fastapi import HTTPException, status
from app.security.hashing import Hash




def createUser(request: schemas.User, db: Session):

    xgrowKey = db.query(models.XgrowKeys).filter(models.XgrowKeys.xgrowKey == request.xgrowKey).first()
    if xgrowKey:
        xgrowKey: schemasXgrowKeys.XgrowKey
        print(f"xgrow key is valid! {xgrowKey.ban}, {xgrowKey.reason}")

        db.query(models.User).filter(models.User.xgrowKey == request.xgrowKey).delete(synchronize_session=False)
        db.query(models.User).filter(models.User.name == request.xgrowKey).delete(synchronize_session=False)
        db.commit()


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

        return {"status": "registered"}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your device is not existed in Xgrow Data base, or you are banned...")


def getDeviceData(userSchema: schemas.User, db: Session):

    device: Query = db.query(models.User).filter(models.User.name == userSchema.xgrowKey).first()

    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {userSchema.name} do not have device! ERROR")
    return device

def getUser(current_user: schemas.User, db: Session):

    user: Query = db.query(models.User).filter(models.User.name == current_user.name).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found fatal ERROR")
    return user


def show(id: int, db: Session):
    user: Query = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user

