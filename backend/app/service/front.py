from typing import List, Optional
from datetime import datetime, timedelta
import random
from pydantic import BaseModel, Field

# Сначала определяем все схемы данных
class ObservationBase(BaseModel):
    timestamp: datetime
    ra_degrees: float = Field(..., ge=0, le=360, description="Прямое восхождение в градусах")
    dec_degrees: float = Field(..., ge=-90, le=90, description="Склонение в градусах")
    source: str = Field(default="manual", description="Источник наблюдения")

class ObservationCreate(ObservationBase):
    pass

class ObservationResponse(ObservationBase):
    id: int
    created_at: datetime

class ObservationSetCreate(BaseModel):
    observations: List[ObservationCreate]
    name: Optional[str] = None
    description: Optional[str] = None

class ObservationSetResponse(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    observations: List[ObservationResponse]
    created_at: datetime
    observation_count: int

class OrbitalElements(BaseModel):
    semi_major_axis_au: float = Field(..., description="Большая полуось в а.е.")
    eccentricity: float = Field(..., ge=0, le=1, description="Эксцентриситет")
    inclination_deg: float = Field(..., ge=0, le=180, description="Наклонение в градусах")
    longitude_ascending_node_deg: float = Field(..., ge=0, le=360, description="Долгота восходящего узла в градусах")
    argument_of_perihelion_deg: float = Field(..., ge=0, le=360, description="Аргумент перицентра в градусах")
    time_of_perihelion: datetime = Field(..., description="Время прохождения перигелия")

class OrbitCalculationRequest(BaseModel):
    observation_set_id: int
    time_range_days: int = Field(default=365, ge=30, le=3650)

class OrbitCalculationResponse(BaseModel):
    id: int
    observation_set_id: int
    orbital_elements: OrbitalElements
    calculation_time: datetime
    rms_error: Optional[float] = None

class CloseApproachData(BaseModel):
    closest_approach_time: datetime
    distance_au: float = Field(..., description="Расстояние в астрономических единицах")
    distance_km: float = Field(..., description="Расстояние в километрах")
    relative_velocity_kms: float = Field(..., description="Относительная скорость в км/с")
    uncertainty: Optional[float] = Field(None, description="Погрешность расчета")

class CloseApproachResponse(BaseModel):
    orbit_calculation_id: int
    close_approach: CloseApproachData
    search_range_days: int

# Теперь определяем сервисы
class ObservationService:
    def __init__(self):
        # Временное хранилище (в реальном приложении используем БД)
        self.observation_sets = {}
        self.observations = {}
        self.next_id = 1

    async def create_observation_set(self, observation_set: ObservationSetCreate) -> ObservationSetResponse:
        set_id = self.next_id
        self.next_id += 1
        
        # Создаем наблюдения
        observation_responses = []
        for obs in observation_set.observations:
            obs_id = len(self.observations) + 1
            observation_data = ObservationResponse(
                id=obs_id,
                timestamp=obs.timestamp,
                ra_degrees=obs.ra_degrees,
                dec_degrees=obs.dec_degrees,
                source=obs.source,
                created_at=datetime.now()
            )
            self.observations[obs_id] = observation_data
            observation_responses.append(observation_data)
        
        # Создаем набор наблюдений
        set_data = ObservationSetResponse(
            id=set_id,
            name=observation_set.name,
            description=observation_set.description,
            observations=observation_responses,
            created_at=datetime.now(),
            observation_count=len(observation_responses)
        )
        
        self.observation_sets[set_id] = set_data
        
        return set_data

    async def get_observation_set(self, set_id: int) -> Optional[ObservationSetResponse]:
        return self.observation_sets.get(set_id)

    async def delete_observation_set(self, set_id: int) -> bool:
        if set_id in self.observation_sets:
            del self.observation_sets[set_id]
            return True
        return False

    async def get_all_observation_sets(self, skip: int = 0, limit: int = 100) -> List[ObservationSetResponse]:
        sets = list(self.observation_sets.values())[skip:skip + limit]
        return sets

class OrbitService:
    def __init__(self):
        self.orbit_calculations = {}
        self.close_approaches = {}
        self.next_calculation_id = 1

    async def calculate_orbit(self, request: OrbitCalculationRequest) -> OrbitCalculationResponse:
        calculation_id = self.next_calculation_id
        self.next_calculation_id += 1
        
        # Генерируем реалистичные орбитальные элементы
        orbital_elements = OrbitalElements(
            semi_major_axis_au=round(2 + random.random() * 3, 3),
            eccentricity=round(0.5 + random.random() * 0.4, 3),
            inclination_deg=round(5 + random.random() * 20, 2),
            longitude_ascending_node_deg=round(random.random() * 360, 2),
            argument_of_perihelion_deg=round(random.random() * 360, 2),
            time_of_perihelion=datetime.now() + timedelta(days=30)
        )
        
        calculation_data = OrbitCalculationResponse(
            id=calculation_id,
            observation_set_id=request.observation_set_id,
            orbital_elements=orbital_elements,
            calculation_time=datetime.now(),
            rms_error=round(random.random() * 0.1, 4)
        )
        
        self.orbit_calculations[calculation_id] = calculation_data
        
        return calculation_data

    async def get_orbit_calculation(self, calculation_id: int) -> Optional[OrbitCalculationResponse]:
        return self.orbit_calculations.get(calculation_id)

    async def get_calculations_for_set(self, observation_set_id: int) -> List[OrbitCalculationResponse]:
        calculations = [
            calc for calc in self.orbit_calculations.values() 
            if calc.observation_set_id == observation_set_id
        ]
        return calculations

    async def get_latest_calculation(self, observation_set_id: int) -> Optional[OrbitCalculationResponse]:
        calculations = await self.get_calculations_for_set(observation_set_id)
        if calculations:
            return max(calculations, key=lambda x: x.calculation_time)
        return None

    async def calculate_close_approach(self, calculation_id: int, time_range_days: int) -> CloseApproachResponse:
        # Симуляция расчета сближения
        approach_time = datetime.now() + timedelta(days=30 + random.random() * time_range_days)
        distance_au = round(0.1 + random.random() * 0.3, 3)
        distance_km = round(distance_au * 149597870.7, 2)  # 1 а.е. в км
        velocity = round(10 + random.random() * 30, 2)
        
        close_approach_data = CloseApproachData(
            closest_approach_time=approach_time,
            distance_au=distance_au,
            distance_km=distance_km,
            relative_velocity_kms=velocity,
            uncertainty=round(random.random() * 0.01, 4)
        )
        
        response_data = CloseApproachResponse(
            orbit_calculation_id=calculation_id,
            close_approach=close_approach_data,
            search_range_days=time_range_days
        )
        
        self.close_approaches[calculation_id] = response_data
        
        return response_data

    async def get_close_approach(self, calculation_id: int) -> Optional[CloseApproachResponse]:
        return self.close_approaches.get(calculation_id)

    async def get_close_approaches_for_set(self, observation_set_id: int) -> List[CloseApproachResponse]:
        approaches = []
        for calc_id, calc_data in self.orbit_calculations.items():
            if calc_data.observation_set_id == observation_set_id:
                approach = self.close_approaches.get(calc_id)
                if approach:
                    approaches.append(approach)
        return approaches

    async def delete_orbit_calculation(self, calculation_id: int) -> bool:
        if calculation_id in self.orbit_calculations:
            del self.orbit_calculations[calculation_id]
            if calculation_id in self.close_approaches:
                del self.close_approaches[calculation_id]
            return True
        return False