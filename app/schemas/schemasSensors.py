from pydantic import BaseModel


class Sensors(BaseModel):

    xgrowKey: str
    #device Section
    airTemperature: str
    airHumidity: str
    potsMoistureList: str
    camera: str

    class Config():
        orm_mode = True


class SensorsToModify(BaseModel):

    airTemperature: str
    airHumidity: str
    potsMoistureList: str
    camera: str

    class Config():
        orm_mode = True
