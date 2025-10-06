import { useState } from 'react';
import ProgressionChart from '../components/progression/ProgressionChart';
import SkillRadar from '../components/progression/SkillRadar';
import ChampionProgression from '../components/progression/ChampionProgression';
import {
  mockProgressionMetrics,
  mockSkillRadar,
  mockChampionProgression,
} from '../data/mockProgression';
import { ProgressionMetric } from '../types/stats';

export default function ProgressionPage() {
  const [selectedMetric, setSelectedMetric] = useState<ProgressionMetric>('kda');

  const currentMetricData = mockProgressionMetrics.find((m) => m.metric === selectedMetric);

  const metricOptions: { value: ProgressionMetric; label: string }[] = [
    { value: 'kda', label: 'KDA' },
    { value: 'vision_score', label: 'Vision Score' },
    { value: 'cs_per_min', label: 'CS per Minute' },
    { value: 'damage_per_min', label: 'Damage per Minute' },
    { value: 'gold_per_min', label: 'Gold per Minute' },
    { value: 'kill_participation', label: 'Kill Participation' },
    { value: 'win_rate', label: 'Win Rate' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      {/* Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-black text-white mb-3">Your Progression</h1>
        <p className="text-xl text-gray-400">Track your improvement over time</p>
      </div>

      {/* Metric Selector */}
      <div className="mb-8">
        <label className="block text-sm font-medium text-gray-400 mb-3">Select Metric</label>
        <div className="flex flex-wrap gap-2">
          {metricOptions.map((option) => (
            <button
              key={option.value}
              onClick={() => setSelectedMetric(option.value)}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                selectedMetric === option.value
                  ? 'bg-lol-gold text-lol-dark'
                  : 'bg-lol-dark-lighter text-gray-300 hover:bg-lol-dark-light'
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Chart */}
      {currentMetricData && (
        <div className="mb-8">
          <ProgressionChart data={currentMetricData} />
        </div>
      )}

      {/* Skill Radar */}
      <div className="mb-8">
        <SkillRadar data={mockSkillRadar} showComparison={true} />
      </div>

      {/* Champion Progression */}
      <div>
        <ChampionProgression champions={mockChampionProgression} />
      </div>
    </div>
  );
}
