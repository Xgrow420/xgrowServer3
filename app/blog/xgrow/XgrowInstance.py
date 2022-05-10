from app.blog.schemas import schemas
from app.blog.xgrow.Climate import Climate


'''TO DO singleton'''

class XgrowInstance():
    def __init__(self):

        self.xgrowObjects = []

    def createXgrowObject(self, currentUser: schemas.User):
        self.xgrowObjects.append(Climate(currentUser, 8, 4, 6))

    def getXgrowObjectsList(self):
        return self.xgrowObjects

    def deleteXgrowObject(self, currentUser: schemas.User):
        for object in self.xgrowObjects:
            if object.xgrowKey == currentUser.xgrowKey:
                self.xgrowObjects.remove(object)

    def getXgrowObject(self, currentUser: schemas.User):
        for object in self.xgrowObjects:
            object: Climate
            if object.xgrowKey == currentUser.xgrowKey:
                return object
            else:
                self.createXgrowObject(currentUser)
                return self.getXgrowObject(currentUser)
        else:
            self.createXgrowObject(currentUser)
            return self.getXgrowObject(currentUser)

xgrowInstnce = XgrowInstance()

def getXgrowObject(currentUser: schemas.User):
    return xgrowInstnce.getXgrowObject(currentUser)


