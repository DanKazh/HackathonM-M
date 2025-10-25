from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.front import router as calculation_router

app = FastAPI(
    title="Comet Orbit Calculator API",
    description="API для расчета минимального расстояния комет до Земли",
    version="1.0.0"
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

@app.get("/")
async def root():
    return {"message": "Comet Orbit Calculator API"}

@app.get("/health")
async def health():
    return {"status": "ok"}