from pydantic import BaseModel


class XgrowKey(BaseModel):

    xgrowKey: str
    #device Section
    ban: bool
    reason: str
    subscription: int

    class Config():
        orm_mode = True


class XgrowKeyToShow(BaseModel):

    #xgrowKey: str
    #device Section
    userName: str
    ban: bool
    reason: str
    subscription: int

    class Config():
        orm_mode = True