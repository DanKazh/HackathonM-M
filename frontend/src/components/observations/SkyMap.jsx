import React, { useState, useRef, useEffect } from 'react';
import Button from '../common/Button';
import Input from '../common/Input';
import StatusMessage from '../common/StatusMessage';
import './SkyMap.css';

function SkyMap({ onPointSelected }) {
  const [message, setMessage] = useState(null);
  const [selectedCoordinates, setSelectedCoordinates] = useState(null);
  const [clickPosition, setClickPosition] = useState(null);
  
   const [observationDate, setObservationDate] = useState(() => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  });
  
  const [timezone, setTimezone] = useState('UTC+3');
  

  const canvasRef = useRef(null);

  useEffect(() => {
    drawStarField();
  }, []);

  useEffect(() => {
    if (clickPosition) {
      drawStarField();
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      ctx.beginPath();
      ctx.arc(clickPosition.x, clickPosition.y, 6, 0, Math.PI * 2);
      ctx.fillStyle = '#ffa726';
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }, [clickPosition]);

  const drawStarField = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.fillStyle = '#0c1445';
    ctx.fillRect(0, 0, width, height);

    for (let i = 0; i < 300; i++) {
      const x = Math.random() * width;
      const y = Math.random() * height;
      const radius = Math.random() * 1.5;
      const opacity = 0.3 + Math.random() * 0.7;

      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
      ctx.fill();
    }

    ctx.strokeStyle = 'rgba(57, 73, 171, 0.3)';
    ctx.lineWidth = 1;

    for (let i = 0; i <= 360; i += 60) {
      const x = (i / 360) * (width - 60);
      ctx.beginPath();
      ctx.moveTo(x + 30, 0);
      ctx.lineTo(x + 30, height);
      ctx.stroke();

      ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
      ctx.font = '12px Arial';
      ctx.fillText(`${i}°`, x + 35, 15);
    }

    for (let i = 90; i >= -90; i -= 30) {
      const y = ((90 - i) / 180) * (height - 40) + 20;
      ctx.beginPath();
      ctx.moveTo(30, y);
      ctx.lineTo(width - 30, y);
      ctx.stroke();

      ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
      ctx.font = '12px Arial';
      const sign = i >= 0 ? '+' : '';
      ctx.fillText(`${sign}${i}°`, 5, y + 5);
    }
  };

  const handleCanvasClick = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    const ra = ((x - 30) / (canvas.width - 60)) * 360;
    const dec = 90 - ((y - 20) / (canvas.height - 40)) * 180;

    const clampedRa = Math.max(0, Math.min(360, ra));
    const clampedDec = Math.max(-90, Math.min(90, dec));

    setSelectedCoordinates({
      ra: parseFloat(clampedRa.toFixed(4)),
      dec: parseFloat(clampedDec.toFixed(4))
    });
    setClickPosition({ x, y });
    setMessage(null);
  };

  const handleAddObservation = () => {
    if (selectedCoordinates && observationDate) {
      const observation = {
        date: observationDate,
        ra: selectedCoordinates.ra,
        dec: selectedCoordinates.dec,
        timezone: timezone
      };
      
      onPointSelected(observation);
      
      setMessage({ 
        text: `Наблюдение добавлено: RA=${selectedCoordinates.ra.toFixed(2)}°, Dec=${selectedCoordinates.dec.toFixed(2)}° (${timezone})`, 
        type: 'success' 
      });
      
      setTimeout(() => {
        setSelectedCoordinates(null);
        setClickPosition(null);
        drawStarField();
      }, 2000);
    }
  };

  const handleCancel = () => {
    setSelectedCoordinates(null);
    setClickPosition(null);
    drawStarField();
    setMessage(null);
  };

  return (
    <div className="sky-map-container">
      <h4 style={{ color: 'white', marginBottom: '15px', textAlign: 'center' }}>
        Карта неба (кликните для выбора координат)
      </h4>
      
      <canvas
        ref={canvasRef}
        width={800}
        height={450}
        className="sky-map-canvas"
        onClick={handleCanvasClick}
      />

      {selectedCoordinates && (
        <div className="coordinates-preview">
          <p><strong>Выбранные координаты:</strong></p>
          
          <div className="coordinate-display">
            <p>RA: {selectedCoordinates.ra.toFixed(4)}°</p>
            <p>Dec: {selectedCoordinates.dec.toFixed(4)}°</p>
          </div>

          <div className="timezone-select-container">
            <label className="timezone-label">Часовой пояс</label>
            <select 
              className="timezone-select"
              value={timezone}
              onChange={(e) => setTimezone(e.target.value)}
            >
              <option value="UTC">UTC (Всемирное координированное время)</option>
              <option value="UTC+3">UTC+3 (МСК - Москва)</option>
              <option value="UTC+2">UTC+2 (Калининград)</option>
              <option value="UTC+4">UTC+4 (Самара)</option>
              <option value="UTC+5">UTC+5 (Екатеринбург)</option>
              <option value="UTC+6">UTC+6 (Омск)</option>
              <option value="UTC+7">UTC+7 (Красноярск)</option>
              <option value="UTC+8">UTC+8 (Иркутск)</option>
              <option value="UTC+9">UTC+9 (Якутск)</option>
              <option value="UTC+10">UTC+10 (Владивосток)</option>
              <option value="UTC+11">UTC+11 (Магадан)</option>
              <option value="UTC+12">UTC+12 (Камчатка)</option>
              <option value="UTC-5">UTC-5 (EST - Восточное побережье США)</option>
              <option value="UTC-8">UTC-8 (PST - Западное побережье США)</option>
              <option value="UTC+1">UTC+1 (Центральная Европа)</option>
              <option value="UTC+9:30">UTC+9:30 (Австралия)</option>
            </select>
          </div>

          <div className="date-input-container">
            <Input
              label={`Дата и время наблюдения (${timezone})`}
              type="datetime-local"
              value={observationDate}
              onChange={(e) => setObservationDate(e.target.value)}
              required
            />
          </div>
          
          <div className="preview-buttons">
            <Button variant="success" onClick={handleAddObservation}>
              Добавить наблюдение
            </Button>
            <Button variant="secondary" onClick={handleCancel}>
              Отмена
            </Button>
          </div>
        </div>
      )}

      <div className="sky-map-info">
        <p>🌟 Кликните на карте для выбора координат кометы</p>
        <p style={{ fontSize: '12px' }}>
          RA (Прямое восхождение): 0° - 360° (горизонталь)
        </p>
        <p style={{ fontSize: '12px' }}>
          Dec (Склонение): -90° до +90° (вертикаль)
        </p>
      </div>

      {message && (
        <StatusMessage
          message={message.text}
          type={message.type}
          onClose={() => setMessage(null)}
        />
      )}
    </div>
  );
}

export default SkyMap;
