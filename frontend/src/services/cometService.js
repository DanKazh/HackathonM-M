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

  // Рассчитать орбиту
  async calculateOrbit(groupId) {
    const response = await api.post(`/calculate-orbit/${groupId}`);
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
