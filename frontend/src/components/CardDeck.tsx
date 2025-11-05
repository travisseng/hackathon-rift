import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import StatCard from './StatCard';
import { CardDeck as CardDeckType, StatCard as StatCardType } from '../types/stats';

interface CardDeckProps {
  primaryDeck: CardDeckType;
  secondaryDeck: CardDeckType;
}

export default function CardDeck({ primaryDeck, secondaryDeck }: CardDeckProps) {
  const [cards, setCards] = useState<StatCardType[]>(primaryDeck.cards);
  const [rerollingIndex, setRerollingIndex] = useState<number | null>(null);
  const [availableCards] = useState<StatCardType[]>([...primaryDeck.cards, ...secondaryDeck.cards]);

  const handleIndividualReroll = (index: number) => {
    setRerollingIndex(index);

    // Quick reroll animation
    setTimeout(() => {
      const newCards = [...cards];
      // Get a random card from available cards that's not currently displayed
      const availableAlternatives = availableCards.filter(
        (card) => !cards.some((displayedCard) => displayedCard.id === card.id)
      );

      if (availableAlternatives.length > 0) {
        const randomCard = availableAlternatives[Math.floor(Math.random() * availableAlternatives.length)];
        newCards[index] = randomCard;
        setCards(newCards);
      }

      setRerollingIndex(null);
    }, 300);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-12 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* TFT-style header */}
      <motion.div
        className="text-center mb-16"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <h1 className="text-6xl font-black text-white mb-4 drop-shadow-2xl tracking-tight">
          Choose One
        </h1>
        <p className="text-2xl text-gray-300 font-medium">
          Your Year in League
        </p>
      </motion.div>

      {/* TFT Augment-style card selection */}
      <div className="flex flex-col lg:flex-row items-start justify-center gap-12">
        <AnimatePresence mode="wait">
          {cards.map((card, index) => (
            <div key={index} className="flex items-center justify-center">
              <StatCard
                card={card}
                onReroll={() => handleIndividualReroll(index)}
                isRerolling={rerollingIndex === index}
              />
            </div>
          ))}
        </AnimatePresence>
      </div>

      {/* Subtle background effects */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>
    </div>
  );
}
