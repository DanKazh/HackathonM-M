from fastapi import APIRouter, status
from typing import List
from models.schemas import ObservationRequest, CloseApproachResponse, ErrorResponse
from service.api_service import ApiService

router = APIRouter()
api_service = ApiService()

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