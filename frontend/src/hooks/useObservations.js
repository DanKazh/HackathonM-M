// hooks/useObservations.js
import { useState } from 'react';

export function useObservations(initialObservations = []) {
  const [observations, setObservations] = useState(initialObservations);

  const addObservation = (observation) => {
    console.log('Adding observation:', observation);
    
    // Убедимся, что данные имеют правильный формат
    const newObservation = {
      id: Date.now(), // уникальный ID
      date: observation.date || new Date().toISOString().split('T')[0] + 'T00:00:00Z',
      ra: parseFloat(observation.ra) || 0,
      dec: parseFloat(observation.dec) || 0,
    };
    
    console.log('Processed observation:', newObservation);
    
    setObservations(prev => {
      const updated = [...prev, newObservation];
      console.log('Updated observations:', updated);
      return updated;
    });
  };

  const updateObservation = (id, updatedObservation) => {
    setObservations(prev => 
      prev.map(obs => obs.id === id ? { ...updatedObservation, id } : obs)
    );
  };

  const deleteObservation = (id) => {
    setObservations(prev => {
      const filtered = prev.filter(obs => obs.id !== id);
      console.log('After deletion:', filtered);
      return filtered;
    });
  };

  const clearObservations = () => {
    console.log('Clearing all observations');
    setObservations([]);
  };

  return {
    observations,
    addObservation,
    updateObservation,
    deleteObservation,
    clearObservations
  };
}