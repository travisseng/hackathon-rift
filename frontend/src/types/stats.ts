/**
 * TypeScript types for the application
 */

export type CardCategory =
  | 'champion_mastery'
  | 'funny'
  | 'survival'
  | 'movement'
  | 'geography'
  | 'milestone'
  | 'social'
  | 'growth';

export type CardRarity = 'common' | 'rare' | 'epic' | 'legendary';

export interface CardTheme {
  artwork_url: string;
  background_color: string;
  accent_color: string;
  icon_url?: string;
}

export interface StatCard {
  id: string;
  category: CardCategory;
  title: string;
  value: string;
  subtitle?: string;
  theme: CardTheme;
  rarity: CardRarity;
  shareable: boolean;
  metadata: Record<string, any>;
}

export interface CardDeck {
  player_id: string;
  deck_type: 'primary' | 'secondary';
  cards: StatCard[];
  generated_at: string;
}

// Progression types
export type ProgressionMetric =
  | 'kda'
  | 'vision_score'
  | 'cs_per_min'
  | 'damage_per_min'
  | 'gold_per_min'
  | 'kill_participation'
  | 'win_rate';

export interface DataPoint {
  timestamp: string;
  value: number;
  match_count: number;
}

export interface ProgressionTimeSeries {
  metric: ProgressionMetric;
  data_points: DataPoint[];
  aggregation_period: 'daily' | 'weekly' | 'monthly';
  trend: 'improving' | 'declining' | 'stable';
  change_percentage?: number;
}

export interface SkillRadar {
  combat: number;
  vision: number;
  farming: number;
  objectives: number;
  positioning: number;
  teamfight: number;
  previous_period?: Record<string, number>;
  percentile_rank?: Record<string, number>;
}

// Coaching types
export type InsightType =
  | 'strength'
  | 'weakness'
  | 'improvement'
  | 'warning'
  | 'tip'
  | 'pattern'
  | 'achievement';

export type InsightPriority = 'critical' | 'high' | 'medium' | 'low';

export interface CoachingInsight {
  id: string;
  type: InsightType;
  priority: InsightPriority;
  title: string;
  description: string;
  evidence: string[];
  actionable: boolean;
  recommended_actions: string[];
  related_matches: string[];
  related_champions: string[];
  generated_at: string;
  confidence_score: number;
}

export interface Recommendation {
  id: string;
  category: string;
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  estimated_impact: 'low' | 'medium' | 'high';
  steps: string[];
  completed: boolean;
  progress: number;
  rationale: string;
  expected_outcome: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  insights?: CoachingInsight[];
  recommendations?: Recommendation[];
}
