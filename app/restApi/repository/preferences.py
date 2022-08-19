
from app.schemas import schemasPreferences
from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas
from fastapi import HTTPException, status

from app.utils.currentUserUtils import userUtils
from app.websocket.repository.connectionManagerFrontend import getConnectionManagerFrontend
from app.websocket.repository.connectionManagerXgrow import getConnectionManagerXgrow


def getPreferences(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    preferences: Query = db.query(models.Preferences).filter(models.Preferences.xgrowKey == xgrowKey).first()
    return preferences


async def createPreferences(request: schemasPreferences.PreferencesToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    preferences: Query = db.query(models.Preferences).filter(models.Preferences.xgrowKey == xgrowKey)

    if not preferences.first():
            newPreferences = models.Preferences(
                xgrowKey=xgrowKey,
                language=request.language,
                temperatureFormat=request.temperatureFormat,
                dateFormat=request.dateFormat,
            )
            db.add(newPreferences)
            db.commit()
            db.refresh(newPreferences)
            if currentUser.userType:
                await getConnectionManagerXgrow().sendMessageToDevice(f"/download preferences", xgrowKey)
            else:
                userName = userUtils.asyncGetUserNameForCurrentUser(currentUser)
                await getConnectionManagerFrontend().sendMessageToDevice(f"[Server] Xgrow was change preferences", userName)

            return newPreferences
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Preferences is already exists")



async def updatePreferences(request: schemasPreferences.PreferencesToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    preferences: Query = db.query(models.Preferences).filter(models.Preferences.xgrowKey == xgrowKey)

    if not preferences.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Preferences not found")
    else:
        preferences.update(request.dict())
        db.commit()
        if currentUser.userType:
            await getConnectionManagerXgrow().sendMessageToDevice(f"/download preferences", xgrowKey)
        else:
            userName = userUtils.asyncGetUserNameForCurrentUser(currentUser)
            await getConnectionManagerFrontend().sendMessageToDevice(f"[Server] Xgrow was change preferences", userName)

        return 'updated'


