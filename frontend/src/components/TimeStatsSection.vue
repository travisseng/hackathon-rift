<template>
  <section class="section time-stats-section">
    <div class="stats-container">
      <h2 class="section-title">Time Investment</h2>

      <!-- Total Time Stats -->
      <div class="subsection">
        <h3 class="subsection-title">Total Time</h3>
        <div class="stats-grid">
          <div class="stat-card time-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-value-large">{{ formatTimeFromSeconds(data.total.game_time) }}</div>
            <div class="stat-label">Total Game Time</div>
            <div class="stat-detail">{{ formatNumber(data.total.game_time) }} seconds</div>
          </div>

          <div class="stat-card death-time-card">
            <div class="stat-icon">💀</div>
            <div class="stat-value-large">{{ formatTimeFromSeconds(data.total.death_time) }}</div>
            <div class="stat-label">Time Spent Dead</div>
            <div class="stat-detail">{{ formatNumber(data.total.death_time) }} seconds</div>
          </div>

          <div class="stat-card longest-card">
            <div class="stat-icon">🏃</div>
            <div class="stat-value-large">{{ formatTimeFromSeconds(data.total.longest_game) }}</div>
            <div class="stat-label">Longest Game</div>
            <div class="stat-detail">{{ formatNumber(data.total.longest_game) }} seconds</div>
          </div>
        </div>
      </div>

      <!-- Average Time Stats -->
      <div class="subsection">
        <h3 class="subsection-title">Averages</h3>
        <div class="stats-grid-small">
          <div class="stat-card-compact">
            <div class="stat-icon-small">📊</div>
            <div class="stat-content">
              <div class="stat-value-compact">{{ formatMinutes(data.average.game_duration) }}</div>
              <div class="stat-label-compact">Avg Game Duration</div>
            </div>
          </div>

          <div class="stat-card-compact">
            <div class="stat-icon-small">⏳</div>
            <div class="stat-content">
              <div class="stat-value-compact">{{ formatMinutes(data.average.death_time) }}</div>
              <div class="stat-label-compact">Avg Death Time</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Play Time Chart Section -->
      <PlayTimeChart ref="chartSection" :data="getSortedPlayTime(data.by_month)" />


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
import PlayTimeChart from './PlayTimeChart.vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  insights: {
    type: Array,
    default: () => []
  }
})

const getSortedPlayTime = (playTimeData) => {
  if (!playTimeData) return {}

  const entries = Object.entries(playTimeData)
  entries.sort((a, b) => {
    const dateA = new Date(a[0])
    const dateB = new Date(b[0])
    return dateA - dateB
  })

  return Object.fromEntries(entries)
}

const formatNumber = (num) => {
  return num.toLocaleString()
}

const formatTimeFromSeconds = (totalSeconds) => {
  const days = Math.floor(totalSeconds / 86400)
  const hours = Math.floor((totalSeconds % 86400) / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)

  const parts = []

  if (days > 0) {
    parts.push(`${days} ${days === 1 ? 'day' : 'days'}`)
  }

  if (hours > 0) {
    parts.push(`${hours} ${hours === 1 ? 'hour' : 'hours'}`)
  }

  if (minutes > 0 || parts.length === 0) {
    parts.push(`${minutes} ${minutes === 1 ? 'minute' : 'minutes'}`)
  }

  return parts.join(' ')
}

const formatMinutes = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${minutes}m ${secs}s`
}
</script>

<style scoped>
.time-stats-section {
  background: radial-gradient(circle at center, rgba(3, 151, 171, 0.1) 0%, transparent 70%);
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
  background: linear-gradient(135deg, #0397ab, #00dfa2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.subsection {
  margin-bottom: 3rem;
}

.subsection-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--lol-gold);
  margin-bottom: 1.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.stats-grid-small {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(3, 151, 171, 0.3);
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: #0397ab;
  box-shadow: 0 10px 30px rgba(3, 151, 171, 0.3);
}

.time-card {
  border-color: rgba(0, 223, 162, 0.5);
}

.death-time-card {
  border-color: rgba(255, 70, 85, 0.5);
}

.longest-card {
  border-color: rgba(200, 155, 60, 0.5);
}

.stat-card-compact {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(3, 151, 171, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.stat-card-compact:hover {
  transform: translateY(-3px);
  border-color: #0397ab;
  box-shadow: 0 8px 20px rgba(3, 151, 171, 0.3);
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.stat-icon-small {
  font-size: 2rem;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  text-align: left;
}

.stat-value-large {
  font-size: 1.8rem;
  font-weight: 900;
  color: #0397ab;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 20px rgba(3, 151, 171, 0.5);
}

.stat-value-compact {
  font-size: 1.5rem;
  font-weight: 900;
  color: #0397ab;
  margin-bottom: 0.3rem;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.stat-label-compact {
  font-size: 0.85rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.stat-detail {
  font-size: 0.75rem;
  color: rgba(240, 230, 210, 0.6);
  margin-top: 0.3rem;
}

/* Monthly Chart */
.monthly-chart {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
  padding: 2rem;
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(3, 151, 171, 0.3);
  border-radius: 15px;
  min-height: 300px;
}

.month-bar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.bar-container {
  width: 100%;
  height: 200px;
  position: relative;
  display: flex;
  align-items: flex-end;
}

.bar-fill {
  width: 100%;
  background: linear-gradient(180deg, #00dfa2, #0397ab);
  border-radius: 8px 8px 0 0;
  position: relative;
  transition: all 0.3s ease;
  min-height: 20px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 0.5rem;
}

.bar-fill:hover {
  filter: brightness(1.2);
  box-shadow: 0 0 20px rgba(0, 223, 162, 0.5);
}

.bar-value {
  font-size: 0.9rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.bar-label {
  font-size: 0.8rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  text-align: center;
}

.insights-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.insight-item {
  background: rgba(10, 20, 40, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(3, 151, 171, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.insight-item:hover {
  border-color: rgba(3, 151, 171, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(3, 151, 171, 0.2);
}

.insight-tag {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: linear-gradient(135deg, rgba(3, 151, 171, 0.2), rgba(3, 151, 171, 0.3));
  border: 1px solid rgba(3, 151, 171, 0.4);
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #00dfa2;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(3, 151, 171, 0.15);
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

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid-small {
    grid-template-columns: 1fr;
  }

  .monthly-chart {
    padding: 1rem;
    min-height: 250px;
    overflow-x: auto;
  }

  .bar-container {
    height: 150px;
  }

  .bar-label {
    font-size: 0.7rem;
  }
}
</style>
