import os
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from dotenv import load_dotenv 
from src.auth.security import SecurityManager

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Авторизация"])

class LoginRequest(BaseModel):
    password: str

@router.post("/login")
async def login(data: LoginRequest):
    admin_hash = os.getenv("ADMIN_PASSWORD_HASH")
    
    if not admin_hash:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Бэкенд не видит .env файл или переменную ADMIN_PASSWORD_HASH!"
        )
    
    if not SecurityManager.verify_password(data.password, admin_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль автора!"
        )
    
    token = SecurityManager.create_access_token(data={"sub": "admin"})
    
    return {"access_token": token, "token_type": "bearer"}