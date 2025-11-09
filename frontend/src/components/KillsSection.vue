<template>
  <section class="section kills-section">
    <div class="content-wrapper">
      <div class="tag">{{ data.tag_comment2 }}</div>
      <h2 class="section-title">Domination Stats</h2>

      <div class="main-stats">
        <div class="big-stat">
          <div class="big-stat-icon">⚔️</div>
          <div class="big-stat-value">{{ data.kills.toLocaleString() }}</div>
          <div class="big-stat-label">Total Kills</div>
        </div>
        <div class="big-stat">
          <div class="big-stat-icon">🤝</div>
          <div class="big-stat-value">{{ data.assists.toLocaleString() }}</div>
          <div class="big-stat-label">Total Assists</div>
        </div>
      </div>

      <div class="multikills-section">
        <h3 class="subsection-title">Multikill Highlights</h3>
        <div class="multikills-grid">
          <div class="multikill-card" :class="{ 'achieved': data.firstbloodkills > 0 }">
            <div class="multikill-icon">🩸</div>
            <div class="multikill-count">{{ data.firstbloodkills }}</div>
            <div class="multikill-name">First Bloods</div>
          </div>
          <div class="multikill-card" :class="{ 'achieved': data.triple_kills > 0 }">
            <div class="multikill-icon">🔥</div>
            <div class="multikill-count">{{ data.triple_kills }}</div>
            <div class="multikill-name">Triple Kills</div>
          </div>
          <div class="multikill-card" :class="{ 'achieved': data.quadra_kills > 0 }">
            <div class="multikill-icon">💥</div>
            <div class="multikill-count">{{ data.quadra_kills }}</div>
            <div class="multikill-name">Quadra Kills</div>
          </div>
          <div class="multikill-card" :class="{ 'achieved': data.penta_kills > 0, 'legendary': data.penta_kills > 0 }">
            <div class="multikill-icon">👑</div>
            <div class="multikill-count">{{ data.penta_kills }}</div>
            <div class="multikill-name">Penta Kills</div>
          </div>
        </div>
      </div>

      <div class="comments-grid">
        <div class="comment-card" v-for="i in 4" :key="i">
          <div class="comment-header">
            <div class="comment-tag">{{ data[`tag_comment${i}`] }}</div>
          </div>
          <p class="comment-text">{{ data[`comment${i}`] }}</p>
        </div>
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
</script>

<style scoped>
.kills-section {
  background: radial-gradient(circle at 70% 30%, rgba(10, 200, 185, 0.05) 0%, transparent 50%);
}

.content-wrapper {
  max-width: 1200px;
  width: 100%;
}

.tag {
  display: inline-block;
  background: linear-gradient(135deg, var(--lol-green), var(--lol-blue));
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 2rem;
  box-shadow: 0 5px 15px rgba(10, 200, 185, 0.3);
}

.section-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 900;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, var(--lol-green), var(--lol-gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.main-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.big-stat {
  background: linear-gradient(135deg, rgba(10, 200, 185, 0.15), rgba(30, 35, 40, 0.8));
  border: 3px solid var(--lol-green);
  border-radius: 25px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.big-stat::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(10, 200, 185, 0.1) 0%, transparent 70%);
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.big-stat:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 50px rgba(10, 200, 185, 0.4);
}

.big-stat-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  position: relative;
  z-index: 1;
}

.big-stat-value {
  font-size: clamp(3.5rem, 6vw, 5rem);
  font-weight: 900;
  color: var(--lol-green);
  margin-bottom: 0.5rem;
  position: relative;
  z-index: 1;
}

.big-stat-label {
  font-size: 1.2rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  position: relative;
  z-index: 1;
}

.multikills-section {
  margin-bottom: 3rem;
}

.subsection-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--lol-gold);
  margin-bottom: 2rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.multikills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.multikill-card {
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(10, 20, 40, 0.6));
  border: 2px solid rgba(91, 90, 86, 0.3);
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  opacity: 0.5;
}

.multikill-card.achieved {
  opacity: 1;
  border-color: var(--lol-green);
}

.multikill-card.legendary {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(200, 155, 60, 0.1));
  border-color: #FFD700;
  box-shadow: 0 10px 40px rgba(255, 215, 0, 0.3);
  animation: legendary-glow 2s ease-in-out infinite;
}

@keyframes legendary-glow {
  0%, 100% { box-shadow: 0 10px 40px rgba(255, 215, 0, 0.3); }
  50% { box-shadow: 0 15px 60px rgba(255, 215, 0, 0.6); }
}

.multikill-card:hover {
  transform: translateY(-5px);
}

.multikill-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.multikill-count {
  font-size: 3rem;
  font-weight: 900;
  color: var(--lol-green);
  margin-bottom: 0.5rem;
}

.multikill-card.legendary .multikill-count {
  color: #FFD700;
}

.multikill-name {
  font-size: 1rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
}

.comments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.comment-card {
  background: linear-gradient(135deg, rgba(10, 200, 185, 0.05), rgba(30, 35, 40, 0.6));
  border-left: 4px solid var(--lol-green);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.comment-card:hover {
  transform: translateX(5px);
  border-left-width: 6px;
  background: linear-gradient(135deg, rgba(10, 200, 185, 0.1), rgba(30, 35, 40, 0.7));
}

.comment-header {
  margin-bottom: 1rem;
}

.comment-tag {
  display: inline-block;
  background: var(--lol-green);
  color: var(--lol-dark);
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.comment-text {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--lol-gold-light);
}

@media (max-width: 768px) {
  .main-stats,
  .multikills-grid,
  .comments-grid {
    grid-template-columns: 1fr;
  }
}
</style>
