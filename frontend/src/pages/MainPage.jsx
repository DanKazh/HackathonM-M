import React, { useState } from 'react';
import ObservationInput from '../components/observations/ObservationInput';
import ObservationTable from '../components/observations/ObservationTable';
import OrbitResults from '../components/results/OrbitResults';
import CloseApproachResults from '../components/results/CloseApproachResults';
import StatusMessage from '../components/common/StatusMessage';
import { useObservations } from '../hooks/useObservations';
import { useOrbitCalculation } from '../hooks/useOrbitCalculation';
import { calculateOrbit } from '../services/cometService';
import './MainPage.css';

function MainPage() {
  const { observations } = useObservations();
  const { loading, orbitData, closeApproachData, updateOrbitData, setLoading } = useOrbitCalculation();
  const [status, setStatus] = useState(null);

  const handleCalculate = async (observations) => {
    try {
      setLoading(true);
      setStatus({ message: 'Выполняется расчет орбиты...', type: 'info' });

      const result = await calculateOrbit(observations);

      updateOrbitData(result);

      setStatus({ message: 'Расчет орбиты завершен!', type: 'success' });
    } catch (error) {
      setStatus({ message: 'Ошибка при расчете орбиты', type: 'error' });
      console.error('Calculation error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = () => {
    setStatus({ message: 'Результаты сохранены', type: 'success' });
  };

  const handleExport = () => {
    const data = {
      observations,
      orbitData,
      closeApproachData
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'comet-orbit-data.json';
    a.click();
    URL.revokeObjectURL(url);
    
    setStatus({ message: 'Данные экспортированы', type: 'success' });
  };

  return (
    <div className="main-page">
      {status && (
        <StatusMessage
          message={status.message}
          type={status.type}
          onClose={() => setStatus(null)}
        />
      )}

      <div className="grid-container">
        <div className="input-section">
          <ObservationInput />
          <ObservationTable onCalculate={handleCalculate} />
        </div>

        <div className="results-section">
          <OrbitResults data={orbitData} loading={loading} />
        </div>
      </div>

      <CloseApproachResults
        data={closeApproachData}
        onSave={handleSave}
        onExport={handleExport}
      />
    </div>
  );
}

export default MainPage;
