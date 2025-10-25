import React, { useState } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';
import { validateObservation } from '../../utils/validators';
import './ObservationForm.css';

function ObservationForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().slice(0, 16),
    ra: '',
    dec: ''
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const validation = validateObservation({
      date: formData.date,
      ra: parseFloat(formData.ra),
      dec: parseFloat(formData.dec)
    });

    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    onSubmit({
      date: formData.date,
      ra: parseFloat(formData.ra),
      dec: parseFloat(formData.dec)
    });

    setFormData({
      date: new Date().toISOString().slice(0, 16),
      ra: '',
      dec: ''
    });
    setErrors({});
  };

  return (
    <form onSubmit={handleSubmit} className="observation-form">
      <Input
        label="Дата и время наблюдения (UTC)"
        type="datetime-local"
        name="date"
        value={formData.date}
        onChange={handleChange}
        error={errors.date}
        required
      />

      <Input
        label="Прямое восхождение (градусы)"
        type="number"
        name="ra"
        value={formData.ra}
        onChange={handleChange}
        placeholder="Например: 12.3456"
        step="0.0001"
        min="0"
        max="360"
        error={errors.ra}
        required
      />

      <Input
        label="Склонение (градусы)"
        type="number"
        name="dec"
        value={formData.dec}
        onChange={handleChange}
        placeholder="Например: -45.6789"
        step="0.0001"
        min="-90"
        max="90"
        error={errors.dec}
        required
      />

      <Button type="submit" variant="primary">
        Добавить наблюдение
      </Button>
    </form>
  );
}

export default ObservationForm;
