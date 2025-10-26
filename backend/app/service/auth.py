from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
import re

from .jwt_handler import verify_password, get_password_hash, create_access_token
from app.database.models import User
from app.models.schemas import UserRegister, UserLogin

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def validate_username(self, username: str) -> bool:
        """Валидация имени пользователя"""
        if len(username) < 3:
            return False
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False
        return True

    def validate_password(self, password: str) -> bool:
        """Валидация пароля"""
        if len(password) < 6:
            return False
        return True

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Находит пользователя по имени"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Находит пользователя по email"""
        return self.db.query(User).filter(User.email == email).first()

    def register_user(self, user_data: UserRegister) -> User:
        """Регистрация нового пользователя"""
        # Валидация данных
        if not self.validate_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя пользователя должно содержать только буквы, цифры и подчеркивания, минимум 3 символа"
            )

        if not self.validate_password(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль должен содержать минимум 6 символов"
            )

        # Проверка существования пользователя
        if self.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем уже существует"
            )

        if self.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )

        # Создание пользователя
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def authenticate_user(self, user_data: UserLogin) -> Optional[User]:
        """Аутентификация пользователя"""
        user = self.get_user_by_username(user_data.username)
        if not user:
            return None
        
        if not verify_password(user_data.password, user.hashed_password):
            return None
        
        return user

    def login_user(self, user_data: UserLogin) -> dict:
        """Логин пользователя и создание токена"""
        user = self.authenticate_user(user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверное имя пользователя или пароль"
            )

        # Создание токена
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username
        }