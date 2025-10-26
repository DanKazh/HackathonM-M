import React, { useState, useEffect } from 'react';
import HolographicPanel from '../common/HolographicPanel';
import ResultCard from './ResultCard';
import Button from '../common/Button';
import { formatDate } from '../../utils/formatters';
import OrbitVisualization from './OrbitVisualization';
import EarthMoonSystem from '../common/EarthMoonSystem';
import './CombinedResults.css';

function CombinedResults({ 
  data, 
  loading, 
  onSave, 
  onExport, 
  orbitAnimation,
  approachData 
}) {
  const [animationLoading, setAnimationLoading] = useState(false);

  // Отслеживаем загрузку анимации
  useEffect(() => {
    if (data?.orbit_animation) {
      setAnimationLoading(false);
    } else if (data && !data.orbit_animation) {
      setAnimationLoading(true);
    }
  }, [data?.orbit_animation]);

  // Общая загрузка (расчет орбиты)
  if (loading) {
    return (
      <HolographicPanel 
        title="Визуализация и результаты"
        width="500px"
        height="200px"
        className="combined-results-panel"
      >
          <p>Расчет орбиты...</p>
      
      </HolographicPanel>
    );
  }

  // Загрузка анимации после расчета орбиты
  const showAnimationLoading = animationLoading && data;

  return (
    <div>
      {/* Основная панель с визуализацией и орбитальными элементами */}
      <HolographicPanel 
        title="Визуализация и результаты"
        width="500px"
        height="auto"
        className="combined-results-panel"
      >
        <div className="combined-content">
          {/* Показываем загрузку анимации или саму анимацию */}
          {showAnimationLoading ? (
            <div className="animation-loading">
              <EarthMoonSystem/>
              <p>Генерация анимации...</p>
            </div>
          ) : (
            <OrbitVisualization orbitAnimation={data?.orbit_animation} />
          )}

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