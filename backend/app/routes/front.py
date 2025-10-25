from fastapi import APIRouter, HTTPException, status
from typing import List
from models.schemas import ObservationRequest, CloseApproachResponse, ObservationPoint, ErrorResponse
from service.front import OrbitCalculationService

router = APIRouter()
calculation_service = OrbitCalculationService()

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
    try:
        # Валидация и преобразование входных данных
        observations = await _validate_and_convert_observations(request.observations)
        
        # Вызов сервиса для расчета
        result = await calculation_service.calculate_min_distance(observations)
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )

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