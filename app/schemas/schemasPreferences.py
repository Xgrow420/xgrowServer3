from pydantic import BaseModel


class Preferences(BaseModel):

    xgrowKey:str
    language: str
    temperatureFormat: str
    dateFormat: str

    class Config():
        orm_mode = True

class PreferencesToModify(BaseModel):
    language: str
    temperatureFormat: str
    dateFormat: str

    class Config():
        orm_mode = True

