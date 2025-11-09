<template>
  <section class="section vision-stats-section">
    <div class="stats-container">
      <h2 class="section-title">Vision Control</h2>

      <!-- Vision Stats -->
      <div class="stats-grid">
        <div class="stat-card vision">
          <div class="stat-icon">🔮</div>
          <div class="stat-value">{{ formatNumber(data.total.vision_score) }}</div>
          <div class="stat-label">Total Vision Score</div>
          <div class="stat-avg">{{ data.average.vision_score.toFixed(1) }} avg</div>
        </div>

        <div class="stat-card wards-placed">
          <div class="stat-icon">📍</div>
          <div class="stat-value">{{ formatNumber(data.total.wards_placed) }}</div>
          <div class="stat-label">Wards Placed</div>
          <div class="stat-avg">{{ data.average.wards_placed.toFixed(1) }} avg</div>
        </div>

        <div class="stat-card wards-killed">
          <div class="stat-icon">🎯</div>
          <div class="stat-value">{{ formatNumber(data.total.wards_killed) }}</div>
          <div class="stat-label">Wards Destroyed</div>
          <div class="stat-avg">{{ data.average.wards_killed.toFixed(1) }} avg</div>
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
</script>

<style scoped>
.vision-stats-section {
  background: radial-gradient(circle at center, rgba(145, 116, 255, 0.1) 0%, transparent 70%);
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
  background: linear-gradient(135deg, #9174ff, #c89bff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(145, 116, 255, 0.3);
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: #9174ff;
  box-shadow: 0 10px 30px rgba(145, 116, 255, 0.3);
}

.vision {
  border-color: rgba(145, 116, 255, 0.5);
}

.wards-placed {
  border-color: rgba(0, 223, 162, 0.5);
}

.wards-killed {
  border-color: rgba(255, 140, 0, 0.5);
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 900;
  color: #9174ff;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 20px rgba(145, 116, 255, 0.5);
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
  border: 1px solid rgba(145, 116, 255, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.insight-item:hover {
  border-color: rgba(145, 116, 255, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(145, 116, 255, 0.2);
}

.insight-tag {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: linear-gradient(135deg, rgba(145, 116, 255, 0.2), rgba(200, 155, 255, 0.2));
  border: 1px solid rgba(145, 116, 255, 0.4);
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #c89bff;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(145, 116, 255, 0.15);
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
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }

  .insight-item {
    padding: 1rem;
  }
}
</style>
