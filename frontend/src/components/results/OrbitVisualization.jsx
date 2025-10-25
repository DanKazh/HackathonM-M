import React from 'react';
import './OrbitVisualization.css';

function OrbitVisualization({ orbitData }) {
  if (!orbitData) {
    return (
      <div className="orbit-visualization">
        <h3>Результаты расчёта орбиты</h3>
        <div className="no-data">
          <p>📊 Добавьте минимум 5 наблюдений и нажмите "Рассчитать орбиту"</p>
        </div>
      </div>
    );
  }

  const {
    semi_major_axis,
    eccentricity,
    inclination,
    perihelion_distance,
    aphelion_distance,
    orbital_period,
    approach_date,
    min_distance_to_earth,
    velocity_at_approach
  } = orbitData;

  return (
    <div className="orbit-visualization">
      <h3>Результаты расчёта орбиты кометы</h3>

      <div className="orbit-grid">
        {/* Орбитальные элементы */}
        <div className="orbit-card">
          <h4>📐 Орбитальные элементы</h4>
          <div className="param-list">
            <div className="param-row">
              <span className="param-label">Большая полуось (a):</span>
              <span className="param-value">{semi_major_axis?.toFixed(4)} а.е.</span>
            </div>
            <div className="param-row">
              <span className="param-label">Эксцентриситет (e):</span>
              <span className="param-value">{eccentricity?.toFixed(6)}</span>
            </div>
            <div className="param-row">
              <span className="param-label">Наклонение (i):</span>
              <span className="param-value">{inclination?.toFixed(2)}°</span>
            </div>
          </div>
        </div>

        {/* Расстояния */}
        <div className="orbit-card">
          <h4>📏 Расстояния</h4>
          <div className="param-list">
            <div className="param-row">
              <span className="param-label">Перигелий (q):</span>
              <span className="param-value">{perihelion_distance?.toFixed(4)} а.е.</span>
            </div>
            <div className="param-row">
              <span className="param-label">Афелий (Q):</span>
              <span className="param-value">{aphelion_distance?.toFixed(4)} а.е.</span>
            </div>
            <div className="param-row">
              <span className="param-label">Период обращения:</span>
              <span className="param-value">{orbital_period?.toFixed(2)} лет</span>
            </div>
          </div>
        </div>

        {/* Сближение с Землёй */}
        <div className="orbit-card highlight">
          <h4>🌍 Сближение с Землёй</h4>
          <div className="param-list">
            <div className="param-row">
              <span className="param-label">Дата сближения:</span>
              <span className="param-value date">
                {approach_date ? new Date(approach_date).toLocaleDateString('ru-RU') : '—'}
              </span>
            </div>
            <div className="param-row">
              <span className="param-label">Минимальное расстояние:</span>
              <span className="param-value distance">
                {min_distance_to_earth?.toFixed(6)} а.е.
              </span>
            </div>
            <div className="param-row">
              <span className="param-label">Скорость при сближении:</span>
              <span className="param-value">{velocity_at_approach?.toFixed(2)} км/с</span>
            </div>
          </div>
        </div>

        {/* Визуальная схема орбиты */}
        <div className="orbit-card full-width">
          <h4>🪐 Схема орбиты</h4>
          <div className="orbit-diagram">
            <svg viewBox="0 0 400 300" className="orbit-svg">
              {/* Солнце */}
              <circle cx="200" cy="150" r="15" fill="#FDB813" />
              <text x="200" y="185" textAnchor="middle" fill="white" fontSize="12">☉ Солнце</text>
              
              {/* Орбита Земли */}
              <ellipse 
                cx="200" 
                cy="150" 
                rx="100" 
                ry="100" 
                fill="none" 
                stroke="#4A90E2" 
                strokeWidth="1"
                strokeDasharray="3,3"
              />
              <circle cx="280" cy="150" r="8" fill="#4A90E2" />
              <text x="280" y="168" textAnchor="middle" fill="#4A90E2" fontSize="10">🌍 Земля</text>
              
              {/* Орбита кометы */}
              <ellipse 
                cx="200" 
                cy="150" 
                rx={Math.min(150, 100 * (1 + eccentricity))} 
                ry={Math.min(120, 100 * Math.sqrt(1 - eccentricity * eccentricity))} 
                fill="none" 
                stroke="#E74C3C" 
                strokeWidth="2"
              />
              
              {/* Комета */}
              <circle 
                cx={200 + Math.min(150, 100 * (1 + eccentricity))} 
                cy="150" 
                r="6" 
                fill="#E74C3C" 
              />
              <text 
                x={200 + Math.min(150, 100 * (1 + eccentricity))} 
                y="168" 
                textAnchor="middle" 
                fill="#E74C3C" 
                fontSize="10"
              >
                ☄️ Комета
              </text>
            </svg>
            <p className="diagram-note">
              * Схема упрощена. Красная линия — орбита кометы, синяя пунктирная — орбита Земли.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default OrbitVisualization;
