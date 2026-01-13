from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import users,notes
from app.logging_config import setup_logging
from app.middleware import timing_middleware
setup_logging()

models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.middleware("http")(timing_middleware)

app.include_router(users.router)
app.include_router(notes.router)

