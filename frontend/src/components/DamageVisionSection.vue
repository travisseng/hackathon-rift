<template>
  <section class="section damage-vision-section">
    <div class="stats-container">
      <h2 class="section-title">Damage & Vision</h2>

      <!-- Damage Stats -->
      <div class="subsection">
        <h3 class="subsection-title">💥 Damage Statistics</h3>
        <div class="stats-grid">
          <div class="stat-card damage-dealt">
            <div class="stat-icon">⚔️</div>
            <div class="stat-value">{{ formatNumber(damageData.total.damage_dealt) }}</div>
            <div class="stat-label">Total Damage Dealt</div>
            <div class="stat-avg">{{ formatNumber(damageData.average.damage_dealt) }} avg</div>
          </div>

          <div class="stat-card damage-taken">
            <div class="stat-icon">🛡️</div>
            <div class="stat-value">{{ formatNumber(damageData.total.damage_taken) }}</div>
            <div class="stat-label">Total Damage Taken</div>
            <div class="stat-avg">{{ formatNumber(damageData.average.damage_taken) }} avg</div>
          </div>

          <div class="stat-card healing">
            <div class="stat-icon">💚</div>
            <div class="stat-value">{{ formatNumber(damageData.total.healing_done) }}</div>
            <div class="stat-label">Total Healing</div>
            <div class="stat-avg">{{ formatNumber(damageData.average.healing_done) }} avg</div>
          </div>

          <div class="stat-card healing-team">
            <div class="stat-icon">💝</div>
            <div class="stat-value">{{ formatNumber(damageData.total.healing_teammates) }}</div>
            <div class="stat-label">Healing Teammates</div>
            <div class="stat-avg">{{ formatNumber(damageData.average.healing_teammates) }} avg</div>
          </div>

          <div class="stat-card cc">
            <div class="stat-icon">🌀</div>
            <div class="stat-value">{{ formatSeconds(damageData.total.cc_time) }}</div>
            <div class="stat-label">Total CC Time</div>
            <div class="stat-avg">{{ damageData.average.cc_time.toFixed(1) }}s avg</div>
          </div>
        </div>
      </div>

      <!-- Vision Stats -->
      <div class="subsection">
        <h3 class="subsection-title">👁️ Vision Control</h3>
        <div class="stats-grid">
          <div class="stat-card vision">
            <div class="stat-icon">🔮</div>
            <div class="stat-value">{{ formatNumber(visionData.total.vision_score) }}</div>
            <div class="stat-label">Total Vision Score</div>
            <div class="stat-avg">{{ visionData.average.vision_score.toFixed(1) }} avg</div>
          </div>

          <div class="stat-card wards-placed">
            <div class="stat-icon">📍</div>
            <div class="stat-value">{{ formatNumber(visionData.total.wards_placed) }}</div>
            <div class="stat-label">Wards Placed</div>
            <div class="stat-avg">{{ visionData.average.wards_placed.toFixed(1) }} avg</div>
          </div>

          <div class="stat-card wards-killed">
            <div class="stat-icon">🎯</div>
            <div class="stat-value">{{ formatNumber(visionData.total.wards_killed) }}</div>
            <div class="stat-label">Wards Destroyed</div>
            <div class="stat-avg">{{ visionData.average.wards_killed.toFixed(1) }} avg</div>
          </div>
        </div>
      </div>

      <!-- Comment Section -->
      <div class="comment-section">
        <div v-if="insights && insights.length > 0" class="insights-list">
          <div v-for="(insight, index) in insights" :key="index" class="insight-item">
            <div class="insight-tag">{{ insight.tag }}</div>
            <div class="insight-comment">{{ insight.comment }}</div>
          </div>
        </div>
        <div v-else class="comment-placeholder">
          Analysis will appear here...
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  damageData: {
    type: Object,
    required: true
  },
  visionData: {
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
.damage-vision-section {
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

/* Comment Section */
.comment-section {
  margin-top: 3rem;
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(145, 116, 255, 0.3);
  border-radius: 15px;
  padding: 2rem;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(145, 116, 255, 0.2);
}

.comment-icon {
  font-size: 1.5rem;
}

.comment-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #9174ff;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.comment-placeholder {
  color: rgba(240, 230, 210, 0.5);
  font-style: italic;
  line-height: 1.6;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.insights-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.insight-item {
  padding: 1rem 1.5rem;
  background: rgba(145, 116, 255, 0.05);
  border-left: 4px solid #9174ff;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.insight-item:hover {
  background: rgba(145, 116, 255, 0.1);
  transform: translateX(5px);
}

.insight-tag {
  font-size: 0.9rem;
  font-weight: 700;
  color: #c89bff;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.insight-comment {
  font-size: 1rem;
  color: var(--lol-gold-light);
  line-height: 1.6;
}


@media (max-width: 768px) {
  .stats-container {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
}
</style>
