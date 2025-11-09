<template>
  <section class="section communication-section">
    <div class="stats-container">
      <h2 class="section-title">Communication Pings</h2>

      <!-- Ping Stats -->
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

const getTopPings = () => {
  const entries = Object.entries(props.data.total)
  const filtered = entries.filter(([key, value]) => value > 0)
  filtered.sort((a, b) => b[1] - a[1])
  return Object.fromEntries(filtered.slice(0, 8))
}

const getTotalPings = () => {
  return Object.values(props.data.total).reduce((sum, val) => sum + val, 0)
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
.section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
}

.communication-section {
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
  margin-bottom: 3rem;
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
  border: 1px solid rgba(0, 223, 162, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.insight-item:hover {
  border-color: rgba(0, 223, 162, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 223, 162, 0.2);
}

.insight-tag {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: linear-gradient(135deg, rgba(0, 223, 162, 0.2), rgba(3, 151, 171, 0.2));
  border: 1px solid rgba(0, 223, 162, 0.4);
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #00dfa2;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0, 223, 162, 0.15);
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

  .ping-grid {
    grid-template-columns: 1fr;
  }

  .insight-item {
    padding: 1rem;
  }
}
</style>
