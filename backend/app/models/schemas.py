from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

# Базовые схемы для наблюдений
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
    
    class Config:
        from_attributes = True

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
    
    class Config:
        from_attributes = True

# Схемы для орбитальных элементов
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

# Схемы для сближений
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

# Схемы для результатов
class ResultsSummary(BaseModel):
    total_observation_sets: int
    total_observations: int
    total_orbit_calculations: int
    total_close_approaches: int

class ObservationSetSummary(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    created_at: datetime
    observation_count: int
    last_calculation: Optional[OrbitCalculationResponse] = None
    close_approach: Optional[CloseApproachData] = None
    status: str = Field(..., description="Статус: 'empty', 'observations_only', 'calculated'")

class ResultsResponse(BaseModel):
    summary: ResultsSummary
    observation_sets: List[ObservationSetSummary]

# Схемы для обработки изображений
class ImageProcessingRequest(BaseModel):
    image_data: str  # base64 encoded image
    observation_time: datetime
    camera_params: Optional[dict] = None

class ImageProcessingResponse(BaseModel):
    success: bool
    coordinates: Optional[List[ObservationCreate]] = None
    error_message: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None