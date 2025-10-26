import React from 'react';
import './Card.css';
export default function Card({ title, children }) {
  return <div className="card">{title && <h2>{title}</h2>}<div>{children}</div></div>;
}