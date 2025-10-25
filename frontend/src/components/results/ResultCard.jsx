import React from 'react';
import { formatNumber } from '../../utils/formatters';
import './ResultCard.css';

function ResultCard({ label, value, unit = '' }) {
  return (
    <div className="result-card">
      <div className="result-label">{label}</div>
      <div className="result-value">
        {value}
      </div>
      {unit && <div className="result-unit">{unit}</div>}
    </div>
  );
}

export default ResultCard;
