import { useState } from 'react';
import { motion } from 'framer-motion';
import { RefreshCw } from 'lucide-react';
import StatCard from './StatCard';
import { CardDeck as CardDeckType } from '../types/stats';

interface CardDeckProps {
  primaryDeck: CardDeckType;
  secondaryDeck: CardDeckType;
}

export default function CardDeck({ primaryDeck, secondaryDeck }: CardDeckProps) {
  const [showingPrimary, setShowingPrimary] = useState(true);
  const [isFlipping, setIsFlipping] = useState(false);

  const currentDeck = showingPrimary ? primaryDeck : secondaryDeck;

  const handleReroll = () => {
    setIsFlipping(true);
    setTimeout(() => {
      setShowingPrimary(!showingPrimary);
      setIsFlipping(false);
    }, 300);
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-12">
      {/* Header */}
      <motion.div
        className="text-center mb-12"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-5xl font-black text-white mb-4 drop-shadow-lg">
          Your Year in League
        </h1>
        <p className="text-xl text-gray-300">
          {showingPrimary ? 'Your Top Stats' : 'More Insights'}
        </p>
      </motion.div>

      {/* Card Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12"
        key={currentDeck.deck_type}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        {currentDeck.cards.map((card, index) => (
          <motion.div
            key={card.id}
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.5 }}
          >
            <StatCard
              card={card}
              isFlipped={isFlipping}
              onShare={() => console.log('Share card:', card.id)}
            />
          </motion.div>
        ))}
      </motion.div>

      {/* Reroll Button */}
      <motion.div
        className="flex justify-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <button
          onClick={handleReroll}
          disabled={isFlipping}
          className="group relative px-8 py-4 bg-gradient-to-r from-lol-blue to-lol-blue-dark text-white font-bold text-lg rounded-lg hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
        >
          <span className="flex items-center gap-3">
            <RefreshCw
              size={24}
              className={`transition-transform ${isFlipping ? 'animate-spin' : 'group-hover:rotate-180'}`}
            />
            {showingPrimary ? 'Show More Stats' : 'Back to Top Stats'}
          </span>
        </button>
      </motion.div>

      {/* Indicator */}
      <div className="flex justify-center gap-2 mt-8">
        <div
          className={`w-3 h-3 rounded-full transition-all ${
            showingPrimary ? 'bg-lol-gold w-8' : 'bg-gray-500'
          }`}
        />
        <div
          className={`w-3 h-3 rounded-full transition-all ${
            !showingPrimary ? 'bg-lol-gold w-8' : 'bg-gray-500'
          }`}
        />
      </div>
    </div>
  );
}
