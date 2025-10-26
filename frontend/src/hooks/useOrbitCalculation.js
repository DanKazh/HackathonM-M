import { useState } from 'react';
import { useAuth } from './useAuth';
import { calculateOrbit, calculateAndSaveOrbit } from '../services/cometService';

export function useOrbitCalculation() {
  const [loading, setLoading] = useState(false);
  const [orbitData, setOrbitData] = useState(null);
  const [closeApproachData, setCloseApproachData] = useState(null);
  
  const { isAuthenticated } = useAuth();

  const updateOrbitData = (result) => {
    console.log('Received result in updateOrbitData:', result);
    
    if (result && !result.error) {
      // Создаем объект с безопасными значениями по умолчанию
      const safeOrbitData = { 
        big_poluos: result.big_poluos || 0,
        eks: result.eks || 0,  
        i: result.i || 0,
        min_distance_au: result.min_distance_au || 0,
        min_distance_km: result.min_distance_km || 0,
        closest_approach_time: result.closest_approach_time || null,
        orbit_animation: result.orbit_animation || null,
        calculation_id: result.calculation_id || null,
        group_id: result.group_id || null, // Добавляем group_id для сохраненных расчетов
        saved_at: result.saved_at || null // Добавляем время сохранения
      };
      
      setOrbitData(safeOrbitData);

      if (result.closest_approach_time) {
        setCloseApproachData({ 
          date: new Date(result.closest_approach_time), 
          distanceAU: result.min_distance_au || 0, 
          distanceKm: result.min_distance_km || 0 
        });
      }
    } else if (result && result.error) {
      console.error('Error in result:', result.error);
      // Сбрасываем данные при ошибке
      setOrbitData(null);
      setCloseApproachData(null);
    } else {
      // Если result null или undefined
      setOrbitData(null);
      setCloseApproachData(null);
    }
  }

  // Новая функция для расчета орбиты с учетом авторизации
  const calculateOrbitWithAuth = async (observations, saveData = {}) => {
    setLoading(true);
    
    try {
      let result;
      
      if (isAuthenticated) {
        // Для авторизованных пользователей используем ручку с сохранением
        console.log('🔄 Using calculate-and-save endpoint for authenticated user');
        result = await calculateAndSaveOrbit(observations, saveData);
      } else {
        // Для неавторизованных пользователей используем обычную ручку
        console.log('🔄 Using calculate endpoint for guest user');
        result = await calculateOrbit(observations);
      }
      
      updateOrbitData(result);
      return result;
      
    } catch (error) {
      console.error('Calculation error:', error);
      const errorResult = { 
        error: error.message || 'Ошибка расчета орбиты',
        details: error 
      };
      updateOrbitData(errorResult);
      return errorResult;
    } finally {
      setLoading(false);
    }
  }

  // Функция для принудительного расчета без сохранения (даже для авторизованных)
  const calculateOrbitWithoutSave = async (observations) => {
    setLoading(true);
    
    try {
      console.log('🔄 Using calculate endpoint (forced without save)');
      const result = await calculateOrbit(observations);
      updateOrbitData(result);
      return result;
    } catch (error) {
      console.error('Calculation error:', error);
      const errorResult = { 
        error: error.message || 'Ошибка расчета орбиты',
        details: error 
      };
      updateOrbitData(errorResult);
      return errorResult;
    } finally {
      setLoading(false);
    }
  }

  // Функция для принудительного расчета с сохранением (требует авторизации)
  const calculateOrbitWithSave = async (observations, saveData) => {
    if (!isAuthenticated) {
      const errorResult = { 
        error: 'Требуется авторизация для сохранения расчетов'
      };
      updateOrbitData(errorResult);
      return errorResult;
    }
    
    setLoading(true);
    
    try {
      console.log('🔄 Using calculate-and-save endpoint (forced with save)');
      const result = await calculateAndSaveOrbit(observations, saveData);
      updateOrbitData(result);
      return result;
    } catch (error) {
      console.error('Calculation error:', error);
      const errorResult = { 
        error: error.message || 'Ошибка расчета орбиты',
        details: error 
      };
      updateOrbitData(errorResult);
      return errorResult;
    } finally {
      setLoading(false);
    }
  }

  return { 
    loading, 
    orbitData, 
    closeApproachData, 
    updateOrbitData, 
    setLoading,
    calculateOrbitWithAuth, // Основная функция с автоматическим выбором эндпоинта
    calculateOrbitWithoutSave, // Принудительный расчет без сохранения
    calculateOrbitWithSave, // Принудительный расчет с сохранением
    isAuthenticated // Добавляем информацию об авторизации
  };
}