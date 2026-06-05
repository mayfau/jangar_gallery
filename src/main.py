import os
import sys
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel

from src.database import engine, Base
from src.paintings.models import PaintingModel 
from src.paintings.router import router as paintings_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Jangar Gallery", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#АВТОРИЗАЦИЯ

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "nelli")

class LoginRequest(BaseModel):
    password: str


@app.post("/auth/login")
async def login(data: LoginRequest):
    if data.password == ADMIN_PASSWORD:
        return {"access_token": "secret-art-token-2026", "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный секретный пароль!"
    )

app.include_router(paintings_router, prefix="/paintings", tags=["Paintings"])