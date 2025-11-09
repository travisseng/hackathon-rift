<template>
  <section class="section most-played-role-section">
    <div class="stats-container">
      <h2 class="section-title">Champions & Roles</h2>

      <!-- Most Played Champions -->
      <div class="subsection">
        <h3 class="subsection-title">🏆 Most Played Champions</h3>
        <div class="champions-grid">
          <div
            v-for="(count, champion) in mostPlayedData.champions"
            :key="champion"
            class="champion-card"
            :class="getChampionRank(champion, mostPlayedData.champions)"
          >
            <div class="champion-image-container">
              <img
                :src="getChampionImageUrl(champion)"
                :alt="champion"
                class="champion-image"
                @error="handleImageError"
              />
            </div>
            <div class="champion-name">{{ champion }}</div>
            <div class="champion-count">{{ count }} games</div>
          </div>
        </div>
      </div>

      <!-- Most Played Roles -->
      <div class="subsection">
        <h3 class="subsection-title">📍 Most Played Roles</h3>
        <div class="roles-grid">
          <div
            v-for="(count, role) in mostPlayedData.roles"
            :key="role"
            class="role-card"
          >
            <div class="role-icon-container">
              <img :src="getRoleIconUrl(role)" :alt="role" class="role-icon-image" />
            </div>
            <div class="role-name">{{ formatRole(role) }}</div>
            <div class="role-count">{{ count }} games</div>
            <div class="role-bar">
              <div
                class="role-bar-fill"
                :style="{ width: getRolePercentage(count) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Role Performance -->
      <div class="subsection">
        <h3 class="subsection-title">📊 Role Performance</h3>
        <div class="performance-grid">
          <div
            v-for="(stats, role) in rolePerformanceData.winrate_by_role"
            :key="role"
            class="performance-card"
            :class="{
              'best-role': role === rolePerformanceData.best_role,
              'worst-role': role === rolePerformanceData.worst_role
            }"
          >
            <div class="performance-header">
              <div class="performance-role-icon-container">
                <img :src="getRoleIconUrl(role)" :alt="role" class="performance-role-icon-image" />
              </div>
              <span class="performance-role-name">{{ formatRole(role) }}</span>
            </div>
            <div class="performance-winrate" :class="getWinrateClass(stats.winrate)">
              {{ (stats.winrate * 100).toFixed(0) }}%
            </div>
            <div class="performance-record">
              {{ stats.wins }}W - {{ stats.losses }}L
            </div>
            <div class="performance-badge" v-if="role === rolePerformanceData.best_role">
              ⭐ Best Role
            </div>
            <div class="performance-badge worst" v-if="role === rolePerformanceData.worst_role">
              ⚠️ Needs Work
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
  mostPlayedData: {
    type: Object,
    required: true
  },
  rolePerformanceData: {
    type: Object,
    required: true
  },
  insights: {
    type: Array,
    default: () => []
  }
})

const getChampionRank = (champion, champions) => {
  const sorted = Object.entries(champions).sort((a, b) => b[1] - a[1])
  const index = sorted.findIndex(([name]) => name === champion)
  if (index === 0) return 'rank-1'
  if (index === 1) return 'rank-2'
  if (index === 2) return 'rank-3'
  return ''
}

const getChampionImageUrl = (championName) => {
  const cleanName = championName.replace(/[^a-zA-Z]/g, '')
  return `https://ddragon.leagueoflegends.com/cdn/15.23.1/img/champion/${cleanName}.png`
}

const handleImageError = (event) => {
  // Fallback to a default image if champion image fails to load
  event.target.src = 'https://ddragon.leagueoflegends.com/cdn/15.22.1/img/profileicon/29.png'
}

const getRoleIconUrl = (role) => {
  const iconUrls = {
    'TOP': 'https://wiki.leagueoflegends.com/en-us/images/Top_icon.png',
    'JUNGLE': 'https://wiki.leagueoflegends.com/en-us/images/Jungle_icon.png',
    'MIDDLE': 'https://wiki.leagueoflegends.com/en-us/images/Middle_icon.png',
    'BOTTOM': 'https://wiki.leagueoflegends.com/en-us/images/Bottom_icon.png',
    'SUPPORT': 'https://wiki.leagueoflegends.com/en-us/images/Support_icon.png',
    'UTILITY': 'https://wiki.leagueoflegends.com/en-us/images/Support_icon.png'
  }
  return iconUrls[role] || 'https://wiki.leagueoflegends.com/en-us/images/Middle_icon.png'
}

const formatRole = (role) => {
  if (role === 'MIDDLE') return 'Mid'
  if (role === 'BOTTOM') return 'ADC'
  if (role === 'SUPPORT' || role === 'UTILITY') return 'Support'
  return role.charAt(0) + role.slice(1).toLowerCase()
}

const getRolePercentage = (count) => {
  const total = Object.values(props.mostPlayedData.roles).reduce((sum, val) => sum + val, 0)
  return (count / total) * 100
}

const getWinrateClass = (winrate) => {
  if (winrate >= 0.55) return 'excellent'
  if (winrate >= 0.50) return 'good'
  if (winrate >= 0.45) return 'average'
  return 'poor'
}
</script>

<style scoped>
.most-played-role-section {
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

/* Champions Grid */
.champions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.champion-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
}

.champion-card:hover {
  transform: translateY(-5px);
  border-color: var(--lol-gold);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.3);
}

.champion-card.rank-1 {
  border-color: rgba(255, 215, 0, 0.7);
  background: rgba(255, 215, 0, 0.05);
}

.champion-card.rank-2 {
  border-color: rgba(192, 192, 192, 0.7);
  background: rgba(192, 192, 192, 0.05);
}

.champion-card.rank-3 {
  border-color: rgba(205, 127, 50, 0.7);
  background: rgba(205, 127, 50, 0.05);
}

.champion-image-container {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--lol-gold);
  box-shadow: 0 4px 15px rgba(200, 155, 60, 0.4);
  transition: all 0.3s ease;
}

.champion-card:hover .champion-image-container {
  transform: scale(1.1);
  box-shadow: 0 6px 25px rgba(200, 155, 60, 0.6);
}

.champion-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.champion-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--lol-gold);
  margin-bottom: 0.5rem;
  text-transform: capitalize;
}

.champion-count {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
}

/* Roles Grid */
.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.role-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(3, 151, 171, 0.3);
  border-radius: 15px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.role-card:hover {
  transform: translateY(-5px);
  border-color: #0397ab;
  box-shadow: 0 10px 30px rgba(3, 151, 171, 0.3);
}

.role-icon-container {
  width: 60px;
  height: 60px;
  margin: 0 auto 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-icon-image {
  width: 50px;
  height: 50px;
  object-fit: contain;
  filter: drop-shadow(0 2px 8px rgba(3, 151, 171, 0.4));
  transition: all 0.3s ease;
}

.role-card:hover .role-icon-image {
  transform: scale(1.1);
  filter: drop-shadow(0 4px 12px rgba(3, 151, 171, 0.6));
}

.role-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--lol-gold);
  margin-bottom: 0.5rem;
}

.role-count {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  margin-bottom: 0.8rem;
}

.role-bar {
  width: 100%;
  height: 8px;
  background: rgba(3, 151, 171, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.role-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #0397ab, #00dfa2);
  transition: width 0.5s ease;
}

/* Performance Grid */
.performance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.performance-card {
  background: rgba(10, 20, 40, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 15px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
}

.performance-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.3);
}

.performance-card.best-role {
  border-color: rgba(0, 223, 162, 0.7);
  background: rgba(0, 223, 162, 0.05);
}

.performance-card.worst-role {
  border-color: rgba(255, 70, 85, 0.7);
  background: rgba(255, 70, 85, 0.05);
}

.performance-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.performance-role-icon-container {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.performance-role-icon-image {
  width: 35px;
  height: 35px;
  object-fit: contain;
  filter: drop-shadow(0 2px 6px rgba(200, 155, 60, 0.4));
}

.performance-role-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--lol-gold);
}

.performance-winrate {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
}

.performance-winrate.excellent {
  color: #00dfa2;
}

.performance-winrate.good {
  color: #0397ab;
}

.performance-winrate.average {
  color: var(--lol-gold);
}

.performance-winrate.poor {
  color: #ff4655;
}

.performance-record {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  margin-bottom: 0.8rem;
}

.performance-badge {
  margin-top: 0.8rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 223, 162, 0.2);
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  color: #00dfa2;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.performance-badge.worst {
  background: rgba(255, 70, 85, 0.2);
  color: #ff4655;
}

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
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.2), rgba(200, 155, 60, 0.3));
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

  .champions-grid,
  .roles-grid,
  .performance-grid {
    grid-template-columns: 1fr;
  }
}
</style>
