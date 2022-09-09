
from pydantic import BaseModel



class Fan(BaseModel):

    xgrowKey: str
    index: int
    fanName: str
    active: bool
    working: bool
    tempMax: int
    tempMin: int

    class Config():
        orm_mode = True

class FanToModify(BaseModel):

    index: int
    fanName: str
    active: bool
    working: bool
    tempMax: int
    tempMin: int

    class Config():
        orm_mode = True
