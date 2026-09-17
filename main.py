from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import engine
import models
from routers import auth, books

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # ========= BOOT ===========
    models.Base.metadata.create_all(bind=engine) # importing the models made Base fill its metadata
    yield

    # ========= SHUTDOWN ===========

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(books.router)

@app.get("/")
def root():
    return {"message": "Hello, World!"}
