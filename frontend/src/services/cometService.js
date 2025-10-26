import api from './api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const cometService = {
  // Создать группу наблюдений
  async createObservationGroup(data) {
    const response = await api.post('/observation-groups/', data);
    return response.data;
  },

  // Добавить наблюдение
  async addObservation(observation) {
    const response = await api.post('/observations/', observation);
    return response.data;
  },

  // Получить результаты сближения
  async getCloseApproach(groupId) {
    const response = await api.get(`/close-approaches/${groupId}`);
    return response.data;
  },

  // Получить все группы наблюдений
  async getObservationGroups() {
    const response = await api.get('/observation-groups/');
    return response.data;
  }
};

// Расчет без сохранения (для всех пользователей)
export const calculateOrbit = async (observations) => {
  console.log('Sending observations to /api/calculate:', observations);
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/calculate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        observations: observations.map(obs => [
          obs.date,           // timestamp как строка
          parseFloat(obs.ra), // ra как число  
          parseFloat(obs.dec) // dec как число
        ])
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      console.error('Server error:', errorData);
      return { error: `HTTP error! status: ${response.status}`, details: errorData };
    }

    return await response.json();
  } catch (error) {
    console.error('Network error:', error);
    return { error: 'Network error', details: error.message };
  }
};

// Расчет с сохранением (только для авторизованных пользователей)
export const calculateAndSaveOrbit = async (observations, saveData = {}) => {
  console.log('Sending observations to /api/calculate-and-save:', observations);
  console.log('Save data:', saveData);
  
  try {
    const response = await api.post('/api/calculate-and-save', {
      observations: observations.map(obs => [
        obs.date,           // timestamp как строка
        parseFloat(obs.ra), // ra как число  
        parseFloat(obs.dec) // dec как число
      ]),
      group_name: saveData.groupName || `Расчет от ${new Date().toLocaleString()}`,
      group_description: saveData.groupDescription || '',
      observer_name: saveData.observerName || ''
    });

    return response.data;
  } catch (error) {
    console.error('Calculate and save error:', error);
    return { 
      error: error.response?.data?.detail || error.message || 'Ошибка расчета с сохранением',
      details: error 
    };
  }
};

// Получение расчетов пользователя
export const getUserCalculations = async () => {
  try {
    const response = await api.get('/api/my-calculations');
    return response.data;
  } catch (error) {
    console.error('Get user calculations error:', error);
    throw error;
  }
};