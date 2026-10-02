from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from database import Base, engine
import db_models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router)