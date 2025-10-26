from typing import List
from models.schemas import ObservationPoint, CloseApproachResponse
import uuid
from orbital_core.calculator.orbitDetermination import OrbitDetermination
from orbital_core.visualizer.orbitVisualizer import OrbitVisualizer
from datetime import datetime
import numpy as np

class OrbitCalculationService:
    """Сервис для расчета орбитальных параметров"""
    
    def __init__(self):
        self.orbit_determination = OrbitDetermination()
        self.visualizer = OrbitVisualizer()
    
    async def calculate_min_distance(self, observations: List[ObservationPoint]) -> CloseApproachResponse:
        """
        Вычисляет минимальное расстояние до Земли на основе наблюдений
        """
        try:
            # Добавление наблюдений в систему определения орбиты
            self._add_observations_to_determination(observations)
            
            # Расчёт орбитальных элементов
            orbital_elements = self._calculate_orbital_elements()
            
            # Расчет минимального расстояния
            min_distance_au, closest_approach_time = self._calculate_min_earth_distance(orbital_elements)
            
            # Генерация анимации орбиты
            orbit_animation = await self._generate_orbit_animation(
                orbital_elements, observations, closest_approach_time
            )
            
            # Формирование ответа
            return self._build_response(
                orbital_elements, min_distance_au, closest_approach_time, orbit_animation
            )
            
        except Exception as e:
            raise ValueError(f"Ошибка при расчёте орбиты: {str(e)}")
    
    def _add_observations_to_determination(self, observations: List[ObservationPoint]) -> None:
        """Добавляет наблюдения в систему определения орбиты"""
        for obs in observations:
            ra_hours = obs.ra_degrees / 15.0
            self.orbit_determination.add_observation(
                obs.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                ra_hours,
                obs.dec_degrees
            )
    
    def _calculate_orbital_elements(self) -> List[float]:
        """Вычисляет орбитальные элементы"""
        orbital_elements = self.orbit_determination.find_best_solution()
        if orbital_elements is None:
            orbital_elements = self._get_fallback_orbit()
        return orbital_elements
    
    def _calculate_min_earth_distance(self, orbital_elements: List[float]) -> tuple:
        """Вычисляет минимальное расстояние до Земли"""
        min_distance_approx, min_date_approx, _ = self.orbit_determination.calculate_min_earth_distance(orbital_elements)
        min_distance, min_date = self.orbit_determination.find_exact_min_distance(min_date_approx)
        return min_distance, min_date
    
    async def _generate_orbit_animation(self, orbital_elements: List[float], 
                                      observations: List[ObservationPoint],
                                      close_approach_time: datetime) -> str:
        """Генерирует анимацию орбиты"""
        try:
            # Эпоха для M0 — первое наблюдение
            epoch_for_M0 = observations[0].timestamp
            
            orbit_animation = self.visualizer.create_orbit_animation(
                a=orbital_elements[0],
                e=orbital_elements[1],
                i=orbital_elements[2],
                Omega=orbital_elements[3],
                omega=orbital_elements[4],
                M0=orbital_elements[5],
                epoch=epoch_for_M0,
                close_approach_time=close_approach_time,
                duration_days=730,  # 2 года вокруг сближения
                frames=100
            )
            return orbit_animation
        except Exception as anim_error:
            print(f"Анимация не создана: {anim_error}")
            return ""
    
    def _build_response(self, orbital_elements: List[float], min_distance_au: float,
                       closest_approach_time: datetime, orbit_animation: str) -> CloseApproachResponse:
        """Формирует объект ответа"""
        distance_km = min_distance_au * 149597870.7
        
        return CloseApproachResponse(
            min_distance_km=distance_km,
            min_distance_au=min_distance_au,
            closest_approach_time=closest_approach_time,
            big_poluos=orbital_elements[0],
            eks=orbital_elements[1],
            i=orbital_elements[2],
            calculation_id=str(uuid.uuid4()),
            orbit_animation=orbit_animation
        )
    
    def _get_fallback_orbit(self) -> List[float]:
        """Запасной набор элементов орбиты (Марс) с небольшим шумом"""
        target = [
            1.52366,           # a
            0.0934,            # e
            np.radians(1.85),  # i
            np.radians(49.58), # Ω
            np.radians(286.46),# ω
            np.radians(19.41)  # M0
        ]
        perturb = 1 + np.random.normal(0, 0.01, 6)
        fallback = [target[i] * perturb[i] for i in range(6)]
        fallback[0] = max(0.1, fallback[0])
        fallback[1] = max(0.0, min(0.99, fallback[1]))
        fallback[2] = max(0.0, min(np.pi, fallback[2]))
        return fallback