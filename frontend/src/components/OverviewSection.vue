<template>
  <section class="section overview-section">
    <div class="stats-container">
      <h2 class="section-title">Season Overview</h2>

      <!-- Player Title Display -->
      <div v-if="title" class="player-title-banner">
        <div class="title-text">{{ title }}</div>
      </div>

      <div class="stats-grid">
        <div class="stat-card primary">
          <div class="stat-icon">🎮</div>
          <div class="stat-value">{{ data.games_played }}</div>
          <div class="stat-label">Games Played</div>
        </div>

        <div class="stat-card success">
          <div class="stat-icon">✨</div>
          <div class="stat-value">{{ data.wins }}</div>
          <div class="stat-label">Victories</div>
        </div>

        <div class="stat-card danger">
          <div class="stat-icon">💔</div>
          <div class="stat-value">{{ data.losses }}</div>
          <div class="stat-label">Defeats</div>
        </div>

        <div class="stat-card highlight">
          <div class="stat-icon">📊</div>
          <div class="stat-value">{{ formatWinrate(data.winrate) }}%</div>
          <div class="stat-label">Win Rate</div>
          <div class="stat-subtext" :class="getWinrateClass(data.winrate)">
            {{ getWinrateText(data.winrate) }}
          </div>
        </div>

        <div class="stat-card info">
          <div class="stat-icon">🏆</div>
          <div class="stat-value">{{ data.champion_pool }}</div>
          <div class="stat-label">Champions Mastered</div>
        </div>
      </div>

      <!-- Insights Section -->
      <div v-if="insights && insights.length > 0" class="insights-section">
          <div v-for="(insight, index) in insights" :key="index" class="insight-item">
            <div class="insight-tag">{{ insight.tag }}</div>
            <div class="insight-comment">{{ insight.comment }}</div>
          </div>
        </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  insights: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: ''
  }
})

const formatWinrate = (winrate) => {
  return (winrate * 100).toFixed(0)
}

const getWinrateClass = (winrate) => {
  if (winrate >= 0.55) return 'excellent'
  if (winrate >= 0.50) return 'good'
  if (winrate >= 0.45) return 'average'
  return 'needs-improvement'
}

const getWinrateText = (winrate) => {
  if (winrate >= 0.55) return 'Excellent!'
  if (winrate >= 0.50) return 'Above Average'
  if (winrate >= 0.45) return 'Close to Target'
  return 'Room to Improve'
}
</script>

<style scoped>
.overview-section {
  background: radial-gradient(circle at center, rgba(200, 155, 60, 0.1) 0%, transparent 70%);
}

.stats-container {
  max-width: 1200px;
  width: 100%;
  padding: 2rem;
}

.section-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 900;
  text-align: center;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-gold-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.player-title-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1.5rem 2rem;
  margin: 0 auto 3rem;
  max-width: 600px;
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.2), rgba(200, 155, 60, 0.1));
  border: 2px solid var(--lol-gold);
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(200, 155, 60, 0.3);
  transition: all 0.3s ease;
}

.player-title-banner:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 50px rgba(200, 155, 60, 0.4);
}

.title-icon {
  font-size: 2.5rem;
  filter: drop-shadow(0 0 15px rgba(200, 155, 60, 0.5));
}

.title-text {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--lol-gold);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  text-shadow: 0 0 20px rgba(200, 155, 60, 0.5);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, transparent, var(--lol-gold), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--lol-gold);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.3);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-card.primary {
  border-color: rgba(3, 151, 171, 0.5);
}

.stat-card.success {
  border-color: rgba(0, 223, 162, 0.5);
}

.stat-card.danger {
  border-color: rgba(255, 70, 85, 0.5);
}

.stat-card.highlight {
  border-color: rgba(200, 155, 60, 0.7);
  background: rgba(200, 155, 60, 0.05);
}

.stat-card.info {
  border-color: rgba(145, 116, 255, 0.5);
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0 0 10px rgba(200, 155, 60, 0.3));
}

.stat-value {
  font-size: 3rem;
  font-weight: 900;
  color: var(--lol-gold);
  margin-bottom: 0.5rem;
  text-shadow: 0 0 20px rgba(200, 155, 60, 0.5);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
}

.stat-subtext {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-subtext.excellent {
  color: #00dfa2;
}

.stat-subtext.good {
  color: #0397ab;
}

.stat-subtext.average {
  color: var(--lol-gold);
}

.stat-subtext.needs-improvement {
  color: #ff4655;
}

.insights-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.insight-item {
  background: rgba(10, 20, 40, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(200, 155, 60, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.insight-item:hover {
  border-color: rgba(200, 155, 60, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(200, 155, 60, 0.2);
}

.insight-tag {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.2), rgba(200, 155, 60, 0.3));
  border: 1px solid rgba(200, 155, 60, 0.4);
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--lol-gold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(200, 155, 60, 0.15);
}

.insight-comment {
  font-size: 1rem;
  color: var(--lol-gold-light);
  line-height: 1.7;
  margin: 0;
}

@media (max-width: 768px) {
  .stats-container {
    padding: 1rem;
  }

  .player-title-banner {
    padding: 1.2rem 1.5rem;
    gap: 0.8rem;
  }

  .title-icon {
    font-size: 2rem;
  }

  .title-text {
    font-size: 1.2rem;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }

  .stat-card {
    padding: 1.5rem 1rem;
  }

  .stat-icon {
    font-size: 2rem;
  }

  .stat-value {
    font-size: 2rem;
  }

  .stat-label {
    font-size: 0.8rem;
  }

  .comment-section {
    padding: 1.5rem;
  }
}
</style>
