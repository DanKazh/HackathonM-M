# dependencies.py
from fastapi import Depends, HTTPException, status, Cookie
from typing import Optional
from routes.security import verify_token  # Импортируем из security.py
from repo.database.database import PostgresDB, db  

async def get_database() -> PostgresDB:
    return db

async def get_current_user(
    access_token: Optional[str] = Cookie(None),
    db: PostgresDB = Depends(get_database)
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = verify_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    username = payload.get("sub")
    user_id = payload.get("user_id")
    
    if not username or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Verify user exists in database
    user = await db.fetchrow(
        "SELECT id, login FROM user_table WHERE id = $1 AND login = $2",
        user_id, username
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return {
        "user_id": str(user["id"]),
        "username": user["login"]
    }