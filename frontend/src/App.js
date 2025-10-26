import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AppProvider } from './store/AppContext';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Container from './components/layout/Container';
import MainPage from './pages/MainPage';
import ProfilePage from './pages/ProfilePage';
import CelestialBackground from './components/layout/CelestialBackground';
import './App.css';

function App() {
  return (
    <Router>
      <AppProvider>
        <CelestialBackground />
        <div className="app">
          <Header />
          <Container>
            <Routes>
              <Route path="/" element={<MainPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Routes>
          </Container>
          <Footer />
        </div>
      </AppProvider>
    </Router>
  );
}

export default App;