import React from 'react';
import styles from './HolographicPanel.module.css';

const HolographicPanel = ({ 
  title, 
  children, 
  width = "400px",
  height = "auto",
  className = "" 
}) => {
  return (
    <div 
      className={`${styles.holographicPanel} ${className}`}
      style={{ width, height }}
    >
      {/* Голографическое свечение */}
      <div className={styles.holographicGlow}></div>
      
      {/* Основной контент */}
      <div className={styles.panelContent}>
        {/* Заголовок с голографическим эффектом */}
        {title && (
          <div className={styles.panelHeader}>
            <h3 className={styles.panelTitle}>{title}</h3>
            <div className={styles.titleGlow}></div>
          </div>
        )}
        
        {/* Контент панели */}
        <div className={styles.panelBody}>
          {children}
        </div>
      </div>
      
    
      
      {/* Частицы голографического поля */}
      <div className={styles.holoParticles}>
        {Array.from({ length: 15 }).map((_, i) => (
          <div
            key={i}
            className={styles.particle}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${Math.random() * 2 + 1}s`
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default HolographicPanel;