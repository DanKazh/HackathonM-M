from fastapi import APIRouter, Depends
from contextlib import asynccontextmanager


from repo.database import database as DB

# Создание экземпляра БД
db = DB.PostgresDB()

@asynccontextmanager
async def lifespan(app: APIRouter):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()

db_router = APIRouter(lifespan=lifespan)

# Dependency для инъекции в эндпоинты
async def get_database() -> DB.PostgresDB:
    return db

@db_router.get("/health")
async def health_check(db: DB.PostgresDB = Depends(get_database)):
    is_healthy = await db.health_check()
    return {"database_healthy": is_healthy}

@db_router.get("/users")
async def get_users(db: DB.PostgresDB = Depends(get_database)): # ИЗМЕНИТЬ ЗАПРОСЫ
    users = await db.fetch("SELECT id, name, email FROM users")
    return [dict(user) for user in users]

@db_router.get("/users/{user_id}")
async def get_user(user_id: int, db: DB.PostgresDB = Depends(get_database)): # ИЗМЕНИТЬ ЗАПРОСЫ
    user = await db.fetchrow(
        "SELECT id, name, email FROM users WHERE id = $1", 
        user_id
    )
    if user:
        return dict(user)
    return {"error": "User not found"}

@db_router.post("/users") 
async def create_user(
    name: str, 
    email: str, 
    db: DB.PostgresDB = Depends(get_database)
):
    user_id = await db.fetchval(
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id",
        name, email
    )
    return {"user_id": user_id, "message": "User created successfully"}