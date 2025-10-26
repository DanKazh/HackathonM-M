import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Важно для отправки куки
});

// Перехватчик для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Автоматический логаут при 401 ошибке
      console.log('Authentication failed, logging out...');
      // Можно добавить автоматический редирект на логин
    }
    return Promise.reject(error);
  }
);

export default api;