import React from 'react';
import { formatNumber } from '../../utils/formatters';
import './ResultCard.css';

function ResultCard({ 
  label, 
  value, 
  unit = '', 
  compact = false,
  align = 'center',
  valueSize = 'normal',
  className = ''
}) {
  const formattedValue = typeof value === 'number' ? formatNumber(value) : value;

  return (
    <div className={`result-card ${compact ? 'compact' : ''} ${className}`} data-align={align}>
      <div className="result-label">{label}</div>
      <div className={`result-value ${valueSize}`}>
        {formattedValue}
        {unit && <span className="result-unit">{unit}</span>}
      </div>
    </div>
  );
}

export default ResultCard;