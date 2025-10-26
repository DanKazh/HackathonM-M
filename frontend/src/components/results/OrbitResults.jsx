import React from 'react';
import Card from '../common/Card';
import ResultCard from './ResultCard';
import OrbitVisualization from './OrbitVisualization';
import './OrbitResults.css';

function OrbitResults({ data, loading }) {
  // Если идет загрузка
  if (loading) {
    return (
      <Card title="Визуализация и результаты">
        <div className="loading-results">
          <div className="loading-spinner"></div>
          <p>Вычисление орбиты...</p>
        </div>
      </Card>
    );
  }


  return (
    <Card title="Визуализация и результаты">
      {/* Передаем данные анимации */}
      <OrbitVisualization orbitAnimation={data?.orbit_animation} />
      
      {data ? (
        <div className="orbit-results">
          <h3>Орбитальные элементы</h3>
          <div className="results-grid">
            <ResultCard
              label="Большая полуось"
              value={data.big_poluos}  // Исправлено на ваше поле
              unit="а.е."
            />
            <ResultCard
              label="Эксцентриситет"
              value={data.eks}  // Исправлено на ваше поле
            />
            <ResultCard
              label="Наклонение"
              value={data.i}  // Исправлено на ваше поле
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