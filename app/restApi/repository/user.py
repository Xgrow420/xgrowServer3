from typing import List

from sqlalchemy.orm import Session, Query
from app.data import models
from app.schemas import schemas, schemasXgrowKeys
from fastapi import HTTPException, status
from app.security.hashing import Hash
from app.utils.currentUserUtils import userUtils


def createUser(request: schemas.User, db: Session):

    xgrowKey = db.query(models.XgrowKeys).filter(models.XgrowKeys.xgrowKey == request.xgrowKey).first()

    users: List[models.User] = db.query(models.User).filter(models.User.name == request.name).all()

    if users:
        if xgrowKey:
            for user in users:
                if user.xgrowKey != xgrowKey.xgrowKey:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail=f"This user name is already taken!")

    if xgrowKey:
        xgrowKey: schemasXgrowKeys.XgrowKey
        #print(f"xgrow key is valid! {xgrowKey.ban}, {xgrowKey.reason}")
        #TODO: Add if statments for ban and validate user account
        if xgrowKey.ban == True:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Your Xgrow was banned... Reason: {xgrowKey.reason}")

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


def getXgrowDevice(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    device = db.query(models.XgrowKeys).filter(models.XgrowKeys.xgrowKey == xgrowKey).first()
    if device:
        '''dokleja username do schema bo username nie jest trzymane w bazie danych'''
        device.userName = str(userUtils.getUserNameForCurrentUser(currentUser))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {currentUser.name} do not have device! ERROR")
    return device

#DEPRECATED
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

