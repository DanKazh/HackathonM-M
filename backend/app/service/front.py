from typing import List
from models.schemas import ObservationPoint, CloseApproachResponse
import uuid
from orbital_core.calculator.orbitDetermination import OrbitDetermination
from datetime import datetime
import numpy as np


class OrbitCalculationService:
    def __init__(self):
        # Инициализируем сервис определения орбиты
        self.orbit_determination = OrbitDetermination()
    
    async def calculate_min_distance(self, observations: List[ObservationPoint]) -> CloseApproachResponse:
        observations = [
    ('2025-10-25 17:50:00', 252.4714, 28.5345),
    ('2025-10-25 17:50:00', 244.1961, -45.8773),
    ('2025-10-25 17:50:00', 115.5531, -66.3296),
    ('2025-10-25 17:50:00', 321.6829, 34.9168),
    ('2025-10-25 17:50:00', 86.2134, 40.5738), ]
        try:
            # Преобразуем наблюдения в формат, ожидаемый OrbitDetermination
            for obs in observations:
                # Преобразуем RA из градусов в часы (1 час = 15 градусов)
                ra_hours = obs.ra_degrees / 15.0
                self.orbit_determination.add_observation(
                    obs.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    ra_hours,
                    obs.dec_degrees
                )
            
            # Вызываем расчет орбиты
            orbital_elements = self.orbit_determination.gauss_method_corrected()
            
            if orbital_elements is None:
                raise ValueError("Не удалось определить орбиту")
            
            # Рассчитываем минимальное расстояние и время сближения
            min_distance_result = self.orbit_determination.calculate_min_earth_distance(
                orbital_elements
            )
            
            return CloseApproachResponse(
                min_distance_km=min_distance_result['min_distance_km'],
                min_distance_au=min_distance_result['min_distance_au'],
                closest_approach_time=min_distance_result['closest_approach_time'],
                calculation_id=str(uuid.uuid4())
            )
            
        except Exception as e:
            raise ValueError(f"Ошибка при расчете орбиты: {str(e)}")
    
    def _simulate_external_calculation(self, observation_data):
        """
        Заглушка для обратной совместимости
        """
        # Для демонстрационных целей
        return {
            'min_distance_km': 1234567.89,
            'min_distance_au': 0.008256,
            'closest_approach_time': datetime.now()
        }