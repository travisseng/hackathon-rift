import { CardDeck } from '../types/stats';

export const mockPrimaryDeck: CardDeck = {
  player_id: 'mock-player-123',
  deck_type: 'primary',
  generated_at: new Date().toISOString(),
  cards: [
    {
      id: 'card_most_played_ahri',
      category: 'champion_mastery',
      title: 'Your Champion',
      value: '147 Games',
      subtitle: 'on Ahri - That\'s 49 hours of charm spam!',
      theme: {
        artwork_url: 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg',
        background_color: '#c77dff',
        accent_color: '#9d4edd',
      },
      rarity: 'epic',
      shareable: true,
      metadata: {
        champion_id: 103,
        total_games: 147,
        win_rate: 0.548,
      },
    },
    {
      id: 'card_penta_kill',
      category: 'milestone',
      title: 'Pentakill Master',
      value: '3 Pentakills',
      subtitle: 'That legendary announcer voice still echoes...',
      theme: {
        artwork_url: 'https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-profiles/global/default/icon-achievement.png',
        background_color: '#ffd60a',
        accent_color: '#fca311',
      },
      rarity: 'legendary',
      shareable: true,
      metadata: {
        total_pentas: 3,
        champions: ['Katarina', 'Yasuo', 'Ahri'],
      },
    },
    {
      id: 'card_vision_king',
      category: 'growth',
      title: 'Vision Improvement',
      value: '+42%',
      subtitle: 'Your vision score jumped from 32 to 45.5 per game',
      theme: {
        artwork_url: 'https://ddragon.leagueoflegends.com/cdn/14.1.1/img/item/2055.png',
        background_color: '#06ffa5',
        accent_color: '#00d084',
      },
      rarity: 'rare',
      shareable: true,
      metadata: {
        old_avg: 32,
        new_avg: 45.5,
        improvement_pct: 42,
      },
    },
  ],
};

export const mockSecondaryDeck: CardDeck = {
  player_id: 'mock-player-123',
  deck_type: 'secondary',
  generated_at: new Date().toISOString(),
  cards: [
    {
      id: 'card_deaths',
      category: 'funny',
      title: 'Death Counter',
      value: '1,247 Deaths',
      subtitle: 'You spent 18 hours looking at gray screens',
      theme: {
        artwork_url: 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',
        background_color: '#ff6b6b',
        accent_color: '#ee5a6f',
      },
      rarity: 'common',
      shareable: true,
      metadata: {
        total_deaths: 1247,
        time_spent_dead: 64800,
      },
    },
    {
      id: 'card_distance',
      category: 'movement',
      title: 'Marathon Runner',
      value: '2,847 km',
      subtitle: 'You could have walked to Berlin and back!',
      theme: {
        artwork_url: 'https://ddragon.leagueoflegends.com/cdn/14.1.1/img/spell/SummonerHaste.png',
        background_color: '#4cc9f0',
        accent_color: '#3a86ff',
      },
      rarity: 'rare',
      shareable: true,
      metadata: {
        total_distance: 2847000,
        distance_km: 2847,
      },
    },
    {
      id: 'card_baron',
      category: 'geography',
      title: 'Baron Secured',
      value: '87 Barons',
      subtitle: 'The purple worm fears you',
      theme: {
        artwork_url: 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/content/src/leagueclient/gamemodeassets/gamemodex/img/icon-baron.png',
        background_color: '#8d99ae',
        accent_color: '#6c757d',
      },
      rarity: 'epic',
      shareable: true,
      metadata: {
        barons_secured: 87,
        baron_steals: 12,
      },
    },
  ],
};
