from typing import List, Optional
from models.schemas import ObservationPoint, CloseApproachResponse, OrbitAnimationResponse
import uuid
<<<<<<< HEAD
from orbital_core.calculator.orbitDetermination import calculate_orbit
=======
from orbital_core.calculator.orbitDetermination import OrbitDetermination
from orbital_core.calculator.orbitDetermination import OrbitDeterminationDenis
>>>>>>> remotes/origin/dev/Babuleh78
from orbital_core.visualizer.orbitVisualizer import OrbitVisualizer
from orbital_core.calculator.orbitDetermination import calculate_orbit
from datetime import datetime
import numpy as np
import base64
import asyncio
from concurrent.futures import ThreadPoolExecutor

class OrbitCalculationService:
    """Сервис для расчета орбитальных параметров"""
    
    def __init__(self):
<<<<<<< HEAD
        # self.orbit_determination = OrbitDetermination()
=======
        self.orbit_determination = OrbitDetermination()
        self.distance_finder = OrbitDeterminationDenis()
>>>>>>> remotes/origin/dev/Babuleh78
        self.visualizer = OrbitVisualizer()
        self.animation_executor = ThreadPoolExecutor(max_workers=2)
    
    async def calculate_orbit(self, observations: List[ObservationPoint]) -> CloseApproachResponse:
        """
        Быстрый расчет орбитальных параметров и сближения
        """
        try:
            print(observations)
            observations_data = [[str(x.timestamp), x.ra_degrees, x.dec_degrees] for x in observations]
            orbital_elements = calculate_orbit(observations_data)
            print(orbital_elements)
            if orbital_elements is None:
                orbital_elements = self._get_fallback_orbit()
            
<<<<<<< HEAD
            # Расчёт орбитальных элементов
            orbital_elements = self._calculate_orbital_elements(observations)
            
            # Расчет минимального расстояния
=======
>>>>>>> remotes/origin/dev/Babuleh78
            min_distance_au, closest_approach_time = self._calculate_min_earth_distance(orbital_elements)
            
            # Формирование ответа БЕЗ анимации
            return self._build_response(
                orbital_elements, min_distance_au, closest_approach_time, orbit_animation=None
            )
            
        except Exception as e:
            raise ValueError(f"Ошибка при расчёте орбиты: {str(e)}")
    
    async def generate_orbit_animation(self, orbit_data: dict, observations: List[ObservationPoint]) -> OrbitAnimationResponse:
        """
        Генерация анимации орбиты на основе орбитальных параметров
        """
        try:
            # Извлекаем орбитальные параметры из данных
            orbital_elements = [
                orbit_data.get('big_poluos', 0),  # a - большая полуось
                orbit_data.get('eks', 0),         # e - эксцентриситет
                orbit_data.get('i', 0),           # i - наклонение (в градусах)
                0,  # Omega - долгота восходящего узла
                0,  # omega - аргумент перицентра
                0   # M0 - средняя аномалия
            ]
            
            # Получаем время сближения
            closest_approach_time = orbit_data.get('closest_approach_time')
            if isinstance(closest_approach_time, str):
                closest_approach_time = datetime.fromisoformat(closest_approach_time.replace('Z', '+00:00'))
            else:
                # Если время не передано, вычисляем его
                min_distance_au, closest_approach_time = self._calculate_min_earth_distance(orbital_elements)
            
            # Получаем эпоху из первого наблюдения
            epoch = observations[0].timestamp if observations else datetime.now()
            
            # Генерация анимации
            orbit_animation = await self._generate_orbit_animation(
                orbital_elements, observations, closest_approach_time
            )
            
            return OrbitAnimationResponse(
                calculation_id=str(uuid.uuid4()),
                orbit_animation=orbit_animation,
                status="completed"
            )
            
        except Exception as e:
            return OrbitAnimationResponse(
                calculation_id=str(uuid.uuid4()),
                orbit_animation=None,
                status="error",
                error_message=str(e)
            )
    
    # ДОБАВЛЯЕМ ОТСУТСТВУЮЩИЙ МЕТОД
    async def _generate_orbit_animation(self, orbital_elements: List[float], 
                                  observations: List[ObservationPoint],
                                  close_approach_time: datetime) -> str:
        """Генерация анимации в отдельном потоке"""
        try:
            # Запускаем в отдельном потоке чтобы не блокировать event loop
            loop = asyncio.get_event_loop()
            animation_bytes = await loop.run_in_executor(
                self.animation_executor,
                self.visualizer.create_orbit_animation,
                orbital_elements[0],  # a
                orbital_elements[1],  # e
                orbital_elements[2],  # i
                orbital_elements[3],  # Omega
                orbital_elements[4],  # omega
                orbital_elements[5],  # M0
                observations[0].timestamp,  # epoch
                close_approach_time,
                730,  # duration_days
                50    # frames (можно уменьшить для ускорения)
            )
            
            if animation_bytes and len(animation_bytes) > 0:
                return base64.b64encode(animation_bytes).decode('utf-8')
            return ""
                
        except Exception as anim_error:
            print(f"Анимация не создана: {anim_error}")
            return ""
    
    # Остальные методы остаются без изменений
    def _add_observations_to_determination(self, observations: List[ObservationPoint]) -> None:
        """Добавляет наблюдения в систему определения орбиты"""
        for obs in observations:
            ra_hours = obs.ra_degrees / 15.0
            self.orbit_determination.add_observation(
                obs.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                ra_hours,
                obs.dec_degrees
            )
    
    def _calculate_orbital_elements(self, observations: List[ObservationPoint]) -> List[float]:
        """Вычисляет орбитальные элементы"""
        observations_data = [[str(x.timestamp), x.ra_degrees, x.dec_degrees] for x in observations]
        orbital_elements = calculate_orbit(observations_data)
        if orbital_elements is None:
            orbital_elements = self._get_fallback_orbit()
        return orbital_elements
    
    def _calculate_min_earth_distance(self, orbital_elements: List[float]) -> tuple:
        """Вычисляет минимальное расстояние до Земли"""
        min_distance_approx, min_date_approx, _ = self.distance_finder.calculate_min_earth_distance(orbital_elements)
        min_distance, min_date = self.distance_finder.find_exact_min_distance(min_date_approx)
        return min_distance, min_date
    
    def _build_response(self, orbital_elements: List[float], min_distance_au: float,
                       closest_approach_time: datetime, orbit_animation: Optional[str]) -> CloseApproachResponse:
        """Формирует объект ответа"""
        distance_km = min_distance_au * 149597870.7
        
        return CloseApproachResponse(
            min_distance_km=round(distance_km, 2),
            min_distance_au=round(min_distance_au, 2),
            closest_approach_time=closest_approach_time,
            big_poluos=round(orbital_elements[0], 2),
            eks=round(orbital_elements[1], 2),
            i=round(orbital_elements[2], 2),
            calculation_id=str(uuid.uuid4()),
            orbit_animation=orbit_animation  # Может быть None
        )
    
    def _get_fallback_orbit(self) -> List[float]:
        """Запасной набор элементов орбиты"""
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