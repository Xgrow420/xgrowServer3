import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.data import models
from app.data.postgresSQLconnection.connect_connector import connect_with_connector
from app.data.postgresSQLconnection.standard import standard_connect
from app.restApi.routers import customDevice, endpointUtils, pot, user, authentication, preferences, \
    airSensorTrigger, logs, sensors
from app.websocket.routers import webSocketConnection
from app.restApi.routers import timerTrigger, air, fan

HOST_LOCATION = '127.0.0.1'
PORT = 8000

app = FastAPI()

models.Base.metadata.create_all(connect_with_connector())
''' 
    for deploy plz use connect_with_connector() in 
    models.Base.metadata.create_all(),
    for localhost use: standard_connect()
'''
app.include_router(authentication.router)
app.include_router(preferences.router)
app.include_router(logs.router)
app.include_router(sensors.router)
app.include_router(user.router)
app.include_router(pot.router)
app.include_router(fan.router)
app.include_router(air.router)
app.include_router(customDevice.router)
app.include_router(timerTrigger.router)
app.include_router(endpointUtils.router)
app.include_router(webSocketConnection.router)
app.include_router(airSensorTrigger.router)


@app.get('/status')
def get_status():
    return 'chuj'

origins = ["http://localhost", "http://localhost:4200", "http://127.0.0.1:8000", "http://localhost:8000",
           "http://127.0.0.1:4200", "http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST_LOCATION, port=PORT)

