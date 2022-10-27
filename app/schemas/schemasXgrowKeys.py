from pydantic import BaseModel


class XgrowKey(BaseModel):

    xgrowKey: str
    #device Section
    ban: bool
    reason: str
    abonament: int

    class Config():
        orm_mode = True