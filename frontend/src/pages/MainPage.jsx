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
import { calculateOrbit } from '../services/cometService';
import './MainPage.css';

function MainPage() {
  // Используем useLocalStorage для сохранения наблюдений
  const [storedObservations, setStoredObservations] = useLocalStorage('comet-observations', []);
  
  // Передаем сохраненные наблюдения в useObservations
  const { observations, addObservation, updateObservation, deleteObservation, clearObservations } = useObservations(storedObservations);
  
  const { loading, orbitData, closeApproachData, updateOrbitData, setLoading } = useOrbitCalculation();
  const [status, setStatus] = useState(null);

  // Сохраняем наблюдения в localStorage при изменении
  useEffect(() => {
    setStoredObservations(observations);
  }, [observations, setStoredObservations]);

  // Функция для преобразования closeApproachData
  const getProcessedCloseApproachData = () => {
    if (!closeApproachData) return null;
    
    // Если closeApproachData - массив из трех элементов
    if (Array.isArray(closeApproachData) && closeApproachData.length === 3) {
      return [
        new Date(closeApproachData[0]), // Первый элемент преобразуем в Date
        closeApproachData[1],           // Второй элемент без изменений
        closeApproachData[2]            // Третий элемент без изменений
      ];
    }
    
    return closeApproachData;
  };

  const processedCloseApproachData = getProcessedCloseApproachData();

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
      closeApproachData: processedCloseApproachData
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
          <ObservationTable 
            observations={observations}
            onUpdateObservation={updateObservation}
            onDeleteObservation={deleteObservation}
            onClearObservations={clearObservations}
            onCalculate={handleCalculate} 
          />
        </div>

      <CombinedResults
        data={orbitData} // данные орбиты
        approachData={processedCloseApproachData} 
      
        onSave={handleSave}
        onExport={handleExport}
      />
      </div>

     
    </div>
  );
}

export default MainPage;