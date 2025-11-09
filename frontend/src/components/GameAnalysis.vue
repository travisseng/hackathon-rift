<template>
  <section class="section analysis-section">
    <div class="analysis-wrapper">
      <!-- Back Button -->
      <button class="back-btn" @click="$emit('back')">
        <span>←</span> Back to Games
      </button>

      <!-- Game Header -->
      <div class="game-header">
        <div class="header-left">
          <img :src="getChampionIcon(analysisData.player.champion)" :alt="analysisData.player.champion" class="header-champion-icon" />
          <div class="header-info">
            <h1 class="header-champion-name">{{ analysisData.player.champion }}</h1>
            <div class="header-role">{{ formatRole(analysisData.player.role) }}</div>
            <div class="player-tags" v-if="analysisData.final_verdict.tags && analysisData.final_verdict.tags.length > 0">
              <span v-for="(tag, idx) in analysisData.final_verdict.tags" :key="idx" class="tag-badge">{{ tag }}</span>
            </div>
          </div>
        </div>
        <div class="header-grade">
          <div class="grade-badge" :class="'grade-' + convertScoreToGrade(analysisData.final_verdict.score).toLowerCase()">
            {{ convertScoreToGrade(analysisData.final_verdict.score) }}
          </div>
          <div class="grade-label">Overall Grade</div>
        </div>
      </div>

      <!-- Game Stats -->
      <div class="game-stats-overview" v-if="gameData">
        <div class="stats-main">
          <div class="stat-kda">
            <div class="kda-numbers">{{ gameData.player.stats.kills }}/{{ gameData.player.stats.deaths }}/{{ gameData.player.stats.assists }}</div>
            <div class="kda-ratio">{{ calculateKDA(gameData.player.stats.kills, gameData.player.stats.deaths, gameData.player.stats.assists) }} KDA</div>
          </div>
          <div class="stat-item-horizontal">
            <span class="stat-icon">💰</span>
            <span class="stat-value">{{ formatGold(gameData.player.stats.goldEarned) }}</span>
          </div>
          <div class="stat-item-horizontal">
            <span class="stat-icon">🌾</span>
            <span class="stat-value">{{ gameData.player.stats.totalMinionsKilled + gameData.player.stats.neutralMinionsKilled }} CS ({{ calculateCSPerMin(gameData.player.stats.totalMinionsKilled + gameData.player.stats.neutralMinionsKilled, gameData.duration) }}/min)</span>
          </div>
          <div class="stat-item-horizontal">
            <span class="stat-icon">👁️</span>
            <span class="stat-value">{{ gameData.player.stats.visionScore }} Vision</span>
          </div>
        </div>

        <!-- Opponent Stats (if available) -->
        <div class="opponent-stats-overview" v-if="gameData.opponent">
          <div class="opponent-header">
            <span class="vs-label">VS</span>
            <img :src="getChampionIcon(gameData.opponent.champion)" :alt="gameData.opponent.champion" class="opponent-icon-small" />
            <div class="opponent-name-info">
              <div class="opponent-name">{{ gameData.opponent.name }}</div>
              <div class="opponent-champion">{{ gameData.opponent.champion }}</div>
            </div>
          </div>
          <div class="opponent-kda" v-if="gameData.opponent.stats">
            <span class="opponent-kda-numbers">{{ gameData.opponent.stats.kills }}/{{ gameData.opponent.stats.deaths }}/{{ gameData.opponent.stats.assists }}</span>
            <div class="opponent-mini-stats">
              <span>💰 {{ formatGold(gameData.opponent.stats.goldEarned) }}</span>
              <span>🌾 {{ gameData.opponent.stats.totalMinionsKilled + gameData.opponent.stats.neutralMinionsKilled }} CS ({{ calculateCSPerMin(gameData.opponent.stats.totalMinionsKilled + gameData.opponent.stats.neutralMinionsKilled, gameData.duration) }}/min)</span>
              <span>👁️ {{ gameData.opponent.stats.visionScore }} Vision</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Phase Analysis -->
      <div class="section-header">
        <h2 class="section-title-analysis">Game Phase Analysis</h2>
      </div>
      <div class="phase-grid">
        <div v-for="(phase, key) in analysisData.phase_analysis" :key="key" class="phase-card">
          <div class="phase-header">
            <h3 class="phase-name">{{ formatPhase(key) }}</h3>
            <div class="phase-rating-grade" :class="'grade-' + convertScoreToGrade(phase.rating || phase.rating_grade).toLowerCase()">
              {{ convertScoreToGrade(phase.rating || phase.rating_grade) }}
            </div>
          </div>
          <div class="phase-title">{{ phase.title }}</div>

          <div class="phase-strengths">
            <div class="list-header strengths-header">
              <span class="icon">✓</span> Strengths
            </div>
            <ul class="strengths-list">
              <li v-for="(strength, idx) in phase.strengths" :key="idx">{{ strength }}</li>
            </ul>
          </div>

          <div class="phase-issues">
            <div class="list-header issues-header">
              <span class="icon">✗</span> Issues
            </div>
            <ul class="issues-list">
              <li v-for="(issue, idx) in phase.issues" :key="idx">{{ issue }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Global Overview -->
      <div class="section-header">
        <h2 class="section-title-analysis">Performance Overview</h2>
      </div>
      <div class="overview-grid">
        <!-- Strengths -->
        <div class="overview-column strengths-column">
          <h3 class="overview-title strengths-title">
            <span class="icon">💪</span> Global Strengths
          </h3>
          <div class="overview-cards">
            <div v-for="(strength, idx) in analysisData.global_strengths" :key="idx" class="overview-card strength-card">
              <div class="card-title">{{ strength.title }}</div>
              <ul class="card-list">
                <li v-for="(detail, detailIdx) in strength.details" :key="detailIdx">{{ detail }}</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Issues -->
        <div class="overview-column issues-column">
          <h3 class="overview-title issues-title">
            <span class="icon">⚠️</span> Global Issues
          </h3>
          <div class="overview-cards">
            <div v-for="(issue, idx) in analysisData.global_issues" :key="idx" class="overview-card issue-card">
              <div class="card-title">{{ issue.title }}</div>
              <ul class="card-list">
                <li v-for="(detail, detailIdx) in issue.details" :key="detailIdx">{{ detail }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Coaching Points -->
      <div class="section-header">
        <h2 class="section-title-analysis">Coaching Points</h2>
      </div>
      <div class="coaching-section">
        <div v-for="(point, idx) in analysisData.coaching_points" :key="idx" class="coaching-card">
          <div class="coaching-header">
            <h3 class="coaching-title">{{ point.title }}</h3>
          </div>
          <div class="coaching-problem">
            <div class="problem-label">Problem:</div>
            <p>{{ point.problem }}</p>
          </div>
          <div class="coaching-solutions">
            <div class="solutions-label">Solutions:</div>
            <ul class="solutions-list">
              <li v-for="(solution, sIdx) in point.solutions" :key="sIdx">{{ solution }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Actionable Improvements -->
      <div class="section-header">
        <h2 class="section-title-analysis">Action Items</h2>
      </div>
      <div class="actions-section">
        <div v-for="(action, idx) in analysisData.actionable_improvements" :key="idx" class="action-card" :class="'priority-' + action.priority.toLowerCase()">
          <div class="action-header">
            <span class="priority-badge">{{ action.priority }}</span>
            <!-- <span class="impact-text">Impact: {{ action.impact.substring(0, 500) }}</span> -->
          </div>
          <div class="action-content">{{ action.action }}</div>
        </div>
      </div>

      <!-- Final Verdict -->
      <div class="section-header">
        <h2 class="section-title-analysis">Final Verdict</h2>
      </div>
      <div class="verdict-section">
        <div class="verdict-summary">
          <p>{{ analysisData.final_verdict.summary }}</p>
        </div>
        <div class="verdict-takeaways">
          <h4 class="takeaways-title">Key Takeaways:</h4>
          <ul class="takeaways-list">
            <li v-for="(takeaway, idx) in analysisData.final_verdict.key_takeaways" :key="idx">{{ takeaway }}</li>
          </ul>
        </div>
      </div>

      <!-- Game Outcome Analysis -->
      <div class="outcome-section">
        <h3 class="outcome-title">Game Outcome Analysis</h3>
        <p class="outcome-summary">{{ analysisData.game_outcome_analysis.summary }}</p>
        <div class="outcome-factors">
          <h4 class="factors-title">Key Factors:</h4>
          <ul class="factors-list">
            <li v-for="(factor, idx) in analysisData.game_outcome_analysis.key_factors" :key="idx">{{ factor }}</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  analysisData: {
    type: Object,
    required: true
  },
  gameData: {
    type: Object,
    required: true
  }
})

defineEmits(['back'])

const getChampionIcon = (championName) => {
  const cleanName = championName.replace(/[^a-zA-Z]/g, '')
  return `https://ddragon.leagueoflegends.com/cdn/15.23.1/img/champion/${cleanName}.png`
}

const formatRole = (role) => {
  const roleNames = {
    'TOP': 'Top Lane',
    'JUNGLE': 'Jungle',
    'MIDDLE': 'Mid Lane',
    'BOTTOM': 'ADC',
    'SUPPORT': 'Support'
  }
  return roleNames[role] || role
}

const formatPhase = (phase) => {
  return phase.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

// Convert numeric score/rating (0-10) to letter grade (S, A, B, C, D)
const convertScoreToGrade = (score) => {
  if (typeof score === 'string') {
    // If already a letter grade, return as is
    return score
  }
  const numScore = parseFloat(score)
  if (isNaN(numScore)) return 'D'

  if (numScore >= 8) return 'S'
  if (numScore >= 6.5) return 'A'
  if (numScore >= 5) return 'B'
  if (numScore >= 3) return 'C'
  return 'D'
}

const calculateKDA = (kills, deaths, assists) => {
  if (deaths === 0) return 'Perfect'
  return ((kills + assists) / deaths).toFixed(1)
}

const formatGold = (gold) => {
  if (gold >= 1000) return `${(gold / 1000).toFixed(1)}k`
  return gold.toString()
}

const calculateCSPerMin = (cs, duration) => {
  return (cs / (duration / 60)).toFixed(1)
}
</script>

<style scoped>
.analysis-section {
  background: linear-gradient(to bottom, rgba(10, 20, 40, 1), rgba(5, 10, 20, 1));
  min-height: 100vh;
  padding: 2rem 1rem;
}

.analysis-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  background: rgba(200, 155, 60, 0.1);
  border: 2px solid var(--lol-gold);
  border-radius: 10px;
  color: var(--lol-gold);
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 2rem;
}

.back-btn:hover {
  background: rgba(200, 155, 60, 0.2);
  transform: translateX(-5px);
}

/* Game Header */
.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(10, 20, 40, 0.8);
  padding: 2rem;
  border-radius: 20px;
  border: 2px solid var(--lol-gold);
  margin-bottom: 3rem;
}

.header-left {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.header-champion-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid var(--lol-gold);
}

.header-champion-name {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--lol-gold-light);
  margin-bottom: 0.5rem;
}

.header-role {
  font-size: 1rem;
  color: var(--lol-gold);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.player-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.8rem;
}

.tag-badge {
  padding: 0.4rem 0.8rem;
  background: rgba(200, 155, 60, 0.15);
  border: 1px solid rgba(200, 155, 60, 0.4);
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.header-grade {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}

.grade-badge {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  font-weight: 900;
  border-radius: 15px;
  border: 4px solid;
  text-shadow: 0 0 20px currentColor;
  transition: all 0.3s ease;
}

.grade-badge:hover {
  transform: scale(1.05);
  box-shadow: 0 0 30px currentColor;
}

.grade-s {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 140, 0, 0.2));
  color: #ffd700;
  border-color: #ffd700;
}

.grade-a {
  background: linear-gradient(135deg, rgba(0, 212, 170, 0.2), rgba(0, 170, 130, 0.2));
  color: #00d4aa;
  border-color: #00d4aa;
}

.grade-b {
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.2), rgba(180, 135, 40, 0.2));
  color: var(--lol-gold);
  border-color: var(--lol-gold);
}

.grade-c {
  background: linear-gradient(135deg, rgba(255, 165, 0, 0.2), rgba(235, 145, 0, 0.2));
  color: #ffa500;
  border-color: #ffa500;
}

.grade-d {
  background: linear-gradient(135deg, rgba(255, 70, 85, 0.2), rgba(235, 50, 65, 0.2));
  color: #ff4655;
  border-color: #ff4655;
}

.grade-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
}

/* Game Stats Overview */
.game-stats-overview {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
}

.stats-main {
  flex: 1;
  min-width: 300px;
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(10, 20, 40, 0.6);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 15px;
  flex-wrap: wrap;
}

.stat-kda {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.8rem 1.2rem;
  background: rgba(200, 155, 60, 0.1);
  border-radius: 10px;
  border: 2px solid var(--lol-gold);
  min-width: 100px;
}

.kda-numbers {
  font-size: 1.3rem;
  font-weight: 900;
  color: var(--lol-gold-light);
  margin-bottom: 0.3rem;
}

.kda-ratio {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--lol-gold);
}

.stat-item-horizontal {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1rem;
  background: rgba(10, 20, 40, 0.8);
  border: 1px solid rgba(200, 155, 60, 0.2);
  border-radius: 10px;
  min-width: 120px;
}

.stat-icon {
  font-size: 1.2rem;
}

.stat-value {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--lol-gold-light);
}

.opponent-stats-overview {
  flex: 0 0 auto;
  min-width: 280px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 70, 85, 0.05);
  border: 2px solid rgba(255, 70, 85, 0.3);
  border-radius: 15px;
}

.opponent-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.vs-label {
  font-size: 0.9rem;
  font-weight: 900;
  color: #ff4655;
  padding: 0.3rem 0.6rem;
  background: rgba(255, 70, 85, 0.2);
  border-radius: 5px;
  border: 1px solid #ff4655;
}

.opponent-icon-small {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #ff4655;
}

.opponent-name-info {
  display: flex;
  flex-direction: column;
}

.opponent-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--lol-gold-light);
}

.opponent-champion {
  font-size: 0.75rem;
  color: var(--lol-gold);
}

.opponent-kda {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.opponent-kda-numbers {
  font-size: 1.1rem;
  font-weight: 900;
  color: var(--lol-gold-light);
}

.opponent-mini-stats {
  display: flex;
  gap: 0.8rem;
  font-size: 0.75rem;
  color: var(--lol-gold-light);
  opacity: 0.8;
}

/* Section Headers */
.section-header {
  margin: 3rem 0 1.5rem;
}

.section-title-analysis {
  font-size: 2rem;
  font-weight: 900;
  color: var(--lol-gold-light);
  text-align: center;
  letter-spacing: 0.05em;
}

/* Phase Analysis Grid */
.phase-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.phase-card {
  background: rgba(10, 20, 40, 0.8);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 15px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.phase-card:hover {
  border-color: var(--lol-gold);
  transform: translateY(-5px);
}

.phase-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.phase-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--lol-gold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.phase-rating-grade {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-weight: 900;
  font-size: 1.5rem;
  border: 3px solid;
  text-shadow: 0 0 10px currentColor;
  transition: all 0.3s ease;
}

.phase-rating-grade:hover {
  transform: scale(1.1);
}

.phase-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--lol-gold-light);
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(200, 155, 60, 0.2);
}

.list-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.strengths-header {
  color: #00d4aa;
}

.issues-header {
  color: #ff4655;
}

.phase-strengths, .phase-issues {
  margin-bottom: 1.5rem;
}

.strengths-list, .issues-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.strengths-list li, .issues-list li {
  padding: 0.5rem 0 0.5rem 1.5rem;
  position: relative;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--lol-gold-light);
}

.strengths-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #00d4aa;
  font-weight: 900;
}

.issues-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #ff4655;
  font-weight: 900;
}

/* Overview Grid */
.overview-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}

.overview-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.overview-title {
  font-size: 1.5rem;
  font-weight: 900;
  padding: 1rem;
  border-radius: 10px;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.strengths-title {
  background: rgba(0, 212, 170, 0.15);
  color: #00d4aa;
  border: 2px solid #00d4aa;
}

.issues-title {
  background: rgba(255, 70, 85, 0.15);
  color: #ff4655;
  border: 2px solid #ff4655;
}

.overview-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.overview-card {
  background: rgba(10, 20, 40, 0.8);
  border-radius: 15px;
  padding: 1.5rem;
  border: 2px solid;
}

.strength-card {
  border-color: rgba(0, 212, 170, 0.3);
}

.strength-card:hover {
  border-color: #00d4aa;
}

.issue-card {
  border-color: rgba(255, 70, 85, 0.3);
}

.issue-card:hover {
  border-color: #ff4655;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--lol-gold-light);
  margin-bottom: 1rem;
}

.card-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.card-list li {
  padding: 0.5rem 0 0.5rem 1.5rem;
  position: relative;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--lol-gold-light);
  opacity: 0.9;
}

.strength-card .card-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #00d4aa;
  font-weight: 900;
}

.issue-card .card-list li::before {
  content: "✗";
  position: absolute;
  left: 0;
  color: #ff4655;
  font-weight: 900;
}

/* Coaching Section */
.coaching-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.coaching-card {
  background: rgba(10, 20, 40, 0.8);
  border: 2px solid rgba(3, 151, 171, 0.5);
  border-radius: 15px;
  padding: 2rem;
}

.coaching-header {
  margin-bottom: 1.5rem;
}

.coaching-title {
  font-size: 1.3rem;
  font-weight: 900;
  color: var(--lol-blue);
}

.coaching-problem {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(255, 70, 85, 0.1);
  border-left: 4px solid #ff4655;
  border-radius: 5px;
}

.problem-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #ff4655;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
}

.coaching-problem p {
  color: var(--lol-gold-light);
  line-height: 1.6;
}

.coaching-solutions {
  padding: 1rem;
  background: rgba(0, 212, 170, 0.1);
  border-left: 4px solid #00d4aa;
  border-radius: 5px;
}

.solutions-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #00d4aa;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.8rem;
}

.solutions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.solutions-list li {
  padding: 0.5rem 0 0.5rem 1.5rem;
  position: relative;
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--lol-gold-light);
}

.solutions-list li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: #00d4aa;
  font-weight: 900;
}

/* Actions Section */
.actions-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1rem;
  margin-bottom: 3rem;
}

.action-card {
  background: rgba(10, 20, 40, 0.8);
  border-radius: 15px;
  padding: 1.5rem;
  border: 2px solid;
}

.priority-critical {
  border-color: #ff4655;
}

.priority-high {
  border-color: #ffa500;
}

.priority-medium {
  border-color: var(--lol-gold);
}

.action-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.priority-badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  width: fit-content;
}

.priority-critical .priority-badge {
  background: rgba(255, 70, 85, 0.2);
  color: #ff4655;
  border: 1px solid #ff4655;
}

.priority-high .priority-badge {
  background: rgba(255, 165, 0, 0.2);
  color: #ffa500;
  border: 1px solid #ffa500;
}

.priority-medium .priority-badge {
  background: rgba(200, 155, 60, 0.2);
  color: var(--lol-gold);
  border: 1px solid var(--lol-gold);
}

.impact-text {
  font-size: 0.85rem;
  color: var(--lol-gold-light);
  opacity: 0.8;
  font-style: italic;
}

.action-content {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--lol-gold-light);
}

/* Verdict Section */
.verdict-section {
  background: rgba(10, 20, 40, 0.8);
  border: 2px solid var(--lol-gold);
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.verdict-summary {
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--lol-gold-light);
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(200, 155, 60, 0.2);
}

.takeaways-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--lol-gold);
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.takeaways-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.takeaways-list li {
  padding: 0.8rem 0 0.8rem 1.5rem;
  position: relative;
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--lol-gold-light);
}

.takeaways-list li::before {
  content: "★";
  position: absolute;
  left: 0;
  color: var(--lol-gold);
  font-size: 1.2rem;
}

/* Outcome Section */
.outcome-section {
  background: rgba(3, 151, 171, 0.1);
  border: 2px solid var(--lol-blue);
  border-radius: 15px;
  padding: 2rem;
}

.outcome-title {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--lol-blue);
  margin-bottom: 1rem;
}

.outcome-summary {
  font-size: 1rem;
  line-height: 1.8;
  color: var(--lol-gold-light);
  margin-bottom: 1.5rem;
}

.factors-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--lol-gold);
  margin-bottom: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.factors-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.factors-list li {
  padding: 0.5rem 0 0.5rem 1.5rem;
  position: relative;
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--lol-gold-light);
}

.factors-list li::before {
  content: "▸";
  position: absolute;
  left: 0;
  color: var(--lol-blue);
  font-weight: 900;
}

@media (max-width: 1024px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }

  .phase-grid {
    grid-template-columns: 1fr;
  }

  .actions-section {
    grid-template-columns: 1fr;
  }

  .game-header {
    flex-direction: column;
    gap: 2rem;
    text-align: center;
  }

  .game-stats-overview {
    flex-direction: column;
  }

  .stats-main {
    justify-content: center;
  }

  .opponent-stats-overview {
    min-width: 100%;
  }
}

@media (max-width: 768px) {
  .analysis-section {
    padding: 1.5rem 0.5rem;
  }

  .analysis-wrapper {
    padding: 0 0.5rem;
  }

  .back-btn {
    font-size: 0.85rem;
    padding: 0.7rem 1.2rem;
    margin-bottom: 1.5rem;
  }

  .game-header {
    padding: 1.5rem;
  }

  .header-champion-icon {
    width: 60px;
    height: 60px;
  }

  .header-champion-name {
    font-size: 1.8rem;
  }

  .header-role {
    font-size: 0.85rem;
  }

  .grade-badge {
    width: 80px;
    height: 80px;
    font-size: 3rem;
  }

  .grade-label {
    font-size: 0.75rem;
  }

  .stats-main {
    gap: 0.8rem;
    padding: 1.2rem;
  }

  .stat-item-horizontal {
    flex: 1 1 100%;
    min-width: 100%;
  }

  .stat-value {
    font-size: 0.8rem;
  }

  .opponent-stats-overview {
    padding: 1.2rem;
  }

  .opponent-mini-stats {
    flex-direction: column;
    gap: 0.3rem;
  }

  .section-header {
    margin: 2rem 0 1rem;
  }

  .section-title-analysis {
    font-size: 1.5rem;
  }

  .phase-grid {
    gap: 1rem;
  }

  .phase-card {
    padding: 1.2rem;
  }

  .phase-name {
    font-size: 1rem;
  }

  .phase-title {
    font-size: 0.9rem;
  }

  .strengths-list li,
  .issues-list li {
    font-size: 0.8rem;
  }

  .overview-title {
    font-size: 1.2rem;
    padding: 0.8rem;
  }

  .overview-card {
    padding: 1.2rem;
  }

  .card-title {
    font-size: 1rem;
  }

  .card-list li {
    font-size: 0.8rem;
  }

  .coaching-card {
    padding: 1.5rem;
  }

  .coaching-title {
    font-size: 1.1rem;
  }

  .coaching-problem,
  .coaching-solutions {
    padding: 0.8rem;
  }

  .action-card {
    padding: 1.2rem;
  }

  .action-content {
    font-size: 0.85rem;
  }

  .verdict-section {
    padding: 1.5rem;
  }

  .verdict-summary {
    font-size: 1rem;
  }

  .takeaways-title {
    font-size: 1.1rem;
  }

  .takeaways-list li {
    font-size: 0.85rem;
  }

  .outcome-section {
    padding: 1.5rem;
  }

  .outcome-title {
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .analysis-section {
    padding: 1rem 0.25rem;
  }

  .analysis-wrapper {
    padding: 0;
  }

  .back-btn {
    font-size: 0.8rem;
    padding: 0.6rem 1rem;
    margin-bottom: 1rem;
  }

  .game-header {
    padding: 1rem;
  }

  .header-left {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .header-champion-icon {
    width: 50px;
    height: 50px;
  }

  .header-champion-name {
    font-size: 1.5rem;
  }

  .header-role {
    font-size: 0.75rem;
  }

  .player-tags {
    justify-content: center;
  }

  .tag-badge {
    padding: 0.3rem 0.6rem;
    font-size: 0.7rem;
  }

  .grade-badge {
    width: 70px;
    height: 70px;
    font-size: 2.5rem;
  }

  .grade-label {
    font-size: 0.7rem;
  }

  .game-stats-overview {
    gap: 1rem;
  }

  .stats-main {
    gap: 0.6rem;
    padding: 1rem;
  }

  .stat-kda {
    padding: 0.6rem 1rem;
  }

  .kda-numbers {
    font-size: 1.1rem;
  }

  .kda-ratio {
    font-size: 0.75rem;
  }

  .stat-item-horizontal {
    padding: 0.6rem 0.8rem;
    min-width: 100%;
  }

  .stat-icon {
    font-size: 1rem;
  }

  .stat-value {
    font-size: 0.75rem;
  }

  .opponent-stats-overview {
    padding: 1rem;
  }

  .section-header {
    margin: 1.5rem 0 1rem;
  }

  .section-title-analysis {
    font-size: 1.3rem;
  }

  .phase-grid {
    gap: 0.8rem;
  }

  .phase-card {
    padding: 1rem;
  }

  .phase-name {
    font-size: 0.9rem;
  }

  .phase-rating-grade {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }

  .phase-title {
    font-size: 0.85rem;
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
  }

  .list-header {
    font-size: 0.8rem;
  }

  .strengths-list li,
  .issues-list li {
    font-size: 0.75rem;
    padding: 0.4rem 0 0.4rem 1.2rem;
  }

  .overview-title {
    font-size: 1.1rem;
    padding: 0.7rem;
  }

  .overview-card {
    padding: 1rem;
  }

  .card-title {
    font-size: 0.95rem;
  }

  .card-list li {
    font-size: 0.75rem;
  }

  .coaching-card {
    padding: 1.2rem;
  }

  .coaching-title {
    font-size: 1rem;
  }

  .coaching-problem,
  .coaching-solutions {
    padding: 0.7rem;
  }

  .problem-label,
  .solutions-label {
    font-size: 0.75rem;
  }

  .coaching-problem p {
    font-size: 0.85rem;
  }

  .solutions-list li {
    font-size: 0.8rem;
  }

  .action-card {
    padding: 1rem;
  }

  .priority-badge {
    padding: 0.3rem 0.8rem;
    font-size: 0.7rem;
  }

  .action-content {
    font-size: 0.8rem;
  }

  .verdict-section {
    padding: 1.2rem;
  }

  .verdict-summary {
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
  }

  .takeaways-title {
    font-size: 1rem;
  }

  .takeaways-list li {
    font-size: 0.8rem;
    padding: 0.6rem 0 0.6rem 1.3rem;
  }

  .outcome-section {
    padding: 1.2rem;
  }

  .outcome-title {
    font-size: 1.2rem;
  }

  .outcome-summary {
    font-size: 0.9rem;
  }

  .factors-title {
    font-size: 0.9rem;
  }

  .factors-list li {
    font-size: 0.8rem;
  }
}
</style>
