import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import './UserInfo.css';

function UserInfo({ user, calculationsCount }) {
  const { logout } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className="user-info">
      <div className="user-card">
        <div className="user-avatar">
          {user.username?.charAt(0).toUpperCase() || 'U'}
        </div>
        <div className="user-details">
          <h3>{user.username}</h3>
          <p className="user-id">ID: {user.user_id}</p>
          <div className="user-stats">
            <span className="stat-item">
              <strong>{calculationsCount}</strong> сохраненных вычислений
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserInfo;