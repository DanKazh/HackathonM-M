import React from 'react';
import HolographicPanel from '../common/HolographicPanel'; // Или правильный путь
import './OrbitVisualization.css';

function OrbitVisualization({ orbitAnimation }) {
  if (orbitAnimation) {
    return (
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
    );
  }

  // Если анимации нет
  return (
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
  );
}

export default OrbitVisualization;