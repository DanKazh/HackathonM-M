import React from 'react';
import HolographicPanel from '../common/HolographicPanel';
import ResultCard from './ResultCard';
import Button from '../common/Button';
import { formatDate } from '../../utils/formatters';
import './CloseApproachResults.css';

function CloseApproachResults({ data, onSave, onExport, orbitAnimation }) {
  return (
    <div className="combined-results-container">
      {/* Визуализация орбиты */}
      {orbitAnimation ? (
        <HolographicPanel 
          title="Визуализация орбиты"
          width="500px"
          height="auto"
          className="orbit-visualization-panel"
        >
          <div className="animation-container">
            <div className="image-wrapper">
              <img 
                src={`data:image/gif;base64,${orbitAnimation}`} 
                alt="Анимация орбиты кометы"
                className="orbit-gif"
              />
            </div>
            <p className="animation-description">
              Траектория движения кометы относительно Земли
            </p>
          </div>
        </HolographicPanel>
      ) : (
        <HolographicPanel 
          title="Визуализация орбиты"
          width="400px"
          height="300px"
          className="orbit-visualization-panel empty"
        >
          <div className="visualization-content">
            <div className="icon">🌌</div>
            <p className="placeholder-text">Ожидание данных</p>
            <p className="hint">Здесь будет отображаться расчетная орбита кометы</p>
          </div>
        </HolographicPanel>
      )}

      {/* Результаты сближения */}
      {data && (
        <HolographicPanel 
          title="Результаты сближения с Землей"
          width="500px"
          height="auto"
          className="approach-results-panel"
        >
          <div className="results-content">
            <div className="results-grid">
              <ResultCard
                label="Дата сближения"
                value={data.date ? formatDate(data.date) : '-'}
              />
              <ResultCard
                label="Расстояние"
                value={data.distanceAU}
                unit="а.е."
              />
              <ResultCard
                label="Расстояние"
                value={data.distanceKm}
                unit="км"
              />
            </div>

            <div className="action-buttons">
              <Button variant="success" onClick={onSave}>
                Сохранить результаты
              </Button>
              <Button onClick={onExport}>
                Экспорт данных
              </Button>
            </div>
          </div>
        </HolographicPanel>
      )}
    </div>
  );
}

export default CloseApproachResults;