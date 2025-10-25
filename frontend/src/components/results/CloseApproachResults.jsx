import React from 'react';
import Card from '../common/Card';
import ResultCard from './ResultCard';
import Button from '../common/Button';
import { formatDateTime } from '../../utils/formatters';
import './CloseApproachResults.css';

function CloseApproachResults({ data, onSave, onExport }) {
  if (!data) return null;

  return (
    <Card title="Результаты сближения с Землей" className="close-approach-card">
      <div className="results-grid">
        <ResultCard
          label="Дата сближения"
          value={data.date ? formatDateTime(data.date) : '-'}
        />
        <ResultCard
          label="Расстояние"
          value={data.distanceAU}
          unit="а.е."
        />
        <ResultCard
          label="Расстояние"
          value={data.distanceKm}
          unit="км"
        />
      </div>

      <div className="action-buttons">
        <Button variant="success" onClick={onSave}>
          Сохранить результаты
        </Button>
        <Button onClick={onExport}>
          Экспорт данных
        </Button>
      </div>
    </Card>
  );
}

export default CloseApproachResults;
