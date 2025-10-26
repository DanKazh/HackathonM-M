import React, { useEffect } from 'react';
import './StatusMessage.css';
export default function StatusMessage({ message, type, onClose, autoClose = 5000 }) {
  useEffect(() => { if (autoClose && onClose) { const timer = setTimeout(onClose, autoClose); return () => clearTimeout(timer); } }, [autoClose, onClose]);
  if (!message) return null;
  return <div className={`status-message status-${type}`}><span>{message}</span>{onClose && <button className="close-btn" onClick={onClose}>×</button>}</div>;
}