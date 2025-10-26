import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import StatusMessage from '../common/StatusMessage';
import './AuthModal.css';

function LoginModal({ isOpen, onClose, onSwitchToRegister, onLoginSuccess }) {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [localError, setLocalError] = useState('');

  const { login, loading, error, clearError } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError('');
    clearError();

    const result = await login(formData.username, formData.password);
    
    if (result.success) {
      onLoginSuccess();
      onClose();
      // Очищаем форму после успешного входа
      setFormData({
        username: '',
        password: ''
      });
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    if (localError) setLocalError('');
    if (error) clearError();
  };

  const handleClose = () => {
    onClose();
    setLocalError('');
    clearError();
    setFormData({
      username: '',
      password: ''
    });
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>🔑 Вход в систему</h2>
          <button className="close-btn" onClick={handleClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {(localError || error) && (
            <StatusMessage
              message={localError || error}
              type="error"
              onClose={() => {
                setLocalError('');
                clearError();
              }}
            />
          )}

          <div className="form-group">
            <label htmlFor="username">Имя пользователя</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              disabled={loading}
              placeholder="Введите имя пользователя"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              disabled={loading}
              placeholder="Введите пароль"
            />
          </div>

          <button 
            type="submit" 
            className="submit-btn"
            disabled={loading}
          >
            {loading ? 'Вход...' : 'Войти'}
          </button>

          <div className="auth-switch">
            <p>Нет аккаунта? <button type="button" onClick={onSwitchToRegister}>Зарегистрироваться</button></p>
          </div>
        </form>
      </div>
    </div>
  );
}

export default LoginModal;