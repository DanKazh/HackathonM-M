import React, { useState } from 'react';
import HolographicPanel from '../common/HolographicPanel'; // Импортируем новый компонент
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
    <HolographicPanel 
      title="Ввод наблюдений"
      width="600px" // Можете настроить по необходимости
      height="auto"
      className="observation-holographic-panel" // Дополнительный класс для кастомных стилей
    >
      <Tabs tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />

      {activeTab === 'manual' && <ObservationForm onSubmit={handleFormSubmit} />}
      {activeTab === 'image' && <ImageUpload onCoordinatesDetected={handleCoordinatesDetected} />}
      {activeTab === 'sky-map' && <SkyMap onPointSelected={handlePointSelected} />}
    </HolographicPanel>
  );
}

export default ObservationInput;