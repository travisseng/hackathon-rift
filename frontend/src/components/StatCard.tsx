import { motion } from 'framer-motion';
import { StatCard as StatCardType } from '../types/stats';
import { RefreshCw } from 'lucide-react';

interface StatCardProps {
  card: StatCardType;
  onReroll?: () => void;
  isRerolling?: boolean;
}

export default function StatCard({ card, onReroll, isRerolling = false }: StatCardProps) {
  // TFT-style tier colors and effects
  const getTierStyle = () => {
    switch (card.rarity) {
      case 'legendary': // Prismatic
        return {
          border: 'border-4 border-transparent bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 p-[4px]',
          glow: 'shadow-2xl shadow-purple-500/50 animate-pulse',
          innerBg: 'bg-gradient-to-br from-purple-900/90 to-pink-900/90',
          shimmer: true,
        };
      case 'epic': // Gold
        return {
          border: 'border-4 border-yellow-400',
          glow: 'shadow-xl shadow-yellow-500/50',
          innerBg: 'bg-gradient-to-br from-yellow-900/80 to-orange-900/80',
          shimmer: false,
        };
      case 'rare': // Silver
        return {
          border: 'border-4 border-gray-300',
          glow: 'shadow-lg shadow-gray-400/40',
          innerBg: 'bg-gradient-to-br from-gray-800/80 to-slate-800/80',
          shimmer: false,
        };
      default: // Common
        return {
          border: 'border-2 border-gray-600',
          glow: '',
          innerBg: 'bg-gradient-to-br from-gray-900/80 to-gray-800/80',
          shimmer: false,
        };
    }
  };

  const tierStyle = getTierStyle();

  return (
    <div className="flex flex-col items-center gap-4">
      {/* Card - AnimatePresence for smooth transitions */}
      <motion.div
        key={card.id}
        className="relative w-80"
        initial={{ opacity: 0, scale: 0.9, rotateY: -90 }}
        animate={{ opacity: 1, scale: 1, rotateY: 0 }}
        exit={{ opacity: 0, scale: 0.9, rotateY: 90 }}
        transition={{ duration: 0.4, ease: 'easeInOut' }}
      >
        {/* Outer border with tier styling */}
        <div className={`relative rounded-2xl ${tierStyle.border} ${tierStyle.glow}`}>
          {/* Inner card content - Fixed height */}
          <div className={`relative rounded-xl ${tierStyle.innerBg} overflow-hidden`} style={{ minHeight: '450px' }}>
            {/* Shimmer effect for prismatic */}
            {tierStyle.shimmer && (
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer" />
            )}

            {/* Artwork icon at top */}
            <div className="flex justify-center pt-6 pb-4">
              <div className="w-20 h-20 rounded-full bg-black/40 flex items-center justify-center border-2 border-white/20">
                <img
                  src={card.theme.artwork_url}
                  alt=""
                  className="w-16 h-16 rounded-full object-cover"
                  onError={(e) => {
                    e.currentTarget.src = 'https://ddragon.leagueoflegends.com/cdn/14.1.1/img/champion/Ahri.png';
                  }}
                />
              </div>
            </div>

            {/* Card content */}
            <div className="px-6 pb-6 text-center flex flex-col" style={{ minHeight: '330px' }}>
              {/* Title */}
              <h3 className="text-white font-bold text-lg mb-3 leading-tight min-h-[56px] flex items-center justify-center">
                {card.title}
              </h3>

              {/* Main stat value */}
              <div className="mb-4 flex-grow flex items-center justify-center">
                <p className="text-3xl font-black text-white drop-shadow-lg">
                  {card.value}
                </p>
              </div>

              {/* Description */}
              <div className="min-h-[60px] flex items-center justify-center">
                {card.subtitle && (
                  <p className="text-gray-300 text-sm leading-relaxed px-2">
                    {card.subtitle}
                  </p>
                )}
              </div>

              {/* Tier indicator */}
              <div className="mt-4 flex justify-center">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                    card.rarity === 'legendary'
                      ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                      : card.rarity === 'epic'
                      ? 'bg-yellow-500 text-black'
                      : card.rarity === 'rare'
                      ? 'bg-gray-400 text-black'
                      : 'bg-gray-600 text-white'
                  }`}
                >
                  {card.rarity === 'legendary' ? 'Prismatic' : card.rarity}
                </span>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Individual Reroll Button */}
      <motion.button
        onClick={onReroll}
        disabled={isRerolling}
        className="flex items-center gap-2 bg-gradient-to-r from-teal-600 to-blue-600 hover:from-teal-500 hover:to-blue-500 text-white font-bold px-4 py-2 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <RefreshCw
          size={16}
          className={`transition-transform ${isRerolling ? 'animate-spin' : 'group-hover:rotate-180'}`}
        />
        <span>Reroll</span>
      </motion.button>
    </div>
  );
}
