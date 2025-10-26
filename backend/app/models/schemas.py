from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

# Модели для запросов
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
    token_type: str = "bearer"

# Модели для JWT
class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

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
    calculation_id: str = Field(..., description="ID расчета")

class ErrorResponse(BaseModel):
    detail: str
    error_code: str = None