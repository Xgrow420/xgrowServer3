import uvicorn
from fastapi import FastAPI
from app.data import models
from app.data.database import engine
from app.routers import air, customDevice, timerTrigger, endpointUtils
from app.routers import fan, blog, authentication, user, pot

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

