import React from 'react';
import './CalculationHistory.css';

function CalculationHistory({ calculations, loading, onDeleteCalculation, onRefresh }) {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('ru-RU', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDistance = (distance) => {
    return new Intl.NumberFormat('ru-RU', {
      minimumFractionDigits: 3,
      maximumFractionDigits: 6
    }).format(distance);
  };

  if (loading) {
    return (
      <div className="calculation-history loading">
        <div className="loading-spinner"></div>
        <p>Загрузка вычислений...</p>
      </div>
    );
  }

  if (calculations.length === 0) {
    return (
      <div className="calculation-history empty">
        <div className="empty-state">
          <h3>📊 Нет сохраненных вычислений</h3>
          <p>Выполните расчеты на главной странице чтобы они появились здесь</p>
          <button onClick={onRefresh} className="retry-btn">
            🔄 Обновить
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="calculation-history">
      <div className="calculations-stats">
        Найдено вычислений: <strong>{calculations.length}</strong>
      </div>
      
      <div className="calculations-grid">
        {calculations.map((calculation) => (
          <div key={calculation.calculation_id} className="calculation-card">
            <div className="calculation-header">
              <h4>{calculation.group_name || 'Без названия'}</h4>
              <button
                className="delete-btn"
                onClick={() => onDeleteCalculation(calculation.calculation_id)}
                title="Удалить вычисление"
              >
                ×
              </button>
            </div>
            
            {calculation.group_description && (
              <p className="calculation-description">
                {calculation.group_description}
              </p>
            )}
            
            <div className="calculation-details">
              <div className="detail-row">
                <span className="label">Мин. расстояние:</span>
                <span className="value">
                  {formatDistance(calculation.min_distance_au)} AU
                </span>
              </div>
              <div className="detail-row">
                <span className="label">Мин. расстояние:</span>
                <span className="value">
                  {formatDistance(calculation.min_distance_km)} км
                </span>
              </div>
              <div className="detail-row">
                <span className="label">Время сближения:</span>
                <span className="value">
                  {formatDate(calculation.closest_approach_time)}
                </span>
              </div>
              <div className="detail-row">
                <span className="label">Наблюдений:</span>
                <span className="value">{calculation.observation_count}</span>
              </div>
              <div className="detail-row">
                <span className="label">Сохранено:</span>
                <span className="value">
                  {formatDate(calculation.saved_at)}
                </span>
              </div>
              {calculation.observer_name && (
                <div className="detail-row">
                  <span className="label">Наблюдатель:</span>
                  <span className="value">{calculation.observer_name}</span>
                </div>
              )}
            </div>
            
          </div>
        ))}
      </div>
    </div>
  );
}

export default CalculationHistory;