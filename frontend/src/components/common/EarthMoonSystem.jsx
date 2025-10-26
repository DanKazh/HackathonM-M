import React from 'react';
import styles from './EarthMoonSystem.module.css';

const EarthMoonSystem = () => {
  // Создаем массив звезд для JSX рендеринга
  const stars = Array.from({ length: 50 }, (_, i) => ({
    id: i,
    left: Math.random() * 100,
    top: Math.random() * 100,
    delay: Math.random() * 3,
    size: Math.random() * 2 + 1
  }));

  return (
    <div className={styles.container}>
      <div className={styles.solarSystem}>
        
        {/* Орбита Луны */}
        <div className={styles.moonOrbit}>
          {/* Земля в центре */}
          <div className={styles.earth}>
            <div className={styles.earthGlow}></div>
            <div className={styles.earthSurface}>
              <div className={styles.continent1}></div>
              <div className={styles.continent2}></div>
              <div className={styles.continent3}></div>
            </div>
            <div className={styles.clouds}>
              <div className={styles.cloud1}></div>
              <div className={styles.cloud2}></div>
              <div className={styles.cloud3}></div>
            </div>
          </div>
          
          {/* Луна на орбите */}
          <div className={styles.moon}>
            <div className={styles.moonSurface}>
              <div className={styles.crater1}></div>
              <div className={styles.crater2}></div>
              <div className={styles.crater3}></div>
            </div>
          </div>
        </div>

        {/* Звездный фон через JSX */}
        <div className={styles.stars}>
          {stars.map(star => (
            <div
              key={star.id}
              className={styles.star}
              style={{
                left: `${star.left}%`,
                top: `${star.top}%`,
                width: `${star.size}px`,
                height: `${star.size}px`,
                animationDelay: `${star.delay}s`
              }}
            />
          ))}
        </div>

      </div>
    </div>
  );
};

export default EarthMoonSystem;