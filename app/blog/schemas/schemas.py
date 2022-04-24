from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str
    xgrowKey: str
    userType: str
    password: str

    class Config():
        orm_mode = True


class Device(User):
    class Config():
        orm_mode = True

class ShowDevice(BaseModel):
    name: str
    userType: str
    xgrowKey: str

class ShowUser(BaseModel):
    name: str
    userType: str
    xgrowKey: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: Optional[str] = None
