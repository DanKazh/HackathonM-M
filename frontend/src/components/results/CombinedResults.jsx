import React from 'react';
import HolographicPanel from '../common/HolographicPanel';
import ResultCard from './ResultCard';
import Button from '../common/Button';
import { formatDate } from '../../utils/formatters';
import './CombinedResults.css';

function CombinedResults({ 
  data, 
  loading, 
  onSave, 
  onExport, 
  orbitAnimation,
  approachData 
}) {
  // Если идет загрузка
  if (loading) {
    return (
      <HolographicPanel 
        title="Визуализация и результаты"
        width="500px"
        height="200px"
        className="combined-results-panel loading"
      >
        <div className="loading-content">
          <div className="loading-spinner"></div>
          <p>Вычисление орбиты...</p>
        </div>
      </HolographicPanel>
    );
  }

  return (
    <div className="combined-results-container">
      {/* Основная панель с визуализацией и орбитальными элементами */}
      <HolographicPanel 
        title="Визуализация и результаты"
        width="500px"
        height="auto"
        className="combined-results-panel"
      >
        <div className="combined-content">
          {/* Визуализация орбиты */}
          <div className="orbit-section">
            {orbitAnimation ? (
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
            ) : (
              <div className="visualization-placeholder">
                <div className="icon">🌌</div>
                <p className="placeholder-text">Ожидание данных</p>
                <p className="hint">Здесь будет отображаться расчетная орбита кометы</p>
              </div>
            )}
          </div>

          {/* Орбитальные элементы */}
          {data && (
            <div className="orbital-elements-section">
              <h4 className="section-title">Орбитальные элементы</h4>
              <div className="elements-grid">
                <ResultCard
                  label="Большая полуось"
                  value={data.big_poluos}
                  unit="а.е."
                  compact
                />
                <ResultCard
                  label="Эксцентриситет"
                  value={data.eks}
                  compact
                />
                <ResultCard
                  label="Наклонение"
                  value={data.i}
                  unit="°"
                  compact
                />
              </div>
            </div>
          )}
        </div>
      </HolographicPanel>

      {/* Панель сближения с Землей */}
      {approachData && (
        <HolographicPanel 
          title="Сближение с Землей"
          width="500px"
          height="auto"
          className="approach-results-panel"
        >
          <div className="approach-content">
            <div className="approach-grid">
              <ResultCard
                label="Дата сближения"
                value={approachData.date ? formatDate(approachData.date) : '-'}
                compact
              />
              <ResultCard
                label="Расстояние"
                value={approachData.distanceAU}
                unit="а.е."
                compact
              />
              <ResultCard
                label="Расстояние"
                value={approachData.distanceKm}
                unit="км"
                compact
              />
            </div>

            <div className="action-buttons">
              <Button variant="success" onClick={onSave} size="small">
                Сохранить результаты
              </Button>
              <Button onClick={onExport} size="small">
                Экспорт данных
              </Button>
            </div>
          </div>
        </HolographicPanel>
      )}
    </div>
  );
}

export default CombinedResults;