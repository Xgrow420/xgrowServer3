from sqlalchemy.orm import Session

from app.blog.xgrow import XgrowInstance
from app.blog import models
from app.blog.schemas import schemas, schemasAir
from fastapi import HTTPException, status

from app.blog.xgrow.Climate import Climate


def getAirObject(currentUser: schemas.User):

    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    schema: schemasAir = xgrow.getAir().getObjectSchema()
    return schema

def setAirObject(request: schemasAir.AirToModify, currentUser: schemas.User):

    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    xgrow.getAir().saveObjectFromSchema(request)


# to do
def updateDB(db: Session, currentUser: schemas.User):

    #checking currentUser is Device or User:
    if currentUser.userType:
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.xgrowKey, models.Pot.potID == potId)
    else:
        pot = db.query(models.Pot).filter(models.Pot.xgrowKey == currentUser.name, models.Pot.potID == potId)

    if not pot.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pot with id {potId} not found")

    pot.update(request.dict())
    db.commit()
    return 'updated'
