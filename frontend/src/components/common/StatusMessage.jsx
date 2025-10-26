import React from 'react';
import './StatusMessage.css';

function StatusMessage({ message, type = 'info', onClose }) {
  return (
    <div className={`status-message status-${type}`}>
      <span className="status-text">{message}</span>
      {onClose && (
        <button className="status-close" onClick={onClose}>×</button>
      )}
    </div>
  );
}

export default StatusMessage;