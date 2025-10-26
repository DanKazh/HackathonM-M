import api from './api';

export const cometService = {
  // БЫСТРЫЙ расчет орбиты (без анимации)
  async calculateOrbit(observations) {
    console.log('🚀 cometService.calculateOrbit called with:', observations);
    
    try {
      const formattedObservations = this.formatObservations(observations);
      console.log('📤 Formatted observations for API:', formattedObservations);

      const response = await api.post('/api/calculate-orbit', {
        observations: formattedObservations
      });
      
      console.log('✅ cometService.calculateOrbit response:', response);
      
      if (response && response.data) {
        return response.data;
      } else if (response) {
        return response;
      } else {
        throw new Error('Empty response from server');
      }
    } catch (error) {
      console.error('❌ cometService.calculateOrbit error:', error);
      throw error;
    }
  },

  // МЕДЛЕННАЯ генерация анимации орбиты
  // МЕДЛЕННАЯ генерация анимации орбиты
async generateOrbitAnimation(orbitData, originalObservations) {
  console.log('🎬 cometService.generateOrbitAnimation called with orbitData:', orbitData);
  
  try {
    // Форматируем наблюдения для отправки
    const formattedObservations = this.formatObservations(originalObservations);
    
    // Подготавливаем только нужные орбитальные параметры
    const orbitParams = {
      big_poluos: orbitData.big_poluos,
      eks: orbitData.eks,
      i: orbitData.i,
      closest_approach_time: orbitData.closest_approach_time,
      min_distance_au: orbitData.min_distance_au,
      min_distance_km: orbitData.min_distance_km
    };
    
    console.log('📤 Sending orbit params for animation:', orbitParams);
    console.log('📤 Sending observations for animation:', formattedObservations);

    // Отправляем только орбитальные параметры и наблюдения
    const response = await api.post('/api/generate-animation', {
      orbit_data: orbitParams,
      observations: formattedObservations
    });
    
    console.log('✅ cometService.generateOrbitAnimation response:', response);
    
    if (response && response.data) {
      return response.data;
    } else if (response) {
      return response;
    } else {
      throw new Error('Empty response from server');
    }
  } catch (error) {
    console.error('❌ cometService.generateOrbitAnimation error:', error);
    throw error;
  }
},

  // Вспомогательный метод для форматирования наблюдений
  formatObservations(observations) {
    return observations.map(obs => {
      if (Array.isArray(obs) && obs.length === 3) {
        return obs;
      }
      else if (obs.date && obs.ra !== undefined && obs.dec !== undefined) {
        return [obs.date, obs.ra, obs.dec];
      }
      else if (obs.timestamp && obs.ra_degrees !== undefined && obs.dec_degrees !== undefined) {
        return [obs.timestamp, obs.ra_degrees, obs.dec_degrees];
      }
      else {
        console.error('❌ Unknown observation format:', obs);
        throw new Error(`Unknown observation format: ${JSON.stringify(obs)}`);
      }
    });
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