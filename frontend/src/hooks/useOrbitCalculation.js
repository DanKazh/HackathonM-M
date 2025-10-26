import { useState } from 'react';

export function useOrbitCalculation() {
  const [loading, setLoading] = useState(false);
  const [orbitData, setOrbitData] = useState(null);
  const [closeApproachData, setCloseApproachData] = useState(null);

  const updateOrbitData = (result) => {
    if (result) {
      setOrbitData({ 
        semiMajorAxis: 2.765, 
        eccentricity: 0.892, 
        inclination: 15.67 
      });

      console.log(result.closest_approach_time);
      setCloseApproachData({ 
        date: new Date(result.closest_approach_time), 
        distanceAU: result.min_distance_au, 
        distanceKm: result.min_distance_km 
      });
    }
  }

  return { loading, orbitData, closeApproachData, updateOrbitData, setLoading };
}