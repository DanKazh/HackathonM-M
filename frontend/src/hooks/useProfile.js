import { useState, useEffect } from 'react';
import api from '../services/api';

export function useProfile() {
  const [userCalculations, setUserCalculations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUserCalculations = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.get('/api/my-calculations');
      setUserCalculations(response.data.calculations || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка загрузки вычислений');
      console.error('Error fetching user calculations:', err);
    } finally {
      setLoading(false);
    }
  };

  const deleteCalculation = async (calculationId) => {
    try {
      // Пока просто удаляем из состояния (можно добавить эндпоинт удаления на бэкенде)
      setUserCalculations(prev => 
        prev.filter(calc => calc.calculation_id !== calculationId)
      );
    } catch (err) {
      setError('Ошибка при удалении вычисления');
      console.error('Error deleting calculation:', err);
    }
  };

  useEffect(() => {
    fetchUserCalculations();
  }, []);

  return {
    userCalculations,
    loading,
    error,
    fetchUserCalculations,
    deleteCalculation
  };
}