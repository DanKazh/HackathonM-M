import React from 'react';
import './OrbitVisualization.css';

function OrbitVisualization() {
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
