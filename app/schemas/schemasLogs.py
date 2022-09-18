from pydantic import BaseModel


class Logs(BaseModel):

    xgrowKey: str
    airTemperatureLogList: str
    airHumidityLogList: str
    events: str
    pot0MoistureLogList: str
    pot1MoistureLogList: str
    pot2MoistureLogList: str
    pot3MoistureLogList: str
    pot4MoistureLogList: str
    pot5MoistureLogList: str
    pot6MoistureLogList: str
    pot7MoistureLogList: str
    
    class Config():
        orm_mode = True

class LogsToModify(BaseModel):

    airTemperatureLogList: str
    airHumidityLogList: str
    events: str
    pot0MoistureLogList: str
    pot1MoistureLogList: str
    pot2MoistureLogList: str
    pot3MoistureLogList: str
    pot4MoistureLogList: str
    pot5MoistureLogList: str
    pot6MoistureLogList: str
    pot7MoistureLogList: str

    class Config():
        orm_mode = True
