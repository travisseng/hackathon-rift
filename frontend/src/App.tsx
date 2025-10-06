import CardDeck from './components/CardDeck';
import { mockPrimaryDeck, mockSecondaryDeck } from './data/mockCards';
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-lol-dark via-lol-dark-light to-lol-dark-lighter">
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-5 bg-[url('https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt4b6e2f1fb5491f2a/6216f9c00af6eb21c0e67de5/LoL_Map_Summoners_Rift.jpg')] bg-cover bg-center" />

      {/* Content */}
      <div className="relative z-10">
        <CardDeck
          primaryDeck={mockPrimaryDeck}
          secondaryDeck={mockSecondaryDeck}
        />
      </div>

      {/* Footer */}
      <div className="relative z-10 text-center pb-12 text-gray-400 text-sm">
        <p>League of Legends AI Analytics - Mockup Demo</p>
        <p className="mt-2">Built for the League of Legends AI Hackathon 🎮</p>
      </div>
    </div>
  );
}

export default App;
