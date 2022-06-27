from app.schemas import schemas


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
