import uvicorn
from fastapi import FastAPI

from app.data import models
from app.data.database import engine
from app.restApi.routers import customDevice, endpointUtils, webSocketWithAuth, pot, user, authentication, blog
from app.websocket.routers import webSocketConnection
from app.restApi.routers import timerTrigger, air, fan

HOST_LOCATION = '127.0.0.1'
PORT = 8000

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(pot.router)
app.include_router(fan.router)
app.include_router(air.router)
app.include_router(customDevice.router)
app.include_router(timerTrigger.router)
app.include_router(endpointUtils.router)
app.include_router(webSocketConnection.router)
app.include_router(webSocketWithAuth.router)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST_LOCATION, port=PORT)

