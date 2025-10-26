const API_BASE_URL = 'http://localhost:8000';

// Базовый клиент API с улучшенной обработкой ошибок
export const api = {
  async get(url) {
    console.log(`📡 GET ${API_BASE_URL}${url}`);
    
    try {
      const response = await fetch(`${API_BASE_URL}${url}`);
      console.log(`📨 GET Response status: ${response.status}`);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ GET Error ${response.status}:`, errorText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log(`✅ GET Success:`, data);
      return data;
    } catch (error) {
      console.error(`💥 GET Request failed:`, error);
      throw error;
    }
  },

  async post(url, data) {
    console.log(`📡 POST ${API_BASE_URL}${url}`, data);
    
    try {
      const response = await fetch(`${API_BASE_URL}${url}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      
      console.log(`📨 POST Response status: ${response.status}`);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ POST Error ${response.status}:`, errorText);
        
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.detail || errorData.message || errorText;
        } catch {
          errorMessage = errorText || `HTTP error! status: ${response.status}`;
        }
        
        throw new Error(errorMessage);
      }
      
      const result = await response.json();
      console.log(`✅ POST Success:`, result);
      return result;
    } catch (error) {
      console.error(`💥 POST Request failed:`, error);
      throw error;
    }
  }
};

export default api;