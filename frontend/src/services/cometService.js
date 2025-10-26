import api from './api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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