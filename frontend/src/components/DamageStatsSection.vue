<template>
  <section class="section damage-stats-section">
    <div class="stats-container">
      <h2 class="section-title">Combat Performance</h2>

      <!-- Damage Stats -->
      <div class="stats-grid">
        <div class="stat-card damage-dealt">
          <div class="stat-icon">⚔️</div>
          <div class="stat-value">{{ formatNumber(data.total.damage_dealt) }}</div>
          <div class="stat-label">Total Damage Dealt</div>
          <div class="stat-avg">{{ formatNumber(data.average.damage_dealt) }} avg</div>
        </div>

        <div class="stat-card damage-taken">
          <div class="stat-icon">🛡️</div>
          <div class="stat-value">{{ formatNumber(data.total.damage_taken) }}</div>
          <div class="stat-label">Total Damage Taken</div>
          <div class="stat-avg">{{ formatNumber(data.average.damage_taken) }} avg</div>
        </div>

        <div class="stat-card healing">
          <div class="stat-icon">💚</div>
          <div class="stat-value">{{ formatNumber(data.total.healing_done) }}</div>
          <div class="stat-label">Total Healing</div>
          <div class="stat-avg">{{ formatNumber(data.average.healing_done) }} avg</div>
        </div>

        <div class="stat-card healing-team">
          <div class="stat-icon">💝</div>
          <div class="stat-value">{{ formatNumber(data.total.healing_teammates) }}</div>
          <div class="stat-label">Healing Teammates</div>
          <div class="stat-avg">{{ formatNumber(data.average.healing_teammates) }} avg</div>
        </div>

        <div class="stat-card cc">
          <div class="stat-icon">🌀</div>
          <div class="stat-value">{{ formatSeconds(data.total.cc_time) }}</div>
          <div class="stat-label">Total CC Time</div>
          <div class="stat-avg">{{ data.average.cc_time.toFixed(1) }}s avg</div>
        </div>
      </div>

      <!-- Insights Section -->
      <div v-if="insights && insights.length > 0" class="insights-section">
        <div v-for="(insight, index) in insights" :key="index" class="insight-item">
          <span class="insight-tag">{{ insight.tag }}</span>
          <p class="insight-comment">{{ insight.comment }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
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

const formatNumber = (num) => {
  return num.toLocaleString()
}

const formatSeconds = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  return minutes > 0 ? `${minutes}m ${secs}s` : `${secs}s`
}
</script>

<style scoped>
.damage-stats-section {
  background: radial-gradient(circle at center, rgba(255, 70, 85, 0.1) 0%, transparent 70%);
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
  background: linear-gradient(135deg, #ff4655, #ff8c94);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 70, 85, 0.3);
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: #ff4655;
  box-shadow: 0 10px 30px rgba(255, 70, 85, 0.3);
}

.damage-dealt {
  border-color: rgba(255, 70, 85, 0.5);
}

.damage-taken {
  border-color: rgba(3, 151, 171, 0.5);
}

.healing {
  border-color: rgba(0, 223, 162, 0.5);
}

.healing-team {
  border-color: rgba(255, 105, 180, 0.5);
}

.cc {
  border-color: rgba(200, 155, 60, 0.5);
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 900;
  color: #ff4655;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 20px rgba(255, 70, 85, 0.5);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.stat-avg {
  font-size: 0.8rem;
  color: rgba(240, 230, 210, 0.6);
  margin-top: 0.5rem;
}

/* Insights Section */
.insights-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.insight-item {
  background: rgba(10, 20, 40, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 70, 85, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.insight-item:hover {
  border-color: rgba(255, 70, 85, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 70, 85, 0.2);
}

.insight-tag {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: linear-gradient(135deg, rgba(255, 70, 85, 0.2), rgba(255, 140, 148, 0.2));
  border: 1px solid rgba(255, 70, 85, 0.4);
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #ff8c94;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(255, 70, 85, 0.15);
}

.insight-comment {
  font-size: 1rem;
  color: var(--lol-gold-light);
  line-height: 1.7;
  margin: 0;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-container {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .insight-item {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
