import type { ProgressionTimeSeries, SkillRadar, DataPoint } from '../types/stats';

// Generate realistic time series data
const generateTimeSeries = (
  metric: string,
  startValue: number,
  trend: 'improving' | 'declining' | 'stable',
  months: number = 12
): DataPoint[] => {
  const data: DataPoint[] = [];
  let value = startValue;
  const trendMultiplier = trend === 'improving' ? 1.02 : trend === 'declining' ? 0.98 : 1.0;

  for (let i = 0; i < months; i++) {
    const date = new Date(2024, i, 1);
    const variance = (Math.random() - 0.5) * 0.1 * startValue;
    value = value * trendMultiplier + variance;

    data.push({
      timestamp: date.toISOString().split('T')[0],
      value: Math.max(0, parseFloat(value.toFixed(2))),
      match_count: Math.floor(Math.random() * 20) + 10,
    });
  }

  return data;
};

export const mockProgressionMetrics: ProgressionTimeSeries[] = [
  {
    metric: 'kda',
    data_points: generateTimeSeries('kda', 2.5, 'improving'),
    aggregation_period: 'monthly',
    trend: 'improving',
    change_percentage: 18.5,
  },
  {
    metric: 'vision_score',
    data_points: generateTimeSeries('vision_score', 32, 'improving'),
    aggregation_period: 'monthly',
    trend: 'improving',
    change_percentage: 35.2,
  },
  {
    metric: 'cs_per_min',
    data_points: generateTimeSeries('cs_per_min', 6.2, 'stable'),
    aggregation_period: 'monthly',
    trend: 'stable',
    change_percentage: 2.1,
  },
  {
    metric: 'damage_per_min',
    data_points: generateTimeSeries('damage_per_min', 580, 'improving'),
    aggregation_period: 'monthly',
    trend: 'improving',
    change_percentage: 12.8,
  },
  {
    metric: 'gold_per_min',
    data_points: generateTimeSeries('gold_per_min', 380, 'stable'),
    aggregation_period: 'monthly',
    trend: 'stable',
    change_percentage: 1.5,
  },
  {
    metric: 'kill_participation',
    data_points: generateTimeSeries('kill_participation', 0.58, 'improving'),
    aggregation_period: 'monthly',
    trend: 'improving',
    change_percentage: 8.6,
  },
  {
    metric: 'win_rate',
    data_points: generateTimeSeries('win_rate', 0.51, 'improving'),
    aggregation_period: 'monthly',
    trend: 'improving',
    change_percentage: 5.9,
  },
];

export const mockSkillRadar: SkillRadar = {
  combat: 78,
  vision: 82,
  farming: 71,
  objectives: 75,
  positioning: 80,
  teamfight: 85,
  previous_period: {
    combat: 72,
    vision: 68,
    farming: 70,
    objectives: 71,
    positioning: 75,
    teamfight: 80,
  },
  percentile_rank: {
    combat: 65,
    vision: 78,
    farming: 58,
    objectives: 62,
    positioning: 72,
    teamfight: 81,
  },
};

export const mockChampionProgression = [
  {
    champion_id: 103,
    champion_name: 'Ahri',
    total_games: 147,
    win_rate: 0.548,
    avg_kda: 3.2,
    mastery_level: 7,
    first_10_games_wr: 0.4,
    recent_10_games_wr: 0.7,
    improvement_trend: 'improving' as const,
    skill_ratings: {
      combat: 85,
      vision: 78,
      farming: 82,
      objectives: 75,
      positioning: 88,
      teamfight: 90,
    },
    best_matchups: ['Zed', 'Yasuo', 'Yone'],
    worst_matchups: ['Malzahar', 'Kassadin', 'Galio'],
  },
  {
    champion_id: 238,
    champion_name: 'Zed',
    total_games: 89,
    win_rate: 0.52,
    avg_kda: 2.8,
    mastery_level: 6,
    first_10_games_wr: 0.3,
    recent_10_games_wr: 0.6,
    improvement_trend: 'improving' as const,
    skill_ratings: {
      combat: 82,
      vision: 65,
      farming: 78,
      objectives: 70,
      positioning: 75,
      teamfight: 72,
    },
    best_matchups: ['Lux', 'Xerath', 'Vel\'Koz'],
    worst_matchups: ['Diana', 'Akali', 'Fizz'],
  },
  {
    champion_id: 157,
    champion_name: 'Yasuo',
    total_games: 67,
    win_rate: 0.46,
    avg_kda: 2.3,
    mastery_level: 5,
    first_10_games_wr: 0.5,
    recent_10_games_wr: 0.4,
    improvement_trend: 'declining' as const,
    skill_ratings: {
      combat: 70,
      vision: 58,
      farming: 85,
      objectives: 65,
      positioning: 62,
      teamfight: 75,
    },
    best_matchups: ['Veigar', 'Lux', 'Syndra'],
    worst_matchups: ['Renekton', 'Akali', 'Irelia'],
  },
];

export const mockMilestones = [
  {
    id: 'milestone_1',
    title: 'First Pentakill!',
    description: 'Achieved your first pentakill on Katarina',
    achieved_at: '2024-03-15T18:30:00Z',
    match_id: 'NA1_4567890123',
    icon_url: 'https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-profiles/global/default/icon-achievement.png',
    rarity: 'legendary',
  },
  {
    id: 'milestone_2',
    title: 'Vision Master',
    description: 'Achieved 100+ vision score in a single game',
    achieved_at: '2024-05-22T20:15:00Z',
    match_id: 'NA1_4567890124',
    icon_url: 'https://ddragon.leagueoflegends.com/cdn/14.1.1/img/item/2055.png',
    rarity: 'epic',
  },
  {
    id: 'milestone_3',
    title: 'Mastery 7',
    description: 'Reached Mastery 7 on Ahri',
    achieved_at: '2024-07-10T14:45:00Z',
    icon_url: 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg',
    rarity: 'rare',
  },
];
