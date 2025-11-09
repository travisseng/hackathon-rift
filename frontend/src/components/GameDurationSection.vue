<template>
  <section class="section game-duration-section">
    <div class="content-wrapper">
      <div class="tag">{{ data.tag_comment1 }}</div>
      <h2 class="section-title">Time in the Rift</h2>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">🎮</div>
          <div class="stat-value">{{ data.gameplayed }}</div>
          <div class="stat-label">Games Played</div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">⏱️</div>
          <div class="stat-value">{{ formatTime(data.timespend) }}</div>
          <div class="stat-label">Total Time Played</div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">⚔️</div>
          <div class="stat-value">{{ data.longest_game.split('minute(s)')[0].split('hour(s)')[1].trim() }}min</div>
          <div class="stat-label">Longest Game</div>
        </div>

        <div class="stat-card highlight">
          <div class="stat-icon">🏆</div>
          <div class="stat-value">{{ (data.winrate * 100).toFixed(0) }}%</div>
          <div class="stat-label">Win Rate</div>
          <div class="win-loss">{{ getWins(data.victory) }}W - {{ getLosses(data.victory) }}L</div>
        </div>
      </div>

      <div class="comment-box">
        <p class="comment">{{ data.comment1 }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  data: {
    type: Object,
    required: true
  }
})

const formatTime = (seconds) => {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${days}d ${hours}h ${minutes}m ${secs}s`
}

const getWins = (victory) => {
  return victory.true || victory['true'] || 0
}

const getLosses = (victory) => {
  return victory.false || victory['false'] || 0
}
</script>

<style scoped>
.game-duration-section {
  background: radial-gradient(circle at 30% 50%, rgba(200, 155, 60, 0.05) 0%, transparent 50%);
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(10, 20, 40, 0.6));
  border: 2px solid rgba(200, 155, 60, 0.2);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--lol-gold);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.3);
}

.stat-card.highlight {
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.2), rgba(3, 151, 171, 0.1));
  border-color: var(--lol-gold);
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.stat-value {
  font-size: clamp(2.5rem, 4vw, 3.5rem);
  font-weight: 900;
  color: var(--lol-gold);
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.8;
}

.win-loss {
  margin-top: 0.5rem;
  font-size: 1.1rem;
  color: var(--lol-green);
  font-weight: 600;
}

.comment-box {
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.1), rgba(3, 151, 171, 0.05));
  border-left: 4px solid var(--lol-gold);
  border-radius: 10px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.comment {
  font-size: 1.2rem;
  line-height: 1.6;
  color: var(--lol-gold-light);
  font-style: italic;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
