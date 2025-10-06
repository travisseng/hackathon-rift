import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';
import { SkillRadar as SkillRadarType } from '../../types/stats';

interface SkillRadarProps {
  data: SkillRadarType;
  showComparison?: boolean;
}

export default function SkillRadar({ data, showComparison = false }: SkillRadarProps) {
  const chartData = [
    { skill: 'Combat', current: data.combat, previous: data.previous_period?.combat, percentile: data.percentile_rank?.combat },
    { skill: 'Vision', current: data.vision, previous: data.previous_period?.vision, percentile: data.percentile_rank?.vision },
    { skill: 'Farming', current: data.farming, previous: data.previous_period?.farming, percentile: data.percentile_rank?.farming },
    { skill: 'Objectives', current: data.objectives, previous: data.previous_period?.objectives, percentile: data.percentile_rank?.objectives },
    { skill: 'Positioning', current: data.positioning, previous: data.previous_period?.positioning, percentile: data.percentile_rank?.positioning },
    { skill: 'Teamfight', current: data.teamfight, previous: data.previous_period?.teamfight, percentile: data.percentile_rank?.teamfight },
  ];

  return (
    <div className="bg-lol-dark-lighter rounded-xl p-6 border border-lol-gold/10">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-white mb-1">Skill Assessment</h3>
        <p className="text-gray-400 text-sm">Your performance across key areas</p>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={chartData}>
          <PolarGrid stroke="#31313C" />
          <PolarAngleAxis dataKey="skill" stroke="#8d99ae" tick={{ fill: '#8d99ae' }} />
          <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#8d99ae" tick={{ fill: '#8d99ae' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1E2328',
              border: '1px solid #C89B3C',
              borderRadius: '8px',
            }}
          />
          <Legend />
          <Radar
            name="Current"
            dataKey="current"
            stroke="#C89B3C"
            fill="#C89B3C"
            fillOpacity={0.6}
            strokeWidth={2}
          />
          {showComparison && data.previous_period && (
            <Radar
              name="Previous Period"
              dataKey="previous"
              stroke="#0AC8B9"
              fill="#0AC8B9"
              fillOpacity={0.3}
              strokeWidth={2}
            />
          )}
        </RadarChart>
      </ResponsiveContainer>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-6">
        {chartData.map((item) => (
          <div key={item.skill} className="bg-lol-dark rounded-lg p-3">
            <p className="text-gray-400 text-xs mb-1">{item.skill}</p>
            <div className="flex items-end gap-2">
              <span className="text-lol-gold font-bold text-2xl">{item.current}</span>
              {item.percentile && (
                <span className="text-gray-500 text-sm mb-1">Top {100 - item.percentile}%</span>
              )}
            </div>
            {item.previous && (
              <p className={`text-xs mt-1 ${item.current > item.previous ? 'text-green-500' : 'text-red-500'}`}>
                {item.current > item.previous ? '+' : ''}
                {(item.current - item.previous).toFixed(0)} from last period
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
