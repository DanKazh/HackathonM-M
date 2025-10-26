# routes/front.py
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from models.schemas import (
    ObservationRequest, 
    CloseApproachResponse, 
    ObservationPoint, 
    ErrorResponse,
    SaveCalculationRequest,
    CalculationResponse,
    UserCalculationsResponse,
    SavedCalculation
)
from service.front import OrbitCalculationService
from dependencies import get_current_user, get_database
from repo.database.database import PostgresDB
import uuid

router = APIRouter()
api_service = ApiService()

@router.post(
    "/calculate",
    response_model=CloseApproachResponse,
    summary="Рассчитать минимальное расстояние до Земли",
    description="Принимает список наблюдений и возвращает минимальное расстояние до Земли и время сближения. Доступно без авторизации.",
    responses={
        400: {"model": ErrorResponse, "description": "Неверный формат данных"},
        500: {"model": ErrorResponse, "description": "Ошибка расчета"}
    }
)
async def calculate_min_distance(request: ObservationRequest):
    """Расчет доступен всем пользователям (без авторизации)"""
    try:
        # Валидация и преобразование входных данных
        observations = await _validate_and_convert_observations(request.observations)
        
        # Вызов сервиса для расчета
        result = await calculation_service.calculate_min_distance(observations)
        
        return result
        
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

@router.post(
    "/calculate-and-save",
    response_model=CalculationResponse,
    summary="Рассчитать и сохранить результат",
    description="Рассчитывает минимальное расстояние и сохраняет результат в базу данных. Требуется авторизация.",
    responses={
        400: {"model": ErrorResponse, "description": "Неверный формат данных"},
        401: {"model": ErrorResponse, "description": "Требуется авторизация"},
        500: {"model": ErrorResponse, "description": "Ошибка расчета или сохранения"}
    }
)
async def calculate_and_save(
    request: SaveCalculationRequest,
    current_user: dict = Depends(get_current_user),
    db: PostgresDB = Depends(get_database)
):
    """Расчет и сохранение - только для авторизованных пользователей"""
    try:
        # Валидация и преобразование входных данных
        observations = await _validate_and_convert_observations(request.observations)
        
        # Вызов сервиса для расчета
        calculation_result = await calculation_service.calculate_min_distance(observations)
        
        # Сохранение в базу данных
        saved_calculation = await _save_calculation_to_db(
            db=db,
            user_id=current_user["user_id"],
            request=request,
            calculation_result=calculation_result,
            observations_count=len(observations)
        )
        
        return CalculationResponse(
            calculation_id=saved_calculation["calculation_id"],
            group_id=saved_calculation["group_id"],
            min_distance_km=calculation_result.min_distance_km,
            min_distance_au=calculation_result.min_distance_au,
            closest_approach_time=calculation_result.closest_approach_time,
            saved_at=saved_calculation["saved_at"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении расчета: {str(e)}"
        )

async def _validate_and_convert_observations(observation_lists: List[List]) -> List[ObservationPoint]:
    """
    Валидирует и преобразует список списков в список ObservationPoint
    """
    if not observation_lists:
        raise ValueError("Список наблюдений не может быть пустым")
    
    observations = []
    
    for i, obs_list in enumerate(observation_lists):
        if len(obs_list) != 3:
            raise ValueError(f"Наблюдение {i} должно содержать 3 элемента: timestamp, ra, dec")
        
        timestamp, ra, dec = obs_list
        
        # Создаем ObservationPoint (Pydantic сам выполнит валидацию)
        try:
            observation = ObservationPoint(
                timestamp=timestamp,
                ra_degrees=float(ra),
                dec_degrees=float(dec)
            )
            observations.append(observation)
        except Exception as e:
            raise ValueError(f"Неверный формат данных в наблюдении {i}: {str(e)}")
    
    # Проверяем, что есть хотя бы 5 наблюдений для расчета орбиты
    if len(observations) < 5:
        raise ValueError("Для расчета орбиты необходимо минимум 5 наблюдений")
    
    return observations

async def _save_calculation_to_db(
    db: PostgresDB,
    user_id: str,
    request: SaveCalculationRequest,
    calculation_result: CloseApproachResponse,
    observations_count: int
) -> dict:
    """Сохраняет расчет в базу данных"""
    
    # Создаем группу наблюдений
    group_id = await db.fetchval(
        """INSERT INTO observation_groups (name, description, status) 
        VALUES ($1, $2, $3) RETURNING id""",
        request.group_name or "Расчет от " + calculation_result.closest_approach_time.isoformat(),
        request.group_description,
        "completed"
    )
    
    # Сохраняем наблюдения
    for i, obs_list in enumerate(request.observations):
        timestamp_str, ra, dec = obs_list
        
        # Преобразуем строку даты в объект datetime
        try:
            if 'T' in timestamp_str:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S%z')
        except (ValueError, AttributeError):
            timestamp = datetime.now()
        
        await db.execute(
            """INSERT INTO observations 
            (user_id, group_id, observation_time, right_ascension, declination, observer_name) 
            VALUES ($1, $2, $3, $4, $5, $6)""",
            uuid.UUID(user_id),
            group_id,
            timestamp,
            float(ra),  # Передаем как число
            float(dec), # Передаем как число
            request.observer_name or f"Наблюдение {i+1}"
        )
    
    # Сохраняем орбитальные параметры
    orbital_params_id = await db.fetchval(
        """INSERT INTO orbital_parameters 
        (group_id, semi_major_axis, eccentricity, inclination, 
         longitude_ascending_node, argument_perihelion, time_perihelion, used_observations_count) 
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id""",
        group_id,
        1.0,   # Передаем как число
        0.5,   # Передаем как число
        45.0,  # Передаем как число
        90.0,  # Передаем как число
        180.0, # Передаем как число
        calculation_result.closest_approach_time,
        observations_count
    )
    
    # Сохраняем результат сближения
    await db.execute(
        """INSERT INTO close_approaches 
        (group_id, orbital_parameters_id, approach_time, distance_au, distance_km) 
        VALUES ($1, $2, $3, $4, $5)""",
        group_id,
        orbital_params_id,
        calculation_result.closest_approach_time,
        float(calculation_result.min_distance_au),  # Передаем как число
        float(calculation_result.min_distance_km)   # Передаем как число
    )
    
    return {
        "calculation_id": calculation_result.calculation_id,
        "group_id": str(group_id),
        "saved_at": datetime.now()
    }

@router.get(
    "/my-calculations",
    response_model=UserCalculationsResponse,
    summary="Получить все мои сохраненные расчеты",
    description="Возвращает список всех сохраненных расчетов текущего пользователя",
    responses={
        401: {"model": ErrorResponse, "description": "Требуется авторизация"},
        500: {"model": ErrorResponse, "description": "Ошибка получения данных"}
    }
)

async def get_my_calculations(
    current_user: dict = Depends(get_current_user),
    db: PostgresDB = Depends(get_database)
):
    """Получение всех сохраненных расчетов пользователя"""
    try:
        
        # Запрос к базе данных для получения всех расчетов пользователя
        calculations = await db.fetch("""
            SELECT 
                ca.id as calculation_id,
                og.id as group_id,
                og.name as group_name,
                og.description as group_description,
                ca.distance_km as min_distance_km,
                ca.distance_au as min_distance_au,
                ca.approach_time as closest_approach_time,
                ca.calculation_date as saved_at,
                COUNT(o.id) as observation_count,
                MAX(o.observer_name) as observer_name
            FROM close_approaches ca
            JOIN orbital_parameters op ON ca.orbital_parameters_id = op.id
            JOIN observation_groups og ON op.group_id = og.id
            JOIN observations o ON og.id = o.group_id
            WHERE o.user_id = $1
            GROUP BY ca.id, og.id, og.name, og.description, ca.distance_km, 
                     ca.distance_au, ca.approach_time, ca.calculation_date
            ORDER BY ca.calculation_date DESC
        """, uuid.UUID(current_user["user_id"]))
        
        # Преобразуем результаты в модель ответа
        calculations_list = [
            SavedCalculation(
                calculation_id=calc["calculation_id"],
                group_id=calc["group_id"],
                group_name=calc["group_name"],
                group_description=calc["group_description"],
                min_distance_km=calc["min_distance_km"],
                min_distance_au=calc["min_distance_au"],
                closest_approach_time=calc["closest_approach_time"],
                observation_count=calc["observation_count"],
                saved_at=calc["saved_at"],
                observer_name=calc["observer_name"]
            )
            for calc in calculations
        ]
        
        return UserCalculationsResponse(
            calculations=calculations_list,
            total_count=len(calculations_list)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении расчетов: {str(e)}"
        )
    

@router.get(
    "/my-calculations/{calculation_id}",
    response_model=SavedCalculation,
    summary="Получить конкретный сохраненный расчет",
    description="Возвращает детальную информацию о конкретном сохраненном расчете",
    responses={
        401: {"model": ErrorResponse, "description": "Требуется авторизация"},
        404: {"model": ErrorResponse, "description": "Расчет не найден"},
        500: {"model": ErrorResponse, "description": "Ошибка получения данных"}
    }
)
async def get_calculation_by_id(
    calculation_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: PostgresDB = Depends(get_database)
):
    """Получение конкретного расчета по ID"""
    try:
        
        # Запрос к базе данных
        calculation = await db.fetchrow("""
            SELECT 
                ca.id as calculation_id,
                og.id as group_id,
                og.name as group_name,
                og.description as group_description,
                ca.distance_km as min_distance_km,
                ca.distance_au as min_distance_au,
                ca.approach_time as closest_approach_time,
                ca.calculation_date as saved_at,
                COUNT(o.id) as observation_count,
                MAX(o.observer_name) as observer_name
            FROM close_approaches ca
            JOIN orbital_parameters op ON ca.orbital_parameters_id = op.id
            JOIN observation_groups og ON op.group_id = og.id
            JOIN observations o ON og.id = o.group_id
            WHERE ca.id = $1 AND o.user_id = $2
            GROUP BY ca.id, og.id, og.name, og.description, ca.distance_km, 
                     ca.distance_au, ca.approach_time, ca.calculation_date
        """, calculation_id, uuid.UUID(current_user["user_id"]))
        
        if not calculation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Расчет не найден или у вас нет доступа к нему"
            )
        
        return SavedCalculation(
            calculation_id=calculation["calculation_id"],
            group_id=calculation["group_id"],
            group_name=calculation["group_name"],
            group_description=calculation["group_description"],
            min_distance_km=calculation["min_distance_km"],
            min_distance_au=calculation["min_distance_au"],
            closest_approach_time=calculation["closest_approach_time"],
            observation_count=calculation["observation_count"],
            saved_at=calculation["saved_at"],
            observer_name=calculation["observer_name"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении расчета: {str(e)}"
        )
    
    