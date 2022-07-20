import uvicorn
from fastapi import FastAPI

from app.restApi.routers import customDevice, endpointUtils, pot, user, authentication, preferences, \
    airSensorTrigger, logs, sensors
from app.websocket.routers import webSocketConnection
from app.restApi.routers import timerTrigger, air, fan

HOST_LOCATION = '127.0.0.1'
PORT = 8000

app = FastAPI()

#models.Base.metadata.create_all(engine)

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


if __name__ == "__main__":
    uvicorn.run(app, host=HOST_LOCATION, port=PORT)

