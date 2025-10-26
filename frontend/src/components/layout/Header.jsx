import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate, useLocation } from 'react-router-dom';
import LoginModal from '../auth/LoginModal';
import RegisterModal from '../auth/RegisterModal';
import './Header.css';

function Header() {
  const { user, isAuthenticated, logout, checkAuth } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  const handleLoginClick = () => {
    setShowLoginModal(true);
  };

  const handleLoginSuccess = () => {
    setShowLoginModal(false);
    checkAuth();
  };

  const handleRegisterSuccess = () => {
    setShowRegisterModal(false);
    checkAuth();
  };

  const handleCloseLogin = () => {
    setShowLoginModal(false);
  };

  const handleCloseRegister = () => {
    setShowRegisterModal(false);
  };

  const switchToRegister = () => {
    setShowLoginModal(false);
    setShowRegisterModal(true);
  };

  const switchToLogin = () => {
    setShowRegisterModal(false);
    setShowLoginModal(true);
  };

  const handleProfileClick = () => {
    navigate('/profile');
  };

  const handleLogout = () => {
    logout(() => navigate('/'));
  };

  return (
    <>
      <header className="header">
        <div className="header-content">
          <div className="header-main">
            <h1>🪐 Comet Orbit Calculator</h1>
            <p>Расчет орбиты комет и предсказание сближений с</p>
          </div>
          
          <div className="header-right">
            {isAuthenticated && user ? (
              <div className="user-info-header">
                <div className="user-avatar-header">
                  {user.username?.charAt(0).toUpperCase() || 'U'}
                </div>
                <div className="user-details-header">
                  <span className="username">{user.username}</span>
                  <div className="user-actions">
                    <button 
                      className="profile-link"
                      onClick={handleProfileClick}
                    >
                      Профиль
                    </button>
                    <span className="separator">|</span>
                    <button 
                      className="logout-link"
                      onClick={handleLogout}
                    >
                      Выйти
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <button 
                className="nav-btn login-btn"
                onClick={handleLoginClick}
              >
                🔑 Войти
              </button>
            )}
          </div>
        </div>

        <div className="header-nav">
          <button 
            className={`nav-btn ${location.pathname === '/' ? 'active' : ''}`}
            onClick={() => navigate('/')}
          >
            🏠 Главная
          </button>
          
          {isAuthenticated && (
            <button 
              className={`nav-btn profile-btn ${location.pathname === '/profile' ? 'active' : ''}`}
              onClick={() => navigate('/profile')}
            >
              👤 Профиль
            </button>
          )}
        </div>
      </header>

      <LoginModal 
        isOpen={showLoginModal}
        onClose={handleCloseLogin}
        onSwitchToRegister={switchToRegister}
        onLoginSuccess={handleLoginSuccess}
      />

      <RegisterModal 
        isOpen={showRegisterModal}
        onClose={handleCloseRegister}
        onSwitchToLogin={switchToLogin}
        onRegisterSuccess={handleRegisterSuccess}
      />
    </>
  );
}

export default Header;