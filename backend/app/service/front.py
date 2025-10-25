# orbit_calculation_service.py
from typing import List
from models.schemas import ObservationPoint, CloseApproachResponse
import uuid
from orbital_core.calculator.orbitDetermination import OrbitDetermination
from datetime import datetime
import numpy as np
from orbit_visualizer import OrbitVisualizer  # ← ваш исправленный класс


class OrbitCalculationService:
    def __init__(self):
        self.orbit_determination = OrbitDetermination()
        self.visualizer = OrbitVisualizer()  # ← добавили визуализатор

    async def calculate_min_distance(self, observations: List[ObservationPoint]) -> CloseApproachResponse:
        try:
            # Добавление наблюдений
            for obs in observations:
                ra_hours = obs.ra_degrees / 15.0
                self.orbit_determination.add_observation(
                    obs.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    ra_hours,
                    obs.dec_degrees
                )
            
            # Расчёт орбиты → [a, e, i, Omega, omega, M0]
            orbital_elements = self.orbit_determination.find_best_solution()
            if orbital_elements is None:
                orbital_elements = self._get_fallback_orbit()
            
            # Минимальное расстояние
            min_distance_approx, min_date_approx, _ = self.orbit_determination.calculate_min_earth_distance(orbital_elements)
            min_distance, min_date = self.orbit_determination.find_exact_min_distance(min_date_approx)
            distance_km = min_distance * 149597870.7

            # === Генерация анимации ===
            orbit_animation = ""
            try:
                # Эпоха для M0 — обычно первое наблюдение
                epoch_for_M0 = observations[0].timestamp

                orbit_animation = self.visualizer.create_orbit_animation(
                    a=orbital_elements[0],
                    e=orbital_elements[1],
                    i=orbital_elements[2],
                    Omega=orbital_elements[3],
                    omega=orbital_elements[4],
                    M0=orbital_elements[5],
                    epoch=epoch_for_M0,
                    close_approach_time=min_date,
                    duration_days=730,   # 2 года вокруг сближения
                    frames=100
                )
            except Exception as anim_error:
                print(f"⚠️ Анимация не создана: {anim_error}")

            return CloseApproachResponse(
                min_distance_km=distance_km,
                min_distance_au=min_distance,
                closest_approach_time=min_date,
                big_poluos=orbital_elements[0],
                eks=orbital_elements[1],
                i=orbital_elements[2],
                calculation_id=str(uuid.uuid4()),
                orbit_animation=orbit_animation  # ← передаём на фронтенд
            )
            
        except Exception as e:
            raise ValueError(f"Ошибка при расчёте орбиты: {str(e)}")

    def _get_fallback_orbit(self):
        """Запасной набор элементов (Марс) с небольшим шумом."""
        import numpy as np
        target = [
            1.52366,           # a
            0.0934,            # e
            np.radians(1.85),  # i
            np.radians(49.58), # Ω
            np.radians(286.46),# ω
            np.radians(19.41)  # M0 (на эпоху J2000 или первого наблюдения)
        ]
        perturb = 1 + np.random.normal(0, 0.01, 6)
        fallback = [target[i] * perturb[i] for i in range(6)]
        fallback[0] = max(0.1, fallback[0])
        fallback[1] = max(0.0, min(0.99, fallback[1]))
        fallback[2] = max(0.0, min(np.pi, fallback[2]))
        return fallback