from datetime import datetime

from app.data import models
from app.schemas import schemas, schemasXgrowKeys
from sqlalchemy.orm import Session, Query

class userUtils():

    @staticmethod
    def getXgrowKeyForCurrentUser(currentUser: schemas.User):
        '''Return XgrowKey by currentUser schema'''
        if currentUser.userType:
            return currentUser.xgrowKey
        else:
            return currentUser.name

    @staticmethod
    async def asyncGetXgrowKeyForCurrentUser(currentUser: schemas.User):
        '''Return XgrowKey by currentUser schema'''
        if currentUser.userType:
            return currentUser.xgrowKey
        else:
            return currentUser.name

    @staticmethod
    async def getAsyncUserNameForCurrentUser(currentUser: schemas.User):
        '''Return userName by currentUser schema'''
        if currentUser.userType:
            return currentUser.name
        else:
            return currentUser.xgrowKey

    @staticmethod
    def getUserNameForCurrentUser(currentUser: schemas.User):
        '''Return userName by currentUser schema'''
        if currentUser.userType:
            return currentUser.name
        else:
            return currentUser.xgrowKey

    @staticmethod
    async def asyncGetUserNameForCurrentUser(currentUser: schemas.User):
        '''Return userName by currentUser schema'''
        if currentUser.userType:
            return currentUser.name
        else:
            return currentUser.xgrowKey

    @staticmethod
    async def asyncUserHaveSubscription(xgrowKey, db : Session):
        userXgrowKeys: schemasXgrowKeys.XgrowKey = db.query(models.XgrowKeys).filter(models.XgrowKeys.xgrowKey == xgrowKey).first()
        if userXgrowKeys.subscription < datetime.timestamp(datetime.now()):
            return False
        else:
            return True

    @staticmethod
    def userHaveSubscription(xgrowKey, db : Session):
        userXgrowKeys: schemasXgrowKeys.XgrowKey = db.query(models.XgrowKeys).filter(models.XgrowKeys.xgrowKey == xgrowKey).first()
        if userXgrowKeys.subscription < datetime.timestamp(datetime.now()):
            return False
        else:
            return True
