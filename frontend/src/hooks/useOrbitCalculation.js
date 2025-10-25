import { useState } from 'react';
export function useOrbitCalculation() {
  const [loading, setLoading] = useState(false);
  const [orbitData, setOrbitData] = useState(null);
  const [closeApproachData, setCloseApproachData] = useState(null);
  const calculateOrbit = async () => {
    setLoading(true);
    await new Promise(r => setTimeout(r, 2000));
    setOrbitData({ semiMajorAxis: 2.765, eccentricity: 0.892, inclination: 15.67 });
    setCloseApproachData({ date: '2024-07-15T08:23:45Z', distanceAU: 0.234, distanceKm: 35012456 });
    setLoading(false);
  };
  return { loading, orbitData, closeApproachData, calculateOrbit };
}