import { useState, useEffect } from 'react';
import apiService from '../services/api';

export function useObservations() {
  const [observations, setObservations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadObservations();
  }, []);

  const loadObservations = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getObservations();
      setObservations(data);
    } catch (err) {
      setError(err.message);
      console.error('Ошибка загрузки наблюдений:', err);
    } finally {
      setLoading(false);
    }
  };

  const addObservation = async (observation) => {
    try {
      setLoading(true);
      setError(null);
      const newObservation = await apiService.addObservation(observation);
      setObservations([...observations, newObservation]);
      return newObservation;
    } catch (err) {
      setError(err.message);
      console.error('Ошибка добавления наблюдения:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteObservation = async (id) => {
    try {
      setLoading(true);
      setError(null);
      await apiService.deleteObservation(id);
      setObservations(observations.filter(obs => obs.id !== id));
    } catch (err) {
      setError(err.message);
      console.error('Ошибка удаления наблюдения:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    observations,
    loading,
    error,
    addObservation,
    deleteObservation,
    refreshObservations: loadObservations
  };
}
