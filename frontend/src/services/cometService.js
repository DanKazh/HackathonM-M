import api from './api';

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

  // // Рассчитать орбиту
  // async calculateOrbit(groupId) {
  //   const response = await api.post(`/calculate-orbit/${groupId}`);
  //   return response.data;
  // },

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

// services/api.js
const API_BASE_URL = 'http://localhost:8000';

export const calculateOrbit = async (observations) => {
  const response = await fetch(`${API_BASE_URL}/api/calculate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      observations: observations.map(obs => [
        obs.date,
        parseFloat(obs.ra),
        parseFloat(obs.dec)
      ])
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
};
