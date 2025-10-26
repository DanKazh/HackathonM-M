# routes/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os
import hashlib
import binascii

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """Проверяет пароль"""
    try:
        # hashed_password хранится как bytea hex строка (40 байт)
        # Конвертируем обратно в бинарный SHA1 для проверки
        hex_string = hashed_password.decode('utf-8')
        stored_hash = binascii.unhexlify(hex_string)  # 20 байт
        
        calculated_hash = hashlib.sha1(plain_password.encode()).digest()
        return calculated_hash == stored_hash
    except Exception:
        return False

def get_password_hash(password: str) -> bytes:
    """Создает SHA1 хеш пароля в hex формате (40 байт)"""
    # Создаем SHA1 хеш
    sha1_hash = hashlib.sha1(password.encode()).digest()  # 20 байт
    
    # Конвертируем в hex строку и затем в байты
    hex_hash = sha1_hash.hex()  # 40 символов
    return hex_hash.encode('utf-8')  # 40 байт

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создает JWT токен"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Проверяет и парсит JWT токен"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None