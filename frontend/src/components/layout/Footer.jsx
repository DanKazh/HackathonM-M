import React from 'react';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <p>Comet Orbit Calculator • Использует Astropy для астрономических расчетов</p>
      <p>
        Для проверки точности: 
        <a 
          href="https://ssd.jpl.nasa.gov/horizons/app.html#/" 
          target="_blank" 
          rel="noopener noreferrer"
        >
          JPL Horizons
        </a>
      </p>
    </footer>
  );
}

export default Footer;
