from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime

# Импорты схем
from app.models.schemas import (
    ResultsResponse,
    ResultsSummary,
    ObservationSetSummary,
    OrbitCalculationResponse,
    CloseApproachData,
    ObservationSetResponse
)

# Импорты сервисов
from app.service import ObservationService
from app.service import OrbitService

router = APIRouter()

# Инициализация сервисов
observation_service = ObservationService()
orbit_service = OrbitService()

@router.get(
    "",
    response_model=ResultsResponse,
    summary="Получить сводку результатов",
    description="Возвращает сводную информацию по всем наборам наблюдений и расчетам"
)
async def get_results(
    include_observations: bool = Query(False, description="Включать детали наблюдений"),
    limit: int = Query(10, ge=1, le=100, description="Лимит наборов"),
    sort_by: str = Query("recent", description="Сортировка: recent, name, observations_count")
):
    try:
        # Получаем все наборы наблюдений
        observation_sets = await observation_service.get_all_observation_sets(0, limit)
        
        # Сортируем наборы
        if sort_by == "name":
            observation_sets.sort(key=lambda x: x.name or "")
        elif sort_by == "observations_count":
            observation_sets.sort(key=lambda x: x.observation_count, reverse=True)
        else:  # recent
            observation_sets.sort(key=lambda x: x.created_at, reverse=True)
        
        # Собираем сводную информацию для каждого набора
        set_summaries = []
        
        for obs_set in observation_sets:
            # Получаем последний расчет орбиты для этого набора
            last_calculation = await orbit_service.get_latest_calculation(obs_set.id)
            
            # Получаем сближение для последнего расчета
            close_approach = None
            if last_calculation:
                close_approach_data = await orbit_service.get_close_approach(last_calculation.id)
                if close_approach_data:
                    close_approach = close_approach_data.close_approach
            
            # Определяем статус набора
            if obs_set.observation_count == 0:
                status = "empty"
            elif not last_calculation:
                status = "observations_only"
            else:
                status = "calculated"
            
            summary = ObservationSetSummary(
                id=obs_set.id,
                name=obs_set.name,
                description=obs_set.description,
                created_at=obs_set.created_at,
                observation_count=obs_set.observation_count,
                last_calculation=last_calculation,
                close_approach=close_approach,
                status=status
            )
            set_summaries.append(summary)
        
        # Считаем общую статистику
        total_observations = sum(obs_set.observation_count for obs_set in observation_sets)
        total_calculations = len([s for s in set_summaries if s.last_calculation])
        total_approaches = len([s for s in set_summaries if s.close_approach])
        
        results_summary = ResultsSummary(
            total_observation_sets=len(observation_sets),
            total_observations=total_observations,
            total_orbit_calculations=total_calculations,
            total_close_approaches=total_approaches
        )
        
        return ResultsResponse(
            summary=results_summary,
            observation_sets=set_summaries
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении результатов: {str(e)}"
        )

@router.get(
    "/set/{set_id}",
    response_model=ObservationSetSummary,
    summary="Получить результаты для конкретного набора",
    description="Возвращает детальную сводку по конкретному набору наблюдений"
)
async def get_results_for_set(set_id: int):
    try:
        # Получаем набор наблюдений
        obs_set = await observation_service.get_observation_set(set_id)
        if not obs_set:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Набор наблюдений с ID {set_id} не найден"
            )
        
        # Получаем последний расчет орбиты
        last_calculation = await orbit_service.get_latest_calculation(obs_set.id)
        
        # Получаем сближение
        close_approach = None
        if last_calculation:
            close_approach_data = await orbit_service.get_close_approach(last_calculation.id)
            if close_approach_data:
                close_approach = close_approach_data.close_approach
        
        # Определяем статус
        if obs_set.observation_count == 0:
            status = "empty"
        elif not last_calculation:
            status = "observations_only"
        else:
            status = "calculated"
        
        return ObservationSetSummary(
            id=obs_set.id,
            name=obs_set.name,
            description=obs_set.description,
            created_at=obs_set.created_at,
            observation_count=obs_set.observation_count,
            last_calculation=last_calculation,
            close_approach=close_approach,
            status=status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении результатов для набора {set_id}: {str(e)}"
        )