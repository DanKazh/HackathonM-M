import { useContext } from 'react';
import { ObservationContext } from '../store/ObservationContext';

export function useObservations() {
  const context = useContext(ObservationContext);
  
  if (!context) {
    throw new Error('useObservations must be used within ObservationProvider');
  }
  
  return context;
}
