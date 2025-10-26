from typing import List
from fastapi import HTTPException, status
from models.schemas import ObservationRequest, CloseApproachResponse, ObservationPoint
from service.validation_service import ValidationService
from service.orbit_calculation_service import OrbitCalculationService

class ApiService:
    """Основной сервис для обработки API запросов"""
    
    def __init__(self):
        self.validation_service = ValidationService()
        self.orbit_calculation_service = OrbitCalculationService()
    
    async def calculate_min_distance(self, request: ObservationRequest) -> CloseApproachResponse:
        """
        Основной метод для расчета минимального расстояния
        """
        try:
            # Валидация и преобразование входных данных
            observations = await self.validation_service.validate_observation_request(request)
            
            # Вызов сервиса для расчета орбиты
            result = await self.orbit_calculation_service.calculate_min_distance(observations)
            
            return result
            
        except HTTPException:
            # Пробрасываем HTTPException дальше
            raise
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