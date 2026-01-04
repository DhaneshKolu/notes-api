from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import users,notes

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(notes.router)

