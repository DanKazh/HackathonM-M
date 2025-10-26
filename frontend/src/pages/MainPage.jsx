import React, { useState, useEffect } from 'react';
import ObservationInput from '../components/observations/ObservationInput';
import ObservationTable from '../components/observations/ObservationTable';
import OrbitResults from '../components/results/OrbitResults';
import CloseApproachResults from '../components/results/CloseApproachResults';
import CombinedResults from '../components/results/CombinedResults';
import StatusMessage from '../components/common/StatusMessage';
import { useObservations } from '../hooks/useObservations';
import { useLocalStorage } from '../hooks/useLocalStorage';
import { useOrbitCalculation } from '../hooks/useOrbitCalculation';
import { cometService } from '../services/cometService'; // ← Импортируем объект cometService
import './MainPage.css';
import ObservationList from '../components/observations/ObservationList';

function MainPage() {
  // Используем useLocalStorage для сохранения наблюдений
  const [storedObservations, setStoredObservations] = useLocalStorage('comet-observations', []);
  
  // Передаем сохраненные наблюдения в useObservations
  const { observations, addObservation, updateObservation, deleteObservation, clearObservations } = useObservations(storedObservations);
  
  // Используем обновленный хук с новыми методами
  const { 
    loading, 
    generatingAnimation,
    orbitData, 
    closeApproachData,
    orbitAnimation,
    calculateOrbit,
    generateAnimation 
  } = useOrbitCalculation();
  
  const [status, setStatus] = useState(null);

  // Сохраняем наблюдения в localStorage при изменении
  useEffect(() => {
    setStoredObservations(observations);
  }, [observations, setStoredObservations]);

  const handleCalculate = async (observations) => {
  try {
    // 1. Сначала рассчитываем орбиту
    const orbitResult = await calculateOrbit(observations);
    console.log('✅ Orbit calculation completed:', orbitResult);
    
    // 2. Затем генерируем анимацию на основе данных орбиты
    if (orbitResult) {
      console.log('🎬 Starting animation generation...');
      await generateAnimation(orbitResult, observations);
    }
    
  } catch (error) {
    console.error('Calculation error:', error);
    // Обработка ошибки
  }
};

  const handleSave = () => {
    setStatus({ message: 'Результаты сохранены', type: 'success' });
  };

  const handleExport = () => {
    const data = {
      observations,
      orbitData,
      closeApproachData,
      orbitAnimation
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
          <ObservationInput onAddObservation={addObservation} />
          <ObservationList
            observations={observations}
            onUpdateObservation={updateObservation}
            onDeleteObservation={deleteObservation}
            onClearObservations={clearObservations}
            onCalculateOrbit={handleCalculate} // ← обновили проп
            onGenerateAnimation={generateAnimation} // ← добавили новый проп
            calculating={loading}
            generatingAnimation={generatingAnimation}
          />
        </div>

        <CombinedResults
          data={orbitData}
          approachData={closeApproachData}
          orbitAnimation={orbitAnimation} // ← передаем отдельно анимацию
          loading={loading}
          onSave={handleSave}
          onExport={handleExport}
        />
      </div>
    </div>
  );
}

export default MainPage;