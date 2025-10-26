from pydantic import BaseModel
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from typing import List

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: UUID
    username: str

class TokenVerifyResponse(BaseModel):
    valid: bool
    user_id: UUID
    username: str

class OrbitAnimationResponse(BaseModel):
    orbit_animation: Optional[str] = Field(None, description="Анимация орбиты в base64")
    status: str = Field(..., description="Статус генерации анимации")
    error_message: Optional[str] = Field(None, description="Сообщение об ошибке")

class ObservationPoint(BaseModel):
    timestamp: datetime
    ra_degrees: float = Field(..., ge=0, le=360, description="Прямое восхождение в градусах")
    dec_degrees: float = Field(..., ge=-90, le=90, description="Склонение в градусах")

class ObservationRequest(BaseModel):
    observations: List[List] = Field(..., description="Список наблюдений: [[timestamp, ra, dec], ...]")

class CloseApproachResponse(BaseModel):
    min_distance_km: float = Field(..., description="Минимальное расстояние от Земли в км")
    min_distance_au: float = Field(..., description="Минимальное расстояние от Земли в а.е.")
    closest_approach_time: datetime = Field(..., description="Время максимального сближения")
    big_poluos: float = Field(..., description="Большая полуось орбиты")
    eks: float = Field(..., description="Эксцентриситет орбиты")
    i: float = Field(..., description="Наклонение орбиты")
    calculation_id: str = Field(..., description="ID расчета")
    orbit_animation: Optional[str] = Field(None, description="Анимация орбиты в base64")

class ErrorResponse(BaseModel):
    detail: str
    error_code: str = None


class SaveCalculationRequest(ObservationRequest):
    """Модель для запроса расчета с сохранением"""
    group_name: Optional[str] = None
    group_description: Optional[str] = None
    observer_name: Optional[str] = None

class CalculationResponse(BaseModel):
    """Модель ответа для сохраненного расчета"""
    calculation_id: str
    group_id: str
    min_distance_km: float
    min_distance_au: float
    closest_approach_time: datetime
    saved_at: datetime

class SavedCalculation(BaseModel):
    calculation_id: UUID
    group_id: UUID
    group_name: Optional[str] = None
    group_description: Optional[str] = None
    min_distance_km: float
    min_distance_au: float
    closest_approach_time: datetime
    observation_count: int
    saved_at: datetime
    observer_name: Optional[str] = None

class UserCalculationsResponse(BaseModel):
    """Модель ответа со списком расчетов пользователя"""
    calculations: List[SavedCalculation]
    total_count: int