import React from 'react';
import { useProfile } from '../../hooks/useProfile';
import { useAuth } from '../../hooks/useAuth';
import StatusMessage from '../common/StatusMessage';
import CalculationHistory from './CalculationHistory';
import UserInfo from './UserInfo';
import './UserProfile.css';

function UserProfile() {
  const { 
    userCalculations, 
    loading, 
    error, 
    fetchUserCalculations,
    deleteCalculation 
  } = useProfile();

  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return (
      <div className="user-profile">
        <div className="auth-required">
          <h2>🔒 Требуется авторизация</h2>
          <p>Для просмотра истории вычислений необходимо войти в систему</p>
        </div>
      </div>
    );
  }

  const handleRetry = () => {
    fetchUserCalculations();
  };

  return (
    <div className="user-profile">
      <div className="profile-header">
        <h1>👤 Профиль пользователя</h1>
        <p>Управление вашими вычислениями и настройками</p>
      </div>

      <UserInfo user={user} calculationsCount={userCalculations.length} />

      <div className="calculations-section">
        <div className="section-header">
          <h2>📊 История вычислений</h2>
        </div>

        {error && (
          <StatusMessage
            message={error}
            type="error"
            onClose={() => {}}
          />
        )}

        <CalculationHistory
          calculations={userCalculations}
          loading={loading}
          onDeleteCalculation={deleteCalculation}
          onRefresh={fetchUserCalculations}
        />
      </div>
    </div>
  );
}

export default UserProfile;