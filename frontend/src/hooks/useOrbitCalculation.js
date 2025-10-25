import { useState } from 'react';
import apiService from '../services/api';

export function useOrbitCalculation() {
  const [loading, setLoading] = useState(false);
  const [orbitData, setOrbitData] = useState(null);
  const [closeApproachData, setCloseApproachData] = useState(null);
  const [error, setError] = useState(null);

  const calculateOrbit = async (observations) => {
    try {
      setLoading(true);
      setError(null);

      const orbit = await apiService.calculateOrbit(observations);
      setOrbitData(orbit);

      try {
        const approach = await apiService.calculateCloseApproach(orbit);
        setCloseApproachData(approach);
      } catch (approachError) {
        console.warn('Не удалось рассчитать сближение:', approachError);
        setCloseApproachData(null);
      }

      return orbit;
    } catch (err) {
      setError(err.message);
      console.error('Ошибка расчета орбиты:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const resetResults = () => {
    setOrbitData(null);
    setCloseApproachData(null);
    setError(null);
  };

  return {
    loading,
    orbitData,
    closeApproachData,
    error,
    calculateOrbit,
    resetResults
  };
}
