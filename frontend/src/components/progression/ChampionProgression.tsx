import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface ChampionProgressionItem {
  champion_id: number;
  champion_name: string;
  total_games: number;
  win_rate: number;
  avg_kda: number;
  mastery_level: number;
  first_10_games_wr: number;
  recent_10_games_wr: number;
  improvement_trend: 'improving' | 'declining' | 'stable';
  skill_ratings: {
    combat: number;
    vision: number;
    farming: number;
    objectives: number;
    positioning: number;
    teamfight: number;
  };
  best_matchups: string[];
  worst_matchups: string[];
}

interface ChampionProgressionProps {
  champions: ChampionProgressionItem[];
}

export default function ChampionProgression({ champions }: ChampionProgressionProps) {
  const getTrendIcon = (trend: string) => {
    if (trend === 'improving') return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (trend === 'declining') return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <Minus className="w-4 h-4 text-gray-500" />;
  };

  const getWinRateColor = (wr: number) => {
    if (wr >= 0.55) return 'text-green-500';
    if (wr >= 0.50) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <div className="bg-lol-dark-lighter rounded-xl p-6 border border-lol-gold/10">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-white mb-1">Champion Progression</h3>
        <p className="text-gray-400 text-sm">Your performance on each champion</p>
      </div>

      <div className="space-y-4">
        {champions.map((champ) => (
          <div
            key={champ.champion_id}
            className="bg-lol-dark rounded-lg p-4 hover:border hover:border-lol-gold/30 transition-all"
          >
            <div className="flex items-start gap-4">
              {/* Champion Icon */}
              <img
                src={`https://ddragon.leagueoflegends.com/cdn/14.1.1/img/champion/${champ.champion_name}.png`}
                alt={champ.champion_name}
                className="w-16 h-16 rounded-lg"
                onError={(e) => {
                  e.currentTarget.src = 'https://ddragon.leagueoflegends.com/cdn/14.1.1/img/champion/Ahri.png';
                }}
              />

              {/* Champion Info */}
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <h4 className="text-white font-bold text-lg">{champ.champion_name}</h4>
                    <span className="text-xs bg-lol-gold/20 text-lol-gold px-2 py-1 rounded">
                      M{champ.mastery_level}
                    </span>
                    {getTrendIcon(champ.improvement_trend)}
                  </div>
                  <span className="text-gray-400 text-sm">{champ.total_games} games</span>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                  <div>
                    <p className="text-gray-400 text-xs">Win Rate</p>
                    <p className={`font-bold ${getWinRateColor(champ.win_rate)}`}>
                      {(champ.win_rate * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-xs">Avg KDA</p>
                    <p className="text-white font-bold">{champ.avg_kda.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-xs">First 10 Games</p>
                    <p className="text-gray-300">{(champ.first_10_games_wr * 100).toFixed(0)}% WR</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-xs">Recent 10 Games</p>
                    <p className={getWinRateColor(champ.recent_10_games_wr)}>
                      {(champ.recent_10_games_wr * 100).toFixed(0)}% WR
                    </p>
                  </div>
                </div>

                {/* Matchups */}
                <div className="flex gap-6 text-sm">
                  <div>
                    <span className="text-green-500 font-medium">Good vs: </span>
                    <span className="text-gray-400">{champ.best_matchups.join(', ')}</span>
                  </div>
                  <div>
                    <span className="text-red-500 font-medium">Weak vs: </span>
                    <span className="text-gray-400">{champ.worst_matchups.join(', ')}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
