<template>
  <section class="section deaths-section">
    <div class="content-wrapper">
      <div class="tag">{{ data.tag_comment1 }}</div>
      <h2 class="section-title">Gray Screen Moments</h2>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">💀</div>
          <div class="stat-value">{{ data.count_dead }}</div>
          <div class="stat-label">Total Deaths</div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">⏳</div>
          <div class="stat-value">{{ formatTime(data.time_dead) }}</div>
          <div class="stat-label">Time Dead</div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">⚰️</div>
          <div class="stat-value">{{ data.longest_time_spent_dead_in_one_game }}s</div>
          <div class="stat-label">Most Time Spent Dead in a Single Game</div>
        </div>
      </div>

      <div class="comment-boxes">
        <div class="comment-box">
          <div class="comment-tag">{{ data.tag_comment1 }}</div>
          <p class="comment">{{ data.comment1 }}</p>
        </div>
        <div class="comment-box">
          <div class="comment-tag">{{ data.tag_comment2 }}</div>
          <p class="comment">{{ data.comment2 }}</p>
        </div>
      </div>


    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${hours}h ${minutes}m ${secs}s`
}

const deathCircleOffset = computed(() => {
  const deathsPerHour = props.data.count_dead / (props.data.time_dead / 3600)
  const percentage = Math.min(deathsPerHour / 10, 1) // Normalize to 0-1 range
  const circumference = 2 * Math.PI * 45
  return circumference * (1 - percentage)
})
</script>

<style scoped>
.deaths-section {
  background: radial-gradient(circle at 30% 70%, rgba(209, 54, 57, 0.05) 0%, transparent 50%);
}

.content-wrapper {
  max-width: 1200px;
  width: 100%;
}

.tag {
  display: inline-block;
  background: linear-gradient(135deg, var(--lol-red), #8B0000);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 2rem;
  box-shadow: 0 5px 15px rgba(209, 54, 57, 0.3);
}

.section-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 900;
  margin-bottom: 3rem;
  color: var(--lol-gold-light);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(10, 20, 40, 0.6));
  border: 2px solid rgba(209, 54, 57, 0.3);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--lol-red);
  box-shadow: 0 10px 30px rgba(209, 54, 57, 0.3);
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  filter: grayscale(50%);
}

.stat-value {
  font-size: clamp(2.5rem, 4vw, 3.5rem);
  font-weight: 900;
  color: var(--lol-red);
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.8;
}

.comment-boxes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.comment-box {
  background: linear-gradient(135deg, rgba(209, 54, 57, 0.1), rgba(30, 35, 40, 0.5));
  border-left: 4px solid var(--lol-red);
  border-radius: 10px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.comment-tag {
  font-size: 0.9rem;
  color: var(--lol-red);
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.comment {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--lol-gold-light);
}

.death-visual {
  display: flex;
  justify-content: center;
  margin-top: 3rem;
}

.respawn-timer {
  text-align: center;
}

.timer-circle {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto 1rem;
}

.timer-circle svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.timer-bg {
  fill: none;
  stroke: rgba(209, 54, 57, 0.2);
  stroke-width: 8;
}

.timer-progress {
  fill: none;
  stroke: var(--lol-red);
  stroke-width: 8;
  stroke-linecap: round;
  stroke-dasharray: 283;
  transition: stroke-dashoffset 2s ease;
}

.timer-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--lol-red);
}

.timer-label {
  font-size: 1.1rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

@media (max-width: 768px) {
  .stats-grid,
  .comment-boxes {
    grid-template-columns: 1fr;
  }
}
</style>
