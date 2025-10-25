import React from 'react';
import './Loading.css';
export default function Loading({ message = 'Загрузка...' }) {
  return <div className="loading"><div className="spinner"></div><p>{message}</p></div>;
}