from app.schemas import schemasLogs
from sqlalchemy.orm import Session, Query

from app.data import models
from app.schemas import schemas
from fastapi import HTTPException, status

from app.utils.currentUserUtils import userUtils


def getLogs(currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    logs: Query = db.query(models.Logs).filter(models.Logs.xgrowKey == xgrowKey).first()
    return logs


def createLogs(request: schemasLogs.LogsToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    logs: Query = db.query(models.Logs).filter(models.Logs.xgrowKey == xgrowKey)

    if not logs.first():
        newLogs = models.Logs(
            xgrowKey=xgrowKey,
            airTemperatureLogList=request.airTemperatureLogList,
            airHumidityLogList=request.airHumidityLogList,
            timeLogList=request.timeLogList,
            pot1MoistureLogList=request.pot1MoistureLogList,
            pot2MoistureLogList=request.pot2MoistureLogList,
            pot3MoistureLogList=request.pot3MoistureLogList,
            pot4MoistureLogList=request.pot4MoistureLogList,
            pot5MoistureLogList=request.pot5MoistureLogList,
            pot6MoistureLogList=request.pot6MoistureLogList,
            pot7MoistureLogList=request.pot7MoistureLogList,
            pot8MoistureLogList=request.pot8MoistureLogList
        )
        db.add(newLogs)
        db.commit()
        db.refresh(newLogs)
        return newLogs
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Logs is already exists")


def updateLogs(request: schemasLogs.LogsToModify, currentUser: schemas.User, db: Session):
    xgrowKey = userUtils.getXgrowKeyForCurrentUser(currentUser)
    logs: Query = db.query(models.Logs).filter(models.Logs.xgrowKey == xgrowKey)

    if not logs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Logs not found")
    else:
        logs.update(request.dict())
        db.commit()
        return 'updated'
