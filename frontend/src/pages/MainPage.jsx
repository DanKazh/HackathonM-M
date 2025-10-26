import React, { useState, useEffect } from 'react';
import ObservationInput from '../components/observations/ObservationInput';
import ObservationTable from '../components/observations/ObservationTable';
import CombinedResults from '../components/results/CombinedResults';
import StatusMessage from '../components/common/StatusMessage';
import { useObservations } from '../hooks/useObservations';
import { useLocalStorage } from '../hooks/useLocalStorage';
import { useOrbitCalculation } from '../hooks/useOrbitCalculation';
import { cometService } from '../services/cometService'; // ← Импортируем объект cometService
import './MainPage.css';

function MainPage() {
  const [storedObservations, setStoredObservations] = useLocalStorage('comet-observations', []);
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
  const { checkAuth } = useAuth();

  // Сохраняем наблюдения в localStorage при изменении
  useEffect(() => {
    setStoredObservations(observations);
  }, [observations, setStoredObservations]);

  // Проверяем аутентификацию при загрузке
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  // Функция для преобразования closeApproachData
  const getProcessedCloseApproachData = () => {
    if (!closeApproachData) return null;
    
    if (Array.isArray(closeApproachData) && closeApproachData.length === 3) {
      return [
        new Date(closeApproachData[0]),
        closeApproachData[1],
        closeApproachData[2]
      ];
    }
    
    return closeApproachData;
  };

  const processedCloseApproachData = getProcessedCloseApproachData();

  const handleCalculate = async (observationsToCalculate) => {
    try {
      setStatus({ message: 'Выполняется расчет орбиты...', type: 'info' });

      // Автоматически выбираем правильный эндпоинт в зависимости от авторизации
      const result = await calculateOrbitWithAuth(observationsToCalculate);

      if (result.error) {
        setStatus({ message: `Ошибка: ${result.error}`, type: 'error' });
      } else {
        const message = isAuthenticated 
          ? 'Расчет орбиты завершен и сохранен! ✅' 
          : 'Расчет орбиты завершен! (для сохранения войдите в систему)';
        setStatus({ message, type: 'success' });
      }
    } catch (error) {
      setStatus({ message: 'Ошибка при расчете орбиты', type: 'error' });
      console.error('Calculation error:', error);
    }
  };

  // Функция для принудительного сохранения с дополнительными данными
  const handleCalculateAndSave = async (saveData) => {
    if (!isAuthenticated) {
      setStatus({ message: 'Для сохранения расчетов требуется авторизация', type: 'error' });
      return;
    }

    try {
      setStatus({ message: 'Выполняется расчет с сохранением...', type: 'info' });

      const result = await calculateOrbitWithSave(observations, saveData);

      if (result.error) {
        setStatus({ message: `Ошибка сохранения: ${result.error}`, type: 'error' });
      } else {
        setStatus({ 
          message: `Расчет сохранен! ID: ${result.group_id || result.calculation_id}`, 
          type: 'success' 
        });
      }
    } catch (error) {
      setStatus({ message: 'Ошибка при сохранении расчета', type: 'error' });
      console.error('Save calculation error:', error);
    }
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
    a.download = `comet-orbit-data-${new Date().toISOString().split('T')[0]}.json`;
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
          isAuthenticated={isAuthenticated}
        />
      </div>
    </div>
  );
}

export default MainPage;