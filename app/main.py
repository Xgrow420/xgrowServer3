import uvicorn
from fastapi import FastAPI
from app.blog import models
from app.blog.database import engine
from app.blog.routers import blog, user, authentication, pot, fan, air, customDevice
from app.blog.xgrow.XgrowInstance import XgrowInstance

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(pot.router)
app.include_router(fan.router)
app.include_router(air.router)
app.include_router(customDevice.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

