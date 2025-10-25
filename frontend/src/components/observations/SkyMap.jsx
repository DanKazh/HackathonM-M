import React, { useState } from 'react';
import Button from '../common/Button';
import StatusMessage from '../common/StatusMessage';
import './SkyMap.css';

function SkyMap({ onPointSelected }) {
  const [message, setMessage] = useState(null);

  const handleMapClick = () => {
    const mockCoordinates = {
      date: new Date().toISOString().slice(0, 16),
      ra: parseFloat((15 + Math.random() * 3).toFixed(4)),
      dec: parseFloat((20 + Math.random() * 5).toFixed(4))
    };

    onPointSelected(mockCoordinates);
    setMessage({ text: 'Координаты добавлены с карты неба', type: 'success' });
  };

  return (
    <div className="sky-map-container">
      <div className="sky-map">
        <div className="sky-map-content">
          <div className="stars">✨</div>
          <p>Интерактивная карта неба</p>
          <p className="hint">Кликните на карте для выбора координат</p>
        </div>
      </div>

      {message && (
        <StatusMessage
          message={message.text}
          type={message.type}
          onClose={() => setMessage(null)}
        />
      )}

      <Button onClick={handleMapClick}>
        Симулировать выбор точки
      </Button>
    </div>
  );
}

export default SkyMap;
