import { BrowserRouter, Routes, Route } from 'react-router-dom';
import NavBar from './components/shared/NavBar';
import RecapPage from './pages/RecapPage';
import ProgressionPage from './pages/ProgressionPage';
import CoachingPage from './pages/CoachingPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gradient-to-br from-lol-dark via-lol-dark-light to-lol-dark-lighter">
        {/* Background pattern */}
        <div className="fixed inset-0 opacity-5 bg-[url('https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt4b6e2f1fb5491f2a/6216f9c00af6eb21c0e67de5/LoL_Map_Summoners_Rift.jpg')] bg-cover bg-center" />

        {/* Navigation */}
        <NavBar />

        {/* Content */}
        <div className="relative z-10">
          <Routes>
            <Route path="/" element={<RecapPage />} />
            <Route path="/progression" element={<ProgressionPage />} />
            <Route path="/coaching" element={<CoachingPage />} />
          </Routes>
        </div>

        {/* Footer */}
        <div className="relative z-10 text-center py-8 text-gray-400 text-sm border-t border-lol-gold/10 mt-12">
          <p>League of Legends AI Analytics - Full Demo</p>
          <p className="mt-2">Built for the League of Legends AI Hackathon 🎮</p>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
