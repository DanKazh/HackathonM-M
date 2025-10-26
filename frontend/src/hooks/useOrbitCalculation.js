import { useState } from 'react';

export function useOrbitCalculation() {
  const [loading, setLoading] = useState(false);
  const [orbitData, setOrbitData] = useState(null);
  const [closeApproachData, setCloseApproachData] = useState(null);

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
        orbit_animation: result.orbit_animation || null, // Может быть null
        calculation_id: result.calculation_id || null
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

  return { 
    loading, 
    orbitData, 
    closeApproachData, 
    updateOrbitData, 
    setLoading 
  };
}