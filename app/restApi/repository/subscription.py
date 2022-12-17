from datetime import datetime, timedelta

from sqlalchemy.orm import Session, Query
from app.data import models
from app.schemas import schemas, schemasXgrowKeys, schemasSubscriptionsKey
from fastapi import HTTPException, status
from app.utils.currentUserUtils import userUtils


def subscriptionKey(currentUser: schemas.User, key: str, db: Session):

    subscriptionKey: Query = db.query(models.SubscriptionKeys).filter(models.SubscriptionKeys.subscriptionKey == key).first()
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)

    if xgrowKey:
        userXgrowKeys: schemasXgrowKeys.XgrowKey = db.query(models.XgrowKeys).filter(models.XgrowKeys.xgrowKey == xgrowKey).first()
        if subscriptionKey:
            if userXgrowKeys:
                days = subscriptionKey.days
                if userXgrowKeys.subscription < datetime.timestamp(datetime.now()):
                    subscriptionTime = datetime.now()
                    subscriptionTime += timedelta(days=days)

                    userXgrowKeys.subscription = int(datetime.timestamp(subscriptionTime))

                else:
                    subscriptionTime = datetime.fromtimestamp(userXgrowKeys.subscription)
                    subscriptionTime += timedelta(days=days)

                    userXgrowKeys.subscription = int(datetime.timestamp(subscriptionTime))

                db.query(models.SubscriptionKeys).filter(models.SubscriptionKeys.subscriptionKey == key).delete(synchronize_session=False)
                db.commit()

                return {"subscriptionEndTimestamp": userXgrowKeys.subscription, "extendedDays": days}

            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Fatal Error user does not exist in xgrowKeys db plz contact with administration",
                                headers={"message": "Your subscription Key is not valid."})

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"popupMessages.invalidKey",
                                headers={"message": "popupMessages.invalidKey"})

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your device is not existed in Xgrow Data base")


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
