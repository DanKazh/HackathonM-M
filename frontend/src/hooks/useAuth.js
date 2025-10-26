import { useState, useEffect } from 'react';
import api from '../services/api';

export function useAuth() {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const checkAuth = async () => {
    try {
      console.log('🔐 Checking authentication...');
      setLoading(true);
      setError(null);
      
      const response = await api.get('/auth/check');
      console.log('Auth check successful:', response.data);
      
      setUser(response.data);
      setIsAuthenticated(true);
      return true;
    } catch (error) {
      console.log('🔐 Auth check failed:', error.response?.data || error.message);
      setUser(null);
      setIsAuthenticated(false);
      setError(error.response?.data?.detail || 'Authentication check failed');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      console.log('🔐 Attempting login for:', username);
      setLoading(true);
      setError(null);

      const response = await api.post('/auth/login', {
        username,
        password
      });

      console.log('✅ Login successful:', response.data);
      
      // Обновляем данные пользователя
      setUser(response.data);
      setIsAuthenticated(true);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ Login failed:', error.response?.data || error.message);
      const errorMessage = error.response?.data?.detail || 
                          error.message || 
                          'Ошибка входа. Проверьте логин и пароль.';
      setError(errorMessage);
      return { 
        success: false, 
        error: errorMessage 
      };
    } finally {
      setLoading(false);
    }
  };

  const register = async (username, password) => {
    try {
      console.log('🔐 Attempting registration for:', username);
      setLoading(true);
      setError(null);

      const response = await api.post('/auth/register', {
        username,
        password
      });

      console.log('✅ Registration successful:', response.data);
      
      // Обновляем данные пользователя после регистрации
      setUser(response.data);
      setIsAuthenticated(true);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ Registration failed:', error.response?.data || error.message);
      const errorMessage = error.response?.data?.detail || 
                          error.message || 
                          'Ошибка регистрации.';
      setError(errorMessage);
      return { 
        success: false, 
        error: errorMessage 
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = async (navigateCallback = null) => {
    try {
      console.log('🔐 Logging out...');
      await api.post('/auth/logout');
      console.log('✅ Logout successful');
    } catch (error) {
      console.error('❌ Logout error:', error);
    } finally {
      setUser(null);
      setIsAuthenticated(false);
      setError(null);
      
      // Вызываем навигацию, если передан callback
      if (navigateCallback) {
        navigateCallback('/');
      }
    }
  };

  const clearError = () => {
    setError(null);
  };

  useEffect(() => {
    checkAuth();
  }, []);

  return {
    user,
    isAuthenticated,
    loading,
    error,
    login,
    register,
    logout,
    checkAuth,
    clearError
  };
}