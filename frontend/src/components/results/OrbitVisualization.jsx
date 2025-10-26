import React from 'react';
import './OrbitVisualization.css';

function OrbitVisualization({ orbitAnimation }) {
  if (orbitAnimation) {
    return (
      <div className="orbit-visualization">
        <div className="animation-container">
          <h4>Анимация орбиты</h4>
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
      </div>
    );
  }

  return (
    <div className="orbit-visualization">
      <div className="visualization-content">
        <div className="icon">🌌</div>
        <p>Визуализация орбиты</p>
        <p className="hint">Здесь будет отображаться расчетная орбита кометы</p>
      </div>
    </div>
  );
}

export default OrbitVisualization;