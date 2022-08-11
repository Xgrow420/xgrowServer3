import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.data import models
from app.data.postgresSQLconnection.connect_connector import connect_with_connector
from app.data.postgresSQLconnection.standard import standard_connect
from app.restApi.routers import customDevice, endpointUtils, pot, user, authentication, preferences, \
    airSensorTrigger, logs, sensors
from app.restApi.routers import timerTrigger, air, fan
from app.websocket.repository.connectionManagerFrontend import ConnectionFrontend, getConnectionManagerFrontend
from app.websocket.repository.connectionManagerXgrow import getConnectionManagerXgrow, ConnectionXgrow
from app.websocket.routers import webSocketXgrow, webSocketFrontend

HOST_LOCATION = '127.0.0.1'
PORT = 8000

localHost = False


app = FastAPI()


#models.Base.metadata.create_all(standard_connect())
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
app.include_router(webSocketXgrow.router)
app.include_router(airSensorTrigger.router)
app.include_router(webSocketFrontend.router)


@app.get('/api/status')
async def get_status():
    count1 = 0
    count2 = 0
    xklist = []
    xklist2 = []

    for connection in getConnectionManagerXgrow().active_connections:
        count1 = count1+1
        connection: ConnectionXgrow
        xklist.append(connection.getXgrowKey())
        await getConnectionManagerXgrow().sendMessageToDevice(f"sendMessageToDevice: {connection.getXgrowKey()}", connection.getXgrowKey())

    for connection1 in getConnectionManagerFrontend().active_connections:
        count2 = count2+1
        connection1: ConnectionFrontend
        xklist2.append(connection1.getUserName())
        await getConnectionManagerFrontend().sendMessageToDevice(f"sendMessageToDevice: {connection1.getUserName()}", connection1.getUserName())

    return f'deviceCount: {count1}, XgrowList: {xklist} , userCount: {count2} UserList{xklist2}'

if __name__ == "__main__":
    uvicorn.run(app, host=HOST_LOCATION, port=PORT)


