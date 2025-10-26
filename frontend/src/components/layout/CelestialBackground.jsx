import React from 'react';
import styles from './CelestialBackground.module.css';

const CelestialBackground = () => {
  // Создаем звезды
  const stars = Array.from({ length: 150 }, (_, i) => ({
    id: i,
    left: Math.random() * 100,
    top: Math.random() * 100,
    size: Math.random() * 2 + 1,
    delay: Math.random() * 5,
    duration: Math.random() * 3 + 2
  }));

  // Создаем кометы с разными траекториями и временем появления
  const comets = [
    {
      id: 1,
      startX: -10,
      startY: 15,
      endX: 110,
      endY: 85,
      duration: 4,
      delay: 0,
      size: 3,
      color: '#4fc3f7'
    },
    {
      id: 2,
      startX: 120,
      startY: 5,
      endX: -20,
      endY: 95,
      duration: 5,
      delay: 2,
      size: 2,
      color: '#e1f5fe'
    },
    {
      id: 3,
      startX: 50,
      startY: -10,
      endX: 60,
      endY: 110,
      duration: 3,
      delay: 1,
      size: 4,
      color: '#b3e5fc'
    },
    {
      id: 4,
      startX: -5,
      startY: 80,
      endX: 105,
      endY: 10,
      duration: 6,
      delay: 3,
      size: 2.5,
      color: '#81d4fa'
    },
    {
      id: 5,
      startX: 90,
      startY: -5,
      endX: 10,
      endY: 105,
      duration: 4.5,
      delay: 4,
      size: 3.5,
      color: '#29b6f6'
    }
  ];

  return (
    <div className={styles.background}>
      {/* Градиентный фон небосвода */}
      <div className={styles.skyGradient}></div>
      
      {/* Звезды */}
      <div className={styles.starsContainer}>
        {stars.map(star => (
          <div
            key={`star-${star.id}`}
            className={styles.star}
            style={{
              left: `${star.left}%`,
              top: `${star.top}%`,
              width: `${star.size}px`,
              height: `${star.size}px`,
              animationDelay: `${star.delay}s`,
              animationDuration: `${star.duration}s`
            }}
          />
        ))}
      </div>

      {/* Кометы */}
      <div className={styles.cometsContainer}>
        {comets.map(comet => (
          <div
            key={`comet-${comet.id}`}
            className={styles.comet}
            style={{
              '--startX': `${comet.startX}%`,
              '--startY': `${comet.startY}%`,
              '--endX': `${comet.endX}%`,
              '--endY': `${comet.endY}%`,
              '--duration': `${comet.duration}s`,
              '--delay': `${comet.delay}s`,
              '--size': `${comet.size}px`,
              '--color': comet.color
            }}
          >
            <div className={styles.cometHead}></div>
            <div className={styles.cometTail}></div>
          </div>
        ))}
      </div>

      {/* Туманности */}
      <div className={styles.nebula1}></div>
      <div className={styles.nebula2}></div>
      <div className={styles.nebula3}></div>
    </div>
  );
};

export default CelestialBackground;