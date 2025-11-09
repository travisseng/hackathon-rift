<template>
  <section class="section objectives-section">
    <div class="stats-container">
      <h2 class="section-title">Epic Objectives</h2>

      <!-- Objectives Stats -->
      <div class="stats-grid-large">
        <div class="stat-card dragon">
          <div class="stat-icon-container">
            <img
              src="https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/3/34/Elder_DragonSquare.png"
              alt="Dragon"
              class="stat-icon-image"
            />
          </div>
          <div class="stat-value">{{ data.total.dragon_takedowns }}</div>
          <div class="stat-label">Dragon Takedowns</div>
          <div class="stat-avg">{{ data.average.dragon_takedowns.toFixed(2) }} per game</div>
        </div>

        <div class="stat-card baron">
          <div class="stat-icon-container">
            <img
              src="https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/3/38/Baron_NashorSquare.png"
              alt="Baron Nashor"
              class="stat-icon-image"
            />
          </div>
          <div class="stat-value">{{ data.total.baron_kills }}</div>
          <div class="stat-label">Baron Kills</div>
          <div class="stat-avg">{{ data.average.baron_kills.toFixed(2) }} per game</div>
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
</script>

<style scoped>
.section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
}

.objectives-section {
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

.stats-grid-large {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 15px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--lol-gold);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.3);
}

.dragon {
  border-color: rgba(255, 140, 0, 0.5);
}

.baron {
  border-color: rgba(145, 116, 255, 0.5);
}

.stat-icon-container {
  width: 100px;
  height: 100px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--lol-gold);
  box-shadow: 0 4px 20px rgba(200, 155, 60, 0.5);
  transition: all 0.3s ease;
}

.stat-card:hover .stat-icon-container {
  transform: scale(1.1);
  box-shadow: 0 6px 30px rgba(200, 155, 60, 0.7);
}

.stat-icon-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.stat-value {
  font-size: 4rem;
  font-weight: 900;
  color: var(--lol-gold);
  margin-bottom: 0.5rem;
  text-shadow: 0 0 30px rgba(200, 155, 60, 0.5);
}

.stat-label {
  font-size: 1rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.stat-avg {
  font-size: 0.85rem;
  color: rgba(240, 230, 210, 0.6);
  margin-top: 0.8rem;
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
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.2), rgba(240, 230, 140, 0.2));
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

  .stats-grid-large {
    grid-template-columns: 1fr;
  }

  .insight-item {
    padding: 1rem;
  }
}
</style>
