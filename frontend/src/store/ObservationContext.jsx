import React, { createContext, useState, useCallback, useContext } from 'react';

const ObservationContext = createContext();

export function useObservation() {
  const context = useContext(ObservationContext);
  if (!context) {
    throw new Error('useObservation must be used within an ObservationProvider');
  }
  return context;
}

export function ObservationProvider({ children }) {
  const [observations, setObservations] = useState([]);

  const addObservation = useCallback((observation) => {
    const newObs = {
      id: Date.now(),
      ...observation
    };
    setObservations(prev => [...prev, newObs]);
  }, []);

  const removeObservation = useCallback((id) => {
    setObservations(prev => prev.filter(obs => obs.id !== id));
  }, []);

  const clearObservations = useCallback(() => {
    setObservations([]);
  }, []);

  return (
    <ObservationContext.Provider value={{
      observations,
      addObservation,
      removeObservation,
      clearObservations
    }}>
      {children}
    </ObservationContext.Provider>
  );
}