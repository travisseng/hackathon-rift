<template>
  <section class="section metrics-section">
    <div class="content-wrapper">
      <div class="tag">Performance Analytics</div>
      <h2 class="section-title">By The Numbers</h2>

      <div class="metrics-grid">
        <div class="metric-card featured">
          <div class="metric-label">Average KDA</div>
          <div class="metric-value">{{ data.kda_avg.toFixed(2) }}</div>
          <div class="metric-bar">
            <div class="metric-fill" :style="{ width: getKDAPercentage() + '%' }"></div>
          </div>
          <div class="metric-rating">{{ getKDARating() }}</div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">💰</div>
          <div class="metric-label">Avg Gold/Game</div>
          <div class="metric-value">{{ data.goldEarned_avg.toLocaleString() }}</div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">🌾</div>
          <div class="metric-label">CS per Minute</div>
          <div class="metric-value">{{ data.avg_cs_min.toFixed(1) }}</div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">💢</div>
          <div class="metric-label">Avg Damage Dealt</div>
          <div class="metric-value">{{ formatNumber(data.total_damage_to_champions_avg) }}</div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">🛡️</div>
          <div class="metric-label">Avg Damage Taken</div>
          <div class="metric-value">{{ formatNumber(data.totalDamageTaken_avg) }}</div>
        </div>

        <div class="metric-card highlight">
          <div class="metric-icon">💎</div>
          <div class="metric-label">Total Gold Earned</div>
          <div class="metric-value">{{ formatNumber(data.goldEarned) }}</div>
          <div class="metric-subtext">That's {{ (data.goldEarned / 2800).toFixed(0) }} Infinity Edges!</div>
        </div>
      </div>

      <div class="insights-section">
        <h3 class="insights-title">Performance Insights</h3>
        <div class="insights-grid">
          <div class="insight-card" v-for="i in 5" :key="i">
            <div class="insight-tag">{{ data[`tag_comment${i}`] }}</div>
            <p class="insight-text">{{ data[`comment${i}`] }}</p>
          </div>
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
  }
})

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toLocaleString()
}

const getKDAPercentage = () => {
  // Map KDA to percentage (5+ KDA = 100%)
  return Math.min((props.data.kda_avg / 5) * 100, 100)
}

const getKDARating = () => {
  const kda = props.data.kda_avg
  if (kda >= 5) return 'Legendary'
  if (kda >= 4) return 'Excellent'
  if (kda >= 3) return 'Great'
  if (kda >= 2) return 'Good'
  return 'Decent'
}
</script>

<style scoped>
.metrics-section {
  background: radial-gradient(circle at 50% 50%, rgba(200, 155, 60, 0.05) 0%, transparent 60%);
}

.content-wrapper {
  max-width: 1200px;
  width: 100%;
}

.tag {
  display: inline-block;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-gold-light));
  color: var(--lol-dark);
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 2rem;
  box-shadow: 0 5px 15px rgba(200, 155, 60, 0.3);
}

.section-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 900;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, var(--lol-gold-light), var(--lol-gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.metric-card {
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(10, 20, 40, 0.6));
  border: 2px solid rgba(200, 155, 60, 0.2);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(200, 155, 60, 0.1), transparent);
  transition: left 0.5s ease;
}

.metric-card:hover::before {
  left: 100%;
}

.metric-card:hover {
  transform: translateY(-5px);
  border-color: var(--lol-gold);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.3);
}

.metric-card.featured {
  grid-column: span 2;
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.15), rgba(3, 151, 171, 0.1));
  border-color: var(--lol-gold);
}

.metric-card.highlight {
  border-color: var(--lol-blue);
  background: linear-gradient(135deg, rgba(3, 151, 171, 0.15), rgba(30, 35, 40, 0.8));
}

.metric-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.metric-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 1rem;
  opacity: 0.9;
}

.metric-value {
  font-size: clamp(2.5rem, 4vw, 3.5rem);
  font-weight: 900;
  color: var(--lol-gold);
  margin-bottom: 0.5rem;
}

.metric-bar {
  width: 100%;
  height: 10px;
  background: rgba(200, 155, 60, 0.2);
  border-radius: 10px;
  overflow: hidden;
  margin: 1.5rem 0 1rem;
}

.metric-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--lol-gold), var(--lol-gold-light));
  border-radius: 10px;
  transition: width 2s ease;
}

.metric-rating {
  font-size: 1.1rem;
  color: var(--lol-gold-light);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.metric-subtext {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--lol-blue);
  font-weight: 600;
}

.insights-section {
  margin-top: 4rem;
}

.insights-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--lol-gold);
  margin-bottom: 2rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.insight-card {
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.05), rgba(30, 35, 40, 0.6));
  border-left: 4px solid var(--lol-gold);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.insight-card:hover {
  transform: translateX(5px);
  border-left-width: 6px;
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.1), rgba(30, 35, 40, 0.7));
}

.insight-tag {
  display: inline-block;
  background: var(--lol-gold);
  color: var(--lol-dark);
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}

.insight-text {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--lol-gold-light);
}

@media (max-width: 768px) {
  .metric-card.featured {
    grid-column: span 1;
  }

  .metrics-grid,
  .insights-grid {
    grid-template-columns: 1fr;
  }
}
</style>
