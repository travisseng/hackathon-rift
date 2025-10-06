import axios from 'axios';
import type { CardDeck, ProgressionTimeSeries, CoachingInsight, Recommendation } from '../types/stats';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Card endpoints
export const cardApi = {
  getPrimaryCards: async (puuid: string): Promise<CardDeck> => {
    const { data } = await api.get(`/cards/${puuid}/primary`);
    return data;
  },

  getSecondaryCards: async (puuid: string): Promise<CardDeck> => {
    const { data } = await api.get(`/cards/${puuid}/secondary`);
    return data;
  },

  generateCards: async (puuid: string, forceRefresh = false): Promise<void> => {
    await api.post(`/cards/${puuid}/generate`, { force_refresh: forceRefresh });
  },

  shareCard: async (cardId: string): Promise<{ url: string }> => {
    const { data } = await api.post(`/cards/${cardId}/share`);
    return data;
  },
};

// Progression endpoints
export const progressionApi = {
  getProgression: async (puuid: string, timePeriod = 'all') => {
    const { data } = await api.get(`/progression/${puuid}`, {
      params: { time_period: timePeriod },
    });
    return data;
  },

  getMetricTimeSeries: async (
    puuid: string,
    metric: string,
    aggregation = 'weekly'
  ): Promise<ProgressionTimeSeries> => {
    const { data } = await api.get(`/progression/${puuid}/metrics/${metric}`, {
      params: { aggregation },
    });
    return data;
  },

  getSkillRadar: async (puuid: string, includeComparison = false) => {
    const { data } = await api.get(`/progression/${puuid}/skill-radar`, {
      params: { include_comparison: includeComparison },
    });
    return data;
  },

  analyzeProgression: async (puuid: string): Promise<void> => {
    await api.post(`/progression/${puuid}/analyze`);
  },
};

// Coaching endpoints
export const coachingApi = {
  getCoaching: async (puuid: string) => {
    const { data } = await api.get(`/coaching/${puuid}`);
    return data;
  },

  getInsights: async (puuid: string, priority?: string): Promise<CoachingInsight[]> => {
    const { data } = await api.get(`/coaching/${puuid}/insights`, {
      params: { priority },
    });
    return data;
  },

  generateInsights: async (puuid: string): Promise<void> => {
    await api.post(`/coaching/${puuid}/insights/generate`);
  },

  getRecommendations: async (puuid: string, category?: string): Promise<Recommendation[]> => {
    const { data } = await api.get(`/coaching/${puuid}/recommendations`, {
      params: { category },
    });
    return data;
  },

  updateRecommendationProgress: async (
    puuid: string,
    recId: string,
    progress: number
  ): Promise<void> => {
    await api.put(`/coaching/${puuid}/recommendations/${recId}/progress`, { progress });
  },

  chatWithCoach: async (puuid: string, message: string, sessionId?: string) => {
    const { data } = await api.post(`/coaching/${puuid}/chat`, {
      message,
      session_id: sessionId,
    });
    return data;
  },

  createGoal: async (puuid: string, goal: any) => {
    const { data } = await api.post(`/coaching/${puuid}/goals`, goal);
    return data;
  },
};

// Player endpoints
export const playerApi = {
  getPlayer: async (puuid: string) => {
    const { data } = await api.get(`/players/${puuid}`);
    return data;
  },

  getPlayerByName: async (region: string, summonerName: string) => {
    const { data } = await api.get(`/players/by-name/${region}/${summonerName}`);
    return data;
  },
};

// Match endpoints
export const matchApi = {
  getMatchHistory: async (puuid: string, start = 0, count = 20) => {
    const { data } = await api.get(`/matches/${puuid}`, {
      params: { start, count },
    });
    return data;
  },

  syncMatches: async (puuid: string): Promise<void> => {
    await api.post(`/matches/${puuid}/sync`);
  },
};

export default api;
