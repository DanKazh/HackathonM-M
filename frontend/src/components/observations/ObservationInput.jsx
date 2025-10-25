import React, { useState } from 'react';
import { useObservations } from '../../hooks/useObservations';
import Card from '../common/Card';
import Tabs from '../common/Tabs';
import ObservationForm from '../forms/ObservationForm';
import ImageUpload from './ImageUpload';
import SkyMap from './SkyMap';
import './ObservationInput.css';

function ObservationInput() {
  const [activeTab, setActiveTab] = useState('manual');
  const { addObservation } = useObservations();

  const tabs = [
    { id: 'manual', label: 'Ручной ввод' },
    { id: 'image', label: 'Изображение' },
    { id: 'sky-map', label: 'Карта неба' }
  ];

  return (
    <Card title="Ввод наблюдений">
      <Tabs tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />

      {activeTab === 'manual' && <ObservationForm onSubmit={addObservation} />}
      {activeTab === 'image' && <ImageUpload onCoordinatesDetected={addObservation} />}
      {activeTab === 'sky-map' && <SkyMap onPointSelected={addObservation} />}
    </Card>
  );
}

export default ObservationInput;
