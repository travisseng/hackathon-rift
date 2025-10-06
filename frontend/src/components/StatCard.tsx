import { motion } from 'framer-motion';
import { StatCard as StatCardType } from '../types/stats';
import { Share2 } from 'lucide-react';

interface StatCardProps {
  card: StatCardType;
  isFlipped: boolean;
  onShare?: () => void;
}

export default function StatCard({ card, isFlipped, onShare }: StatCardProps) {
  const rarityBorder = {
    common: 'border-gray-400',
    rare: 'border-blue-400',
    epic: 'border-purple-500',
    legendary: 'border-yellow-400',
  };

  const rarityGlow = {
    common: '',
    rare: 'shadow-lg shadow-blue-400/50',
    epic: 'shadow-lg shadow-purple-500/50',
    legendary: 'shadow-2xl shadow-yellow-400/70 animate-pulse',
  };

  return (
    <motion.div
      className="relative w-full aspect-[2/3] perspective-1000"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <motion.div
        className={`relative w-full h-full rounded-xl border-4 ${rarityBorder[card.rarity]} ${rarityGlow[card.rarity]} overflow-hidden`}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6, ease: 'easeInOut' }}
        style={{ transformStyle: 'preserve-3d' }}
      >
        {/* Card Front */}
        <div
          className="absolute inset-0 backface-hidden"
          style={{
            backgroundColor: card.theme.background_color,
            backgroundImage: `linear-gradient(135deg, ${card.theme.background_color} 0%, ${card.theme.accent_color} 100%)`,
          }}
        >
          {/* Artwork Background */}
          <div
            className="absolute inset-0 opacity-30"
            style={{
              backgroundImage: `url(${card.theme.artwork_url})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
            }}
          />

          {/* Content */}
          <div className="relative h-full flex flex-col justify-between p-6 text-white">
            {/* Header */}
            <div>
              <div className="flex justify-between items-start mb-4">
                <span className="text-xs uppercase tracking-wider opacity-80">
                  {card.category.replace('_', ' ')}
                </span>
                <span className="text-xs uppercase tracking-wider font-bold opacity-90">
                  {card.rarity}
                </span>
              </div>

              <h3 className="text-2xl font-bold mb-2 drop-shadow-lg">
                {card.title}
              </h3>
            </div>

            {/* Main Value */}
            <div className="flex-1 flex items-center justify-center">
              <p className="text-5xl font-black drop-shadow-2xl text-center">
                {card.value}
              </p>
            </div>

            {/* Footer */}
            <div>
              {card.subtitle && (
                <p className="text-sm opacity-90 mb-3 drop-shadow">
                  {card.subtitle}
                </p>
              )}

              {card.shareable && onShare && (
                <button
                  onClick={onShare}
                  className="flex items-center gap-2 text-sm hover:opacity-80 transition-opacity"
                >
                  <Share2 size={16} />
                  Share
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Card Back (Optional - can be used for additional info) */}
        <div
          className="absolute inset-0 backface-hidden rotate-y-180"
          style={{ backgroundColor: card.theme.accent_color }}
        >
          <div className="h-full flex items-center justify-center text-white text-2xl font-bold">
            League of Legends
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
