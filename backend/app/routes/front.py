# routes/front.py
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from models.schemas import (
    ObservationRequest, 
    CloseApproachResponse, 
    ObservationPoint, 
    ErrorResponse,
    SaveCalculationRequest,
    CalculationResponse,
    UserCalculationsResponse,
    SavedCalculation,
    OrbitAnimationResponse
)
from service.front import OrbitCalculationService
from service.api_service import ApiService
from dependencies import get_current_user, get_database
from repo.database.database import PostgresDB
import uuid

router = APIRouter()
calculation_service = OrbitCalculationService()
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
    return await api_service.calculate_min_distance(request)

async def _validate_and_convert_observations(observation_lists: List[List]) -> List[ObservationPoint]:
    """
    Валидирует и преобразует список списков в список ObservationPoint
    """
    if not observation_lists:
        raise ValueError("Список наблюдений не может быть пустым")
    
    observations = []
    
    for i, obs_list in enumerate(observation_lists):
        if len(obs_list) != 3:
            raise ValueError(f"Наблюдение {i} должно содержать 3 элемента: timestamp, ra, dec")
        
        timestamp, ra, dec = obs_list
        
        # Создаем ObservationPoint (Pydantic сам выполнит валидацию)
        try:
            observation = ObservationPoint(
                timestamp=timestamp,
                ra_degrees=float(ra),
                dec_degrees=float(dec)
            )
            observations.append(observation)
        except Exception as e:
            raise ValueError(f"Неверный формат данных в наблюдении {i}: {str(e)}")
    
    # Проверяем, что есть хотя бы 3 наблюдения для расчета орбиты
    if len(observations) < 3:
        raise ValueError("Для расчета орбиты необходимо минимум 3 наблюдения")
    
    return observations