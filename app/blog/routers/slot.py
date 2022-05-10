from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.blog import schemas, database, models, oauth2
from app.blog.schemas import schemas, schemasSlot
from sqlalchemy.orm import Session
from app.blog.repository import slot

router = APIRouter(
    prefix="/slot",
    tags=['Slot']
)

dataBase = database.getDataBase




@router.get('/', response_model=schemasSlot.SlotToModify)
def getAllSlots(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return slot.getSlots(current_user)

@router.get('/{slotId}', response_model=schemasSlot.SlotToModify)
def getSlot(slotId: int, current_user: schemas.User = Depends(oauth2.get_current_user)):
    return slot.getSlot(slotId, current_user)

@router.post('/', response_model=schemasSlot.SlotToModify)
def setSlotObject(request: schemasSlot.SlotToModify, current_user: schemas.User = Depends(oauth2.get_current_user)):
    return slot.setSlotObject(request, current_user)

