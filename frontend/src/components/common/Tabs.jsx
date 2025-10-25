import React from 'react';
import './Tabs.css';
export default function Tabs({ tabs, activeTab, onTabChange }) {
  return <div className="tab-navigation">{tabs.map(tab => <button key={tab.id} className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`} onClick={() => onTabChange(tab.id)}>{tab.label}</button>)}</div>;
}