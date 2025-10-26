import { useState } from 'react';
import { cometService } from '../services/cometService';

export function useOrbitCalculation() {
  const [loading, setLoading] = useState(false);
  const [generatingAnimation, setGeneratingAnimation] = useState(false);
  const [orbitData, setOrbitData] = useState(null);
  const [closeApproachData, setCloseApproachData] = useState(null);
  const [orbitAnimation, setOrbitAnimation] = useState(null);

  const calculateOrbit = async (observations) => {
    console.log('🔧 useOrbitCalculation: calculateOrbit called');
    setLoading(true);
    
    try {
      console.log('📤 Calling cometService.calculateOrbit...');
      const result = await cometService.calculateOrbit(observations);
      console.log('📥 cometService.calculateOrbit result:', result);
      
      if (result && typeof result === 'object') {
        const safeOrbitData = { 
          big_poluos: result.big_poluos || 0,
          eks: result.eks || 0,  
          i: result.i || 0,
          min_distance_au: result.min_distance_au || 0,
          min_distance_km: result.min_distance_km || 0,
          closest_approach_time: result.closest_approach_time || null,
          orbit_animation: result.orbit_animation || null,
          calculation_id: result.calculation_id || null
        };
        
        console.log('💾 Setting orbitData:', safeOrbitData);
        setOrbitData(safeOrbitData);

        if (result.closest_approach_time) {
          console.log('📅 Setting closeApproachData');
          setCloseApproachData({ 
            date: new Date(result.closest_approach_time), 
            distanceAU: result.min_distance_au || 0, 
            distanceKm: result.min_distance_km || 0 
          });
        }
        
        return safeOrbitData;
      } else {
        console.error('❌ Invalid result format:', result);
        throw new Error('Invalid response format from server');
      }
    } catch (error) {
      console.error('💥 Error in calculateOrbit:', error);
      throw error;
    } finally {
      console.log('🏁 Setting loading to false');
      setLoading(false);
    }
  };

  const generateAnimation = async (orbitData, originalObservations) => {
    console.log('🎬 generateAnimation called with orbitData:', orbitData);
    console.log('🎬 originalObservations:', originalObservations);
    
    setGeneratingAnimation(true);
    try {
      // Используем данные орбиты для генерации анимации
      const result = await cometService.generateOrbitAnimation(orbitData, originalObservations);
      
      if (result && result.orbit_animation) {
        setOrbitAnimation(result.orbit_animation);
        // Обновляем orbitData с новой анимацией
        setOrbitData(prev => prev ? { ...prev, orbit_animation: result.orbit_animation } : null);
        return result.orbit_animation;
      }
    } catch (error) {
      console.error('Error generating animation:', error);
      throw error;
    } finally {
      setGeneratingAnimation(false);
    }
  };

  return { 
    loading, 
    generatingAnimation,
    orbitData, 
    closeApproachData,
    orbitAnimation,
    calculateOrbit,
    generateAnimation,
    setLoading 
  };
}