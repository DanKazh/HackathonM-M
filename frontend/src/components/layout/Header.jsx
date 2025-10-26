import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <h1>🪐 Comet Orbit Calculator</h1>
        <p>Расчет орбиты комет и предсказание сближений с Землей</p>
      </div>
    </header>
  );
}

export default Header;
