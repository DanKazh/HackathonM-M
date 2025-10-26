# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.front import router as calculation_router
from routes.database_router import db_router
from routes.auth import router as auth_router
from routes.database_router import db
from contextlib import asynccontextmanager
import asyncio  # Добавьте этот импорт

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    
    # Ждем пока база данных будет готова
    max_retries = 10
    for i in range(max_retries):
        try:
            is_healthy = await db.health_check()
            if is_healthy:
                print("Database connection established successfully")
                break
            else:
                print(f"Database not ready yet, retrying... ({i+1}/{max_retries})")
                await asyncio.sleep(2)
        except Exception as e:
            print(f"Connection attempt {i+1} failed: {e}")
            await asyncio.sleep(2)
    else:
        print("Failed to connect to database after multiple attempts")
    
    yield
    # Shutdown
    await db.disconnect()

app = FastAPI(
    title="Comet Orbit Calculator API",
    description="API для расчета минимального расстояния комет до Земли",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(calculation_router, prefix="/api", tags=["calculations"])
app.include_router(db_router, prefix="/db", tags=["database"])
app.include_router(auth_router, tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Comet Orbit Calculator API"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# Простая тестовая ручка
@app.get("/api/results")
async def get_results():
    return {
        "summary": {
            "total_observation_sets": 0,
            "total_observations": 0,
            "total_orbit_calculations": 0,
            "total_close_approaches": 0
        },
        "observation_sets": []
    }

@app.get("/api/results/set/{set_id}")
async def get_results_for_set(set_id: int):
    return {
        "id": set_id,
        "name": "Тестовый набор",
        "description": "Тестовое описание",
        "created_at": "2024-01-15T20:35:00",
        "observation_count": 5,
        "status": "calculated"
    }