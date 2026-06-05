import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
import bcrypt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

class SecurityManager:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверяет, подходит ли введенный пароль к хэшу"""
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False

    @staticmethod
    def create_access_token(data: dict) -> str:
        """Создает электронный цифровой пропуск (JWT-токен)"""
        to_encode = data.copy()
        
        expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt