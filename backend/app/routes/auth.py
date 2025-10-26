# auth.py
from fastapi import APIRouter, HTTPException, status, Response, Depends
from models.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from repo.database.database import PostgresDB 
from dependencies import get_database, get_current_user  
from routes.security import (  # Импортируем из security.py
    verify_password, 
    get_password_hash, 
    create_access_token,
    verify_token
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: PostgresDB = Depends(get_database)
):
    """Регистрация нового пользователя"""
    # Проверяем, существует ли пользователь
    existing_user = await db.fetchrow(
        "SELECT id FROM user_table WHERE login = $1", 
        user_data.username
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Хешируем пароль
    hashed_password = get_password_hash(user_data.password)
    
    # Создаем пользователя
    user_id = await db.fetchval(
        "INSERT INTO user_table (login, password_hash) VALUES ($1, $2) RETURNING id",
        user_data.username, hashed_password
    )
    
    return UserResponse(
        id=user_id,
        username=user_data.username
    )

@router.post("/login", response_model=UserResponse)
async def login(
    response: Response,
    user_data: UserLogin,
    db: PostgresDB = Depends(get_database)
):
    """Логин пользователя с установкой токена в куки"""
    # Находим пользователя
    user = await db.fetchrow(
        "SELECT id, login, password_hash FROM user_table WHERE login = $1",
        user_data.username
    )
    
    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Создаем токен
    access_token = create_access_token(
        data={"sub": user["login"], "user_id": str(user["id"])}
    )
    
    # Устанавливаем токен в HTTP-only куки
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=30 * 60,  # 30 минут
        secure=False,  # True в продакшене (HTTPS)
        samesite="strict"
    )
    
    return UserResponse(
        id=user["id"],  
        username=user["login"]  
    )

@router.post("/logout")
async def logout(response: Response):
    """Выход пользователя (удаление токена из куки)"""
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """Получение информации о текущем пользователе"""
    return UserResponse(
        id=current_user["user_id"],
        username=current_user["username"]
    )