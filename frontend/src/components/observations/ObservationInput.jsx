import React, { useState } from 'react';
import Card from '../common/Card';
import Tabs from '../common/Tabs';
import ObservationForm from '../forms/ObservationForm';
import ImageUpload from './ImageUpload';
import SkyMap from './SkyMap';
import './ObservationInput.css';

function ObservationInput({ onAddObservation }) {
  const [activeTab, setActiveTab] = useState('manual');

  const tabs = [
    { id: 'manual', label: 'Ручной ввод' },
    { id: 'image', label: 'Изображение' },
    { id: 'sky-map', label: 'Карта неба' }
  ];

  // Обработчик для SkyMap
  const handlePointSelected = (coordinates) => {
    console.log('SkyMap coordinates:', coordinates);
    if (onAddObservation) {
      onAddObservation(coordinates);
    }
  };

  // Обработчик для ImageUpload
  const handleCoordinatesDetected = (coordinates) => {
    console.log('ImageUpload coordinates:', coordinates);
    if (onAddObservation) {
      onAddObservation(coordinates);
    }
  };

  // Обработчик для ObservationForm
  const handleFormSubmit = (observationData) => {
    console.log('Form observationData:', observationData);
    if (onAddObservation) {
      onAddObservation(observationData);
    }
  };

  return (
    <Card title="Ввод наблюдений">
      <Tabs tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />

      {activeTab === 'manual' && <ObservationForm onSubmit={handleFormSubmit} />}
      {activeTab === 'image' && <ImageUpload onCoordinatesDetected={handleCoordinatesDetected} />}
      {activeTab === 'sky-map' && <SkyMap onPointSelected={handlePointSelected} />}
    </Card>
  );
}

export default ObservationInput;