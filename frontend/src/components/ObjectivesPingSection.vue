<template>
  <section class="section objectives-ping-section">
    <div class="stats-container">
      <h2 class="section-title">Objectives & Communication</h2>

      <!-- Objectives Stats -->
      <div class="subsection">
        <h3 class="subsection-title">🐉 Epic Objectives</h3>
        <div class="stats-grid-large">
          <div class="stat-card dragon">
            <div class="stat-icon">🐲</div>
            <div class="stat-value">{{ objectivesData.total.dragon_takedowns }}</div>
            <div class="stat-label">Dragon Takedowns</div>
            <div class="stat-avg">{{ objectivesData.average.dragon_takedowns.toFixed(2) }} per game</div>
          </div>

          <div class="stat-card baron">
            <div class="stat-icon">👹</div>
            <div class="stat-value">{{ objectivesData.total.baron_kills }}</div>
            <div class="stat-label">Baron Kills</div>
            <div class="stat-avg">{{ objectivesData.average.baron_kills.toFixed(2) }} per game</div>
          </div>
        </div>
      </div>

      <!-- Ping Stats -->
      <div class="subsection">
        <h3 class="subsection-title">📡 Communication Pings</h3>
        <div class="ping-grid">
          <div class="ping-item" v-for="(count, pingType) in getTopPings()" :key="pingType">
            <div class="ping-icon">{{ getPingIcon(pingType) }}</div>
            <div class="ping-content">
              <div class="ping-count">{{ count }}</div>
              <div class="ping-label">{{ formatPingType(pingType) }}</div>
            </div>
          </div>
        </div>
        <div class="ping-total">
          Total Pings: {{ getTotalPings() }}
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
  objectivesData: {
    type: Object,
    required: true
  },
  pingData: {
    type: Object,
    required: true
  },
  insights: {
    type: Array,
    default: () => []
  }
})

const getTopPings = () => {
  const entries = Object.entries(props.pingData.total)
  const filtered = entries.filter(([key, value]) => value > 0)
  filtered.sort((a, b) => b[1] - a[1])
  return Object.fromEntries(filtered.slice(0, 8))
}

const getTotalPings = () => {
  return Object.values(props.pingData.total).reduce((sum, val) => sum + val, 0)
}

const formatPingType = (type) => {
  return type.split('_').map(word =>
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

const getPingIcon = (type) => {
  const icons = {
    'all_in': '⚡',
    'assist_me': '🆘',
    'command': '📢',
    'danger': '⚠️',
    'enemy_missing': '❓',
    'enemy_vision': '👁️',
    'get_back': '↩️',
    'on_my_way': '🏃',
    'retreat': '🏃‍♂️',
    'need_vision': '🔍',
    'push': '➡️',
    'hold': '✋',
    'vision_cleared': '✅',
    'basic': '📍'
  }
  return icons[type] || '📌'
}
</script>

<style scoped>
.objectives-ping-section {
  background: radial-gradient(circle at center, rgba(0, 223, 162, 0.1) 0%, transparent 70%);
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
  background: linear-gradient(135deg, #00dfa2, #0397ab);
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

.stats-grid-large {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.stat-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(0, 223, 162, 0.3);
  border-radius: 15px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: #00dfa2;
  box-shadow: 0 10px 30px rgba(0, 223, 162, 0.3);
}

.dragon {
  border-color: rgba(255, 140, 0, 0.5);
}

.baron {
  border-color: rgba(145, 116, 255, 0.5);
}

.stat-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.stat-value {
  font-size: 4rem;
  font-weight: 900;
  color: #00dfa2;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 30px rgba(0, 223, 162, 0.5);
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

/* Ping Grid */
.ping-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.ping-item {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(0, 223, 162, 0.3);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.ping-item:hover {
  transform: translateY(-3px);
  border-color: #00dfa2;
  box-shadow: 0 8px 20px rgba(0, 223, 162, 0.3);
}

.ping-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.ping-content {
  flex: 1;
  text-align: left;
}

.ping-count {
  font-size: 1.5rem;
  font-weight: 900;
  color: #00dfa2;
  margin-bottom: 0.2rem;
}

.ping-label {
  font-size: 0.8rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.ping-total {
  text-align: center;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--lol-gold);
  padding: 1rem;
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(0, 223, 162, 0.3);
  border-radius: 10px;
}

/* Comment Section */
.comment-section {
  margin-top: 3rem;
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(0, 223, 162, 0.3);
  border-radius: 15px;
  padding: 2rem;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(0, 223, 162, 0.2);
}

.comment-icon {
  font-size: 1.5rem;
}

.comment-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #00dfa2;
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
  background: rgba(0, 223, 162, 0.05);
  border-left: 4px solid #00dfa2;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.insight-item:hover {
  background: rgba(0, 223, 162, 0.1);
  transform: translateX(5px);
}

.insight-tag {
  font-size: 0.9rem;
  font-weight: 700;
  color: #0397ab;
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

  .stats-grid-large {
    grid-template-columns: 1fr;
  }

  .ping-grid {
    grid-template-columns: 1fr;
  }
}
</style>
