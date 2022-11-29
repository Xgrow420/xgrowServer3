import ast

from enum import Enum

from fastapi import Query
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.utils.currentUserUtils import userUtils


from app.data import models


class DeviceFunction(Enum):
    TIMER = 1
    TEMPERATURE_MIN = 2
    TEMPERATURE_MAX = 3
    HUMIDITY_MIN = 4
    HUMIDITY_MAX = 5
    NULL = 6

def convertListToString(list: list):
    return str(list)

def convertStringToList(string: str):
    return ast.literal_eval(string)



def getUserSchemaFromName(userName, db: Session):
    user: schemas.User = db.query(models.User).filter(models.User.name == userName).first()
    return user

async def asyncGetUserSchemaFromName(userName, db: Session):

    user: schemas.User = db.query(models.User).filter(models.User.name == userName).first()
    return user

class deviceFunctionUtils():

    @staticmethod
    def convertStringToEnum(deviceFunction: str):

        if deviceFunction == DeviceFunction.TIMER.__str__():
            return DeviceFunction.TIMER

        if deviceFunction == DeviceFunction.TEMPERATURE_MAX.__str__():
            return DeviceFunction.TEMPERATURE_MAX

        if deviceFunction == DeviceFunction.TEMPERATURE_MIN.__str__():
            return DeviceFunction.TEMPERATURE_MIN

        if deviceFunction == DeviceFunction.HUMIDITY_MAX.__str__():
            return DeviceFunction.HUMIDITY_MAX

        if deviceFunction == DeviceFunction.HUMIDITY_MIN.__str__():
            return DeviceFunction.HUMIDITY_MIN

        if deviceFunction == DeviceFunction.NULL.__str__():
            return DeviceFunction.NULL

    @staticmethod
    def convertEnumToString(deviceFunction: DeviceFunction):
        return deviceFunction.__str__()
