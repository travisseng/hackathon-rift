<template>
  <section class="section combat-stats-section">
    <div class="stats-container">
      <h2 class="section-title">Combat Performance</h2>

      <!-- KDA Overview -->
      <div class="kda-showcase">
        <div class="kda-stat">
          <div class="kda-icon">⚔️</div>
          <div class="kda-value">{{ data.total.kills }}</div>
          <div class="kda-label">Total Kills</div>
        </div>
        <div class="kda-separator">/</div>
        <div class="kda-stat">
          <div class="kda-icon">💀</div>
          <div class="kda-value">{{ data.total.deaths }}</div>
          <div class="kda-label">Total Deaths</div>
        </div>
        <div class="kda-separator">/</div>
        <div class="kda-stat">
          <div class="kda-icon">🤝</div>
          <div class="kda-value">{{ data.total.assists }}</div>
          <div class="kda-label">Total Assists</div>
        </div>
      </div>

      <!-- Average KDA -->
      <div class="average-kda-card">
        <div class="average-label">Average KDA</div>
        <div class="average-kda-value" :class="getKdaClass(data.average.kda)">
          {{ data.average.kda.toFixed(2) }}
        </div>
        <div class="average-breakdown">
          {{ data.average.kills.toFixed(1) }} /
          {{ data.average.deaths.toFixed(1) }} /
          {{ data.average.assists.toFixed(1) }}
        </div>
      </div>

      <!-- Multikills & Achievements -->
      <div class="subsection">
        <h3 class="subsection-title">Epic Moments</h3>
        <div class="stats-grid">
          <div class="stat-card achievement-card">
            <div class="stat-icon">🩸</div>
            <div class="stat-value">{{ data.total.first_bloods }}</div>
            <div class="stat-label">First Bloods</div>
          </div>

          <div class="stat-card achievement-card triple">
            <div class="stat-icon">🔥</div>
            <div class="stat-value">{{ data.total.triple_kills }}</div>
            <div class="stat-label">Triple Kills</div>
          </div>

          <div class="stat-card achievement-card quadra">
            <div class="stat-icon">⚡</div>
            <div class="stat-value">{{ data.total.quadra_kills }}</div>
            <div class="stat-label">Quadra Kills</div>
          </div>

          <div class="stat-card achievement-card penta">
            <div class="stat-icon">👑</div>
            <div class="stat-value">{{ data.total.penta_kills }}</div>
            <div class="stat-label">Penta Kills</div>
            <div class="penta-message" v-if="data.total.penta_kills === 0">
              So close yet so far...
            </div>
            <div class="penta-message legendary" v-else>
              LEGENDARY!
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
})

const getKdaClass = (kda) => {
  if (kda >= 4.0) return 'legendary'
  if (kda >= 3.0) return 'excellent'
  if (kda >= 2.0) return 'good'
  return 'average'
}
</script>

<style scoped>
.combat-stats-section {
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

/* KDA Showcase */
.kda-showcase {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  padding: 3rem 2rem;
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 70, 85, 0.3);
  border-radius: 20px;
  margin-bottom: 2rem;
}

.kda-stat {
  text-align: center;
  flex: 1;
  max-width: 200px;
}

.kda-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.kda-value {
  font-size: 3.5rem;
  font-weight: 900;
  color: #ff4655;
  text-shadow: 0 0 20px rgba(255, 70, 85, 0.5);
  margin-bottom: 0.5rem;
}

.kda-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
}

.kda-separator {
  font-size: 3rem;
  font-weight: 300;
  color: rgba(255, 70, 85, 0.5);
}

/* Average KDA Card */
.average-kda-card {
  text-align: center;
  padding: 2.5rem;
  background: rgba(10, 20, 40, 0.8);
  backdrop-filter: blur(10px);
  border: 3px solid rgba(200, 155, 60, 0.5);
  border-radius: 20px;
  margin-bottom: 3rem;
  position: relative;
  overflow: hidden;
}

.average-kda-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, transparent, var(--lol-gold), transparent);
}

.average-label {
  font-size: 1.2rem;
  color: var(--lol-gold);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
  margin-bottom: 1rem;
}

.average-kda-value {
  font-size: 5rem;
  font-weight: 900;
  margin-bottom: 1rem;
  text-shadow: 0 0 30px currentColor;
}

.average-kda-value.legendary {
  color: #f0e68c;
  text-shadow: 0 0 30px #f0e68c, 0 0 60px #daa520;
}

.average-kda-value.excellent {
  color: #00dfa2;
}

.average-kda-value.good {
  color: #0397ab;
}

.average-kda-value.average {
  color: var(--lol-gold);
}

.average-breakdown {
  font-size: 1.5rem;
  color: var(--lol-gold-light);
  font-weight: 600;
}

/* Subsection */
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
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 70, 85, 0.3);
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(255, 70, 85, 0.3);
}

.achievement-card.triple {
  border-color: rgba(255, 140, 0, 0.5);
}

.achievement-card.quadra {
  border-color: rgba(200, 155, 60, 0.6);
}

.achievement-card.penta {
  border-color: rgba(240, 230, 140, 0.7);
  background: rgba(240, 230, 140, 0.02);
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.stat-value {
  font-size: 3rem;
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
}

.penta-message {
  margin-top: 0.8rem;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: rgba(240, 230, 210, 0.6);
  font-style: italic;
}

.penta-message.legendary {
  color: #f0e68c;
  font-size: 1rem;
  font-style: normal;
  text-shadow: 0 0 10px #f0e68c;
}

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
  background: linear-gradient(135deg, rgba(255, 70, 85, 0.2), rgba(255, 70, 85, 0.3));
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

@media (max-width: 768px) {
  .stats-container {
    padding: 1rem;
  }

  .kda-showcase {
    flex-direction: column;
    gap: 1.5rem;
    padding: 2rem 1rem;
  }

  .kda-separator {
    transform: rotate(90deg);
    font-size: 2rem;
  }

  .kda-value {
    font-size: 2.5rem;
  }

  .average-kda-value {
    font-size: 3.5rem;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
}
</style>
