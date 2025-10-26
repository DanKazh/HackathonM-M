from typing import List
from fastapi import HTTPException, status
from models.schemas import ObservationPoint, ObservationRequest
from datetime import datetime

class ValidationService:
    """Сервис для валидации и преобразования входных данных"""
    
    def __init__(self):
        pass
    
    async def validate_observation_request(self, request: ObservationRequest) -> List[ObservationPoint]:
        """
        Валидирует и преобразует ObservationRequest в список ObservationPoint
        """
        if not request.observations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Список наблюдений не может быть пустым"
            )
        
        return await self._convert_to_observation_points(request.observations)
    
    async def _convert_to_observation_points(self, observation_lists: List[List]) -> List[ObservationPoint]:
        """
        Преобразует список списков в список ObservationPoint
        """
        observations = []
        
        for i, obs_list in enumerate(observation_lists):
            if len(obs_list) != 3:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Наблюдение {i} должно содержать 3 элемента: timestamp, ra, dec"
                )
            
            timestamp, ra, dec = obs_list
            
            try:
                # Преобразуем timestamp в datetime
                if isinstance(timestamp, str):
                    # Парсим строку в datetime
                    observation_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    # Если это число (timestamp), конвертируем в datetime
                    observation_timestamp = datetime.fromtimestamp(float(timestamp))
                
                observation = ObservationPoint(
                    timestamp=observation_timestamp,
                    ra_degrees=float(ra),
                    dec_degrees=float(dec)
                )
                observations.append(observation)
                
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Неверный формат данных в наблюдении {i}: {str(e)}"
                )
        
        # Проверяем минимальное количество наблюдений
        if len(observations) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Для расчета орбиты необходимо минимум 3 наблюдения"
            )
        
        return observations