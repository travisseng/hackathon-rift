<template>
  <section class="section economy-stats-section">
    <div class="stats-container">
      <h2 class="section-title">Economy & Farming</h2>

      <!-- Total Stats -->
      <div class="subsection">
        <h3 class="subsection-title">Total Earnings</h3>
        <div class="stats-grid">
          <div class="stat-card gold-card">
            <div class="stat-icon">💰</div>
            <div class="stat-value">{{ formatNumber(data.total.gold_earned) }}</div>
            <div class="stat-label">Total Gold Earned</div>
          </div>

          <div class="stat-card cs-card">
            <div class="stat-icon">🗡️</div>
            <div class="stat-value">{{ formatNumber(data.total.cs) }}</div>
            <div class="stat-label">Total CS (Creep Score)</div>
          </div>
        </div>
      </div>

      <!-- Average Stats -->
      <div class="subsection">
        <h3 class="subsection-title">Averages Per Game</h3>
        <div class="stats-grid-compact">
          <div class="stat-card-compact">
            <div class="stat-icon-small">💵</div>
            <div class="stat-content">
              <div class="stat-value-compact">{{ formatNumber(data.average.gold_earned) }}</div>
              <div class="stat-label-compact">Avg Gold / Game</div>
            </div>
          </div>

          <div class="stat-card-compact">
            <div class="stat-icon-small">⚔️</div>
            <div class="stat-content">
              <div class="stat-value-compact">{{ data.average.cs.toFixed(1) }}</div>
              <div class="stat-label-compact">Avg CS / Game</div>
            </div>
          </div>

          <div class="stat-card-compact highlight">
            <div class="stat-icon-small">📈</div>
            <div class="stat-content">
              <div class="stat-value-compact" :class="getCsPerMinClass(data.average.cs_per_min)">
                {{ data.average.cs_per_min.toFixed(2) }}
              </div>
              <div class="stat-label-compact">CS Per Minute</div>
              <div class="cs-rating">{{ getCsRating(data.average.cs_per_min) }}</div>
            </div>
          </div>
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
const props = defineProps({
  data: {
    type: Object,
    required: true
    },
  insights: {
    type: Array,
    default: () => []
  }
}
)

const formatNumber = (num) => {
  return num.toLocaleString()
}

const getCsPerMinClass = (cspm) => {
  if (cspm >= 8.0) return 'legendary'
  if (cspm >= 7.0) return 'excellent'
  if (cspm >= 6.0) return 'good'
  return 'average'
}

const getCsRating = (cspm) => {
  if (cspm >= 8.0) return 'Elite Farmer'
  if (cspm >= 7.0) return 'Great Farming'
  if (cspm >= 6.0) return 'Solid Performance'
  return 'Needs Practice'
}
</script>

<style scoped>
.economy-stats-section {
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
  background: linear-gradient(135deg, var(--lol-gold), #f0e68c);
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

.stats-grid-compact {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--lol-gold);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.3);
}

.gold-card {
  border-color: rgba(240, 230, 140, 0.5);
}

.cs-card {
  border-color: rgba(200, 155, 60, 0.5);
}

.stat-card-compact {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 15px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.stat-card-compact:hover {
  transform: translateY(-5px);
  border-color: var(--lol-gold);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.3);
}

.stat-card-compact.highlight {
  border-color: rgba(200, 155, 60, 0.6);
  background: rgba(200, 155, 60, 0.05);
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

.stat-value {
  font-size: 3rem;
  font-weight: 900;
  color: var(--lol-gold);
  margin-bottom: 0.5rem;
  text-shadow: 0 0 20px rgba(200, 155, 60, 0.5);
}

.stat-value-compact {
  font-size: 1.8rem;
  font-weight: 900;
  color: var(--lol-gold);
  margin-bottom: 0.3rem;
}

.stat-value-compact.legendary {
  color: #f0e68c;
  text-shadow: 0 0 20px #f0e68c;
}

.stat-value-compact.excellent {
  color: #00dfa2;
}

.stat-value-compact.good {
  color: #0397ab;
}

.stat-value-compact.average {
  color: var(--lol-gold);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
}

.stat-label-compact {
  font-size: 0.85rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.cs-rating {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: rgba(240, 230, 210, 0.7);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 700;
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

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid-compact {
    grid-template-columns: 1fr;
  }
}
</style>
