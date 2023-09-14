from pydantic import BaseModel


class Admin(BaseModel):

    AdminXgrowKey: str
    monitoredXgrowKey: str
    monitoredUser: str

    class Config():
        orm_mode = True
