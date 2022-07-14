
from app.schemas import schemasPreferences
from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas
from fastapi import HTTPException, status



def getPreferences(currentUser: schemas.User, db: Session):
    preferences: Query = db.query(models.Preferences).filter(models.Preferences.xgrowKey == currentUser.xgrowKey).first()
    return preferences


def createPreferences(request: schemasPreferences.PreferencesToModify, currentUser: schemas.User, db: Session):
    preferences: Query = db.query(models.Preferences).filter(models.Preferences.xgrowKey == currentUser.xgrowKey)

    if not preferences.first():
            newPreferences = models.Preferences(
                xgrowKey=currentUser.xgrowKey,
                language=request.language,
                temperatureFormat=request.temperatureFormat,
                dateFormat=request.dateFormat,
            )
            db.add(newPreferences)
            db.commit()
            db.refresh(newPreferences)
            return newPreferences
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Preferences is already exists")



def updatePreferences(request: schemasPreferences.PreferencesToModify, currentUser: schemas.User, db: Session):
    preferences: Query = db.query(models.Preferences).filter(models.Preferences.xgrowKey == currentUser.xgrowKey)

    if not preferences.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Preferences not found")
    else:
        preferences.update(request.dict())
        db.commit()
        return 'updated'


