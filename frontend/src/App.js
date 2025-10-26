import React from 'react';
import { AppProvider } from './store/AppContext';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Container from './components/layout/Container';
import MainPage from './pages/MainPage';
import CelestialBackground from './components/layout/CelestialBackground';
import './App.css';

function App() {
  return (
    
    <AppProvider>
           <CelestialBackground />
      <div>
        <Header />
        <Container>
          <MainPage />
        </Container>
        <Footer />
      </div>
    </AppProvider>
  );
}

export default App;
