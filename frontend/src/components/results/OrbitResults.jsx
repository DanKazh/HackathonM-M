import React from 'react';
import Card from '../common/Card';
import ResultCard from './ResultCard';
import OrbitVisualization from './OrbitVisualization';
import './OrbitResults.css';

function OrbitResults({ data }) {
  return (
    <Card title="Визуализация и результаты">
      <OrbitVisualization />
      
      {data ? (
        <div className="orbit-results">
          <h3>Орбитальные элементы</h3>
          <div className="results-grid">
            <ResultCard
              label="Большая полуось"
              value={data.semiMajorAxis}
              unit="а.е."
            />
            <ResultCard
              label="Эксцентриситет"
              value={data.eccentricity}
            />
            <ResultCard
              label="Наклонение"
              value={data.inclination}
              unit="°"
            />
          </div>
        </div>
      ) : (
        <div className="empty-results">
          <p>Добавьте наблюдения и нажмите "Рассчитать орбиту"</p>
        </div>
      )}
    </Card>
  );
}

export default OrbitResults;
