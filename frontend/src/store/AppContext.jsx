import React, { createContext } from 'react';
import { ObservationProvider } from './ObservationContext';

export const AppContext = createContext();

export function AppProvider({ children }) {
  return (
    <ObservationProvider>
      {children}
    </ObservationProvider>
  );
}
