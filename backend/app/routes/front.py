from fastapi import APIRouter, status
from typing import List
from models.schemas import ObservationRequest, CloseApproachResponse, OrbitAnimationResponse, ErrorResponse
from service.api_service import ApiService

router = APIRouter()
api_service = ApiService()

@router.post(
    "/calculate-orbit",
    response_model=CloseApproachResponse,
    summary="Быстрый расчет орбитальных параметров",
    description="Принимает список наблюдений и возвращает орбитальные параметры без анимации",
    responses={
        400: {"model": ErrorResponse, "description": "Неверный формат данных или недостаточно наблюдений"},
        500: {"model": ErrorResponse, "description": "Ошибка расчета орбиты"}
    }
)
async def calculate_orbit(request: ObservationRequest):
    """
    Быстрый расчет орбитальных параметров (без анимации)
    """
    return await api_service.calculate_orbit(request)

@router.post(
    "/generate-animation",
    response_model=OrbitAnimationResponse,
    summary="Генерация анимации орбиты",
    description="Генерирует анимацию орбиты на основе рассчитанных орбитальных параметров",
    responses={
        400: {"model": ErrorResponse, "description": "Недостаточно данных для генерации анимации"},
        500: {"model": ErrorResponse, "description": "Ошибка генерации анимации"}
    }
)
async def generate_animation(request: dict):  # Принимаем словарь с данными орбиты
    """
    Генерация анимации орбиты на основе данных орбиты
    """
    return await api_service.generate_orbit_animation(request)

# Существующий эндпоинт для обратной совместимости
@router.post(
    "/calculate",
    response_model=CloseApproachResponse,
    summary="Рассчитать минимальное расстояние до Земли",
    description="Принимает список наблюдений и возвращает минимальное расстояние до Земли и время сближения",
    responses={
        400: {"model": ErrorResponse, "description": "Неверный формат данных"},
        500: {"model": ErrorResponse, "description": "Ошибка расчета"}
    }
)
async def calculate_min_distance(request: ObservationRequest):
    """
    Эндпоинт для расчета минимального расстояния до Земли
    """
    return await api_service.calculate_min_distance(request)