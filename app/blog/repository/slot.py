from sqlalchemy.orm import Session

from app.blog import models
from app.blog.schemas import schemas, schemasSlot
from fastapi import HTTPException, status

from app.blog.xgrow import XgrowInstance
from app.blog.xgrow.Climate import Climate


def getSlots(currentUser: schemas.User):

    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    schemasList = []
    for slot in xgrow.getSlotList():
        schemasList.append(slot.getObjectSchema())

    return schemasList


def getSlot(slotId: int, currentUser: schemas.User):

    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    return xgrow.getSlotList().__getitem__(slotId - 1).getObjectSchema()


def setSlotObject(request: schemasSlot.SlotToModify, currentUser: schemas.User):
    xgrow: Climate = XgrowInstance.getXgrowObject(currentUser)
    xgrow.getSlotList().__getitem__(request.slotId - 1).saveObjectFromSchema(request)

