import React from 'react';
import './Input.css';
export default function Input({ label, type = 'text', value, onChange, placeholder, error, required, step, min, max, name }) {
  return <div className="form-group">{label && <label>{label}{required && <span className="required">*</span>}</label>}
  <input type={type} name={name} value={value} onChange={onChange} placeholder={placeholder} className={`form-control ${error ? 'error' : ''}`} step={step} min={min} max={max} required={required} />
  {error && <span className="error-message">{error}</span>}</div>;
}