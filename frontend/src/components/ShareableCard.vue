<template>
  <section class="section shareable-section">
    <div class="content-wrapper">
      <h2 class="section-title">Share Your 2025 Wrapped</h2>

      <div class="story-card" ref="cardRef">
        <!-- HEADER -->
        <div class="card-header">
          <div class="header-content">
            <div class="header-top">
              <!-- <span class="header-game">LEAGUE OF LEGENDS</span>
              <span class="header-divider">•</span>
              <span class="header-year">2025 WRAPPED</span> -->
            </div>
            <div class="header-player" v-if="summonerName">
              <span class="player-name">{{ summonerName }}</span>
              <span class="player-tag">#{{ summonerTag }}</span>

              <span class="role-text-compact"><img style="position: relative; top: 3px;" :src="getMostPlayedRoleIcon()" alt="Role Icon" class="role-icon-compact" /> MAIN</span>
            </div>
            <div class="player-title" v-if="data.aiInsights.player_title">
              {{ data.aiInsights.player_title }}
            </div>
          </div>
        </div>

        <!-- TOP HALF: Champions Splash Arts -->
        <div class="champions-half">
          <div class="champions-grid">
            <div
              v-for="(champion, index) in getTop3Champions()"
              :key="index"
              class="champion-splash"
              :class="`champion-${index + 1}`"
              :style="{ backgroundImage: `url(${getChampionSplashArtByName(champion.name)})` }"
            >
              <div class="champion-overlay">
                <div class="champion-rank">#{{ index + 1 }}</div>
                <div class="champion-info">
                  <div class="champion-name">{{ formatChampionName(champion.name) }}</div>
                  <div class="champion-games-count">{{ champion.games }} games</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- BOTTOM HALF: Stats -->
        <div class="stats-half">
          <!-- Rank Display -->
          <div class="rank-display" v-if="getRankData()">
            <img :src="getRankImageUrl(getRankData().tier)" alt="Rank" class="rank-icon" />
            <div class="rank-info">
              <div class="rank-tier">{{ formatRank() }}</div>
              <div class="rank-lp">{{ getRankData().lp }} LP</div>
            </div>
          </div>


          <!-- Key Stats Grid -->
          <div class="stats-grid">
            <div class="stat-box">
              <div class="stat-number">{{ data.overview.games_played }}</div>
              <div class="stat-label">Games</div>
            </div>
            <div class="stat-box">
              <div class="stat-number">{{ (data.overview.winrate * 100).toFixed(0) }}%</div>
              <div class="stat-label">Win Rate</div>
            </div>
            <div class="stat-box">
              <div class="stat-number kda-breakdown">{{ data.combat_stats.average.kills.toFixed(1) }} / {{ data.combat_stats.average.deaths.toFixed(1) }} / {{ data.combat_stats.average.assists.toFixed(1) }}</div>
              <div class="stat-label">K / D / A</div>
              <div class="kda-ratio">{{ data.combat_stats.average.kda.toFixed(2) }} KDA</div>
            </div>
          </div>

          <!-- Performance Stats -->
          <div class="performance-stats">
            <div class="stat-box secondary">
              <div class="stat-number">{{ getTotalPlaytimeHours() }}</div>
              <div class="stat-label">Hours Played</div>
            </div>
            <div class="stat-box secondary">
              <div class="stat-number">{{ getMultikills() }}</div>
              <div class="stat-label">Penta/Quadra/Triple</div>
            </div>
            <div class="stat-box secondary">
              <div class="stat-number">{{ data.overview.champion_pool }}</div>
              <div class="stat-label">Champion Pool</div>
            </div>
            
            
          </div>

          <!-- Additional Stats -->
          <div class="secondary-stats">
            <div class="stat-box performance">
              <div class="stat-number">{{ getVPM() }}</div>
              <div class="stat-label">VPM</div>
              <div class="stat-sublabel">Vision Per Minute</div>
            </div>
            <div class="stat-box performance">
              <div class="stat-number">{{ getDPM() }}</div>
              <div class="stat-label">DPM</div>
              <div class="stat-sublabel">Damage Per Minute</div>
            </div>
            <div class="stat-box performance">
              <div class="stat-number">{{ getCSPerMin() }}</div>
              <div class="stat-label">CS/Min</div>
            </div>
          </div>


          <!-- Monthly Activity Chart -->
          <div class="activity-chart">
            <div class="chart-title">Activity Throughout the Year</div>
            <div class="chart-bars">
              <div
                v-for="(games, month) in getMonthlyData()"
                :key="month"
                class="bar-container"
              >
                <div class="bar-wrapper">
                  <div
                    class="bar"
                    :style="{ height: getBarHeight(games) + '%' }"
                  ></div>
                </div>
                <div class="bar-label">{{ formatMonth(month) }}</div>
              </div>
            </div>
          </div>

          
          <!-- Footer -->
          <div class="card-footer-story">
            <div class="footer-watermark">League of Legends • 2025 Wrapped</div>
          </div>
        </div>
      </div>

      <!-- Share Instructions -->
      <div class="share-instructions">
        <p class="instruction-text">Perfect for Instagram Stories & TikTok!</p>
        <div class="share-buttons">
          <button class="share-btn" @click="downloadCard">
            <span class="btn-icon">📥</span>
            Download
          </button>
          <button class="share-btn secondary" @click="resetApp">
            <span class="btn-icon">🔄</span>
            New Search
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import html2canvas from 'html2canvas'

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  accountData: {
    type: Object,
    default: null
  },
  summonerName: {
    type: String,
    default: ''
  },
  summonerTag: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['reset'])
const cardRef = ref(null)

// Get rank data from account data
const getRankData = () => {
  if (!props.accountData?.league_overview?.data?.queue_1) {
    return null
  }
  // get keys in league_overview.data
  const keys = Object.keys(props.accountData.league_overview.data)
  // iterate to find queue RANKED_SOLO_5x5 or equivalent
  for (const key of keys) {
    const queueData = props.accountData.league_overview.data[key]
    if (queueData.queueType === 'RANKED_SOLO_5x5') {
      return {
        tier: queueData.tier,
        rank: queueData.rank,
        lp: queueData.leaguePoints,
        wins: queueData.wins,
        losses: queueData.losses
      }
    }
  }
  // Fallback to queue_1 if specific queue not found
  if (keys.length > 0) {
    const fallbackData = props.accountData.league_overview.data[keys[0]]
    return {
      tier: fallbackData.tier,
      rank: fallbackData.rank,
      lp: fallbackData.leaguePoints,
      wins: fallbackData.wins,
      losses: fallbackData.losses
    }
  }
}

// Get rank image URL (placeholder for now)
const getRankImageUrl = (tier) => {
  if (!tier) return '/ranks/unranked.png'

  const tierLower = tier.toLowerCase()
  return `/ranks/Rank=${tierLower}.png`
}

// Format rank display
const formatRank = () => {
  const rank = getRankData()
  if (!rank) return 'Unranked'

  return `${rank.tier} ${rank.rank}`
}

const formatChampionName = (name) => {
  return name.replace(/([A-Z])/g, ' $1').trim().toUpperCase()
}

const getTopChampion = () => {
  const champions = props.data.most_played.champions
  const entries = Object.entries(champions)
  if (entries.length === 0) return 'Unknown'
  return entries[0][0]
}

const getTopChampionGames = () => {
  const champions = props.data.most_played.champions
  const entries = Object.entries(champions)
  if (entries.length === 0) return 0
  return entries[0][1]
}

const getTop3Champions = () => {
  const champions = props.data.most_played.champions
  const entries = Object.entries(champions)

  // Sort by games played (descending) and take top 3
  entries.sort((a, b) => b[1] - a[1])
  const top3 = entries.slice(0, 3)

  return top3.map(([name, games]) => ({
    name,
    games
  }))
}

const getChampionSplashArtByName = (championName) => {
  // Clean champion name for URL (remove spaces and special chars)
  const cleanName = championName.replace(/[^a-zA-Z]/g, '')
  return `https://ddragon.leagueoflegends.com/cdn/img/champion/loading/${cleanName}_0.jpg`
}

const getMostPlayedRole = () => {
  const roles = props.data.most_played.roles
  const entries = Object.entries(roles)
  if (entries.length === 0) return 'Unknown'

  const [role] = entries.reduce((max, entry) => entry[1] > max[1] ? entry : max)

  const roleNames = {
    'TOP': 'Top',
    'JUNGLE': 'Jungle',
    'MIDDLE': 'Mid',
    'BOTTOM': 'ADC',
    'UTILITY': 'Support',
    'SUPPORT': 'Support'
  }

  return roleNames[role] || role
}

const getMostPlayedRoleIcon = () => {
  const roles = props.data.most_played.roles
  const entries = Object.entries(roles)
  if (entries.length === 0) return 'https://wiki.leagueoflegends.com/en-us/images/Middle_icon.png'

  const [role] = entries.reduce((max, entry) => entry[1] > max[1] ? entry : max)

  const iconUrls = {
    'TOP': 'https://wiki.leagueoflegends.com/en-us/images/Top_icon.png',
    'JUNGLE': 'https://wiki.leagueoflegends.com/en-us/images/Jungle_icon.png',
    'MIDDLE': 'https://wiki.leagueoflegends.com/en-us/images/Middle_icon.png',
    'BOTTOM': 'https://wiki.leagueoflegends.com/en-us/images/Bottom_icon.png',
    'UTILITY': 'https://wiki.leagueoflegends.com/en-us/images/Support_icon.png',
    'SUPPORT': 'https://wiki.leagueoflegends.com/en-us/images/Support_icon.png'
  }
  return iconUrls[role] || 'https://wiki.leagueoflegends.com/en-us/images/Middle_icon.png'
}

const formatNumber = (num) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const getMultikills = () => {
  // Get from combat_stats
  const combatStats = props.data.combat_stats.total || {}
  const pentas = combatStats.penta_kills || 0
  const quadras = combatStats.quadra_kills || 0
  const triples = combatStats.triple_kills || 0

  return `${pentas}/${quadras}/${triples}`
}

const getCSPerMin = () => {
  // Get from economy_stats
  const economyStats = props.data.economy_stats.average || {}
  const csMin = economyStats.cs_per_min || 0
  return csMin ? csMin.toFixed(1) : '0.0'
}

const getTotalPlaytimeHours = () => {
  // Get total game time in seconds and convert to hours
  const totalSeconds = props.data.time_stats.total.game_time || 0
  const hours = totalSeconds / 3600
  return Math.round(hours)
}

const getDPM = () => {
  // Calculate damage per minute: average damage / (average game duration in seconds / 60)
  const avgDamage = props.data.damage_stats.average.damage_dealt || 0
  const avgDuration = props.data.time_stats.average.game_duration || 1 // Avoid division by zero
  const dpm = avgDamage / (avgDuration / 60)
  return Math.round(dpm)
}

const getVPM = () => {
  // Calculate vision per minute: average vision score / (average game duration in seconds / 60)
  const avgVision = props.data.vision_stats.average.vision_score || 0
  const avgDuration = props.data.time_stats.average.game_duration || 1 // Avoid division by zero
  const vpm = avgVision / (avgDuration / 60)
  return vpm.toFixed(1)
}

const getMonthlyData = () => {
  const monthlyData = props.data.time_stats.by_month || {}

  // Define all 12 months of 2025
  const months2025 = [
    'January 2025', 'February 2025', 'March 2025', 'April 2025',
    'May 2025', 'June 2025', 'July 2025', 'August 2025',
    'September 2025', 'October 2025', 'November 2025', 'December 2025'
  ]

  // Create an object with all months, defaulting to 0 games
  const result = {}
  months2025.forEach(month => {
    // Check if this month exists in the data
    result[month] = monthlyData[month] || 0
  })

  return result
}

const getBarHeight = (games) => {
  // Get the max from 2025 months only
  const data2025 = getMonthlyData()
  const maxGames = Math.max(...Object.values(data2025))
  return maxGames > 0 ? (games / maxGames) * 100 : 0
}

const formatMonth = (monthYear) => {
  // Convert "January 2025" to "Jan"
  const parts = monthYear.split(' ')
  if (parts.length > 0) {
    return parts[0].substring(0, 3)
  }
  return monthYear
}

const downloadCard = async () => {
  if (!cardRef.value) return

  try {
    const canvas = await html2canvas(cardRef.value, {
      backgroundColor: null,
      scale: 2,
      logging: false,
      useCORS: true
    })

    const link = document.createElement('a')
    link.download = 'lol-wrapped-2025-story.png'
    link.href = canvas.toDataURL()
    link.click()
  } catch (error) {
    console.error('Failed to download card:', error)
  }
}

const resetApp = () => {
  emit('reset')
}
</script>

<style scoped>
.shareable-section {
  background: radial-gradient(circle at 50% 50%, rgba(200, 155, 60, 0.08) 0%, transparent 60%);
  min-height: 100vh;
  padding: 4rem 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-x: hidden;
}

.content-wrapper {
  max-width: 550px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-title {
  font-size: clamp(2rem, 4vw, 2.5rem);
  font-weight: 900;
  text-align: center;
  margin-bottom: 2.5rem;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-gold-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Story Card - 9:16 Ratio - Fixed dimensions */
.story-card {
  position: relative;
  width: 405px;
  height: 720px;
  margin: 0 auto;
  border-radius: 25px;
  overflow: hidden;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.8),
              0 0 60px rgba(200, 155, 60, 0.4);
  display: flex;
  flex-direction: column;
  transform-origin: center center;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

/* HEADER */
.card-header {
  position: relative;
  background: linear-gradient(135deg, rgba(200, 155, 60, 1), rgba(180, 135, 50, 0.95));
  padding: 0.6rem 1rem;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  border-bottom: 2px solid rgba(255, 215, 100, 0.5);
}

.card-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    90deg,
    transparent,
    transparent 2px,
    rgba(255, 255, 255, 0.03) 2px,
    rgba(255, 255, 255, 0.03) 4px
  );
  pointer-events: none;
}

.header-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  font-size: 0.5rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: rgba(10, 20, 40, 0.7);
}

.header-game {
  opacity: 0.8;
}

.header-divider {
  font-size: 0.4rem;
  opacity: 0.6;
}

.header-year {
  opacity: 0.8;
}

.header-player {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.3rem 0.8rem;
  background: rgba(10, 20, 40, 0.15);
  border-radius: 8px;
  margin: 0 auto;
  max-width: fit-content;
  backdrop-filter: blur(5px);
}

.player-name {
  font-size: 1.1rem;
  font-weight: 900;
  color: var(--lol-dark);
  letter-spacing: 0.05em;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.2);
}

.player-tag {
  font-size: 0.85rem;
  font-weight: 700;
  color: rgba(10, 20, 40, 0.8);
  letter-spacing: 0.05em;
}

.player-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: rgba(10, 20, 40, 0.9);
  letter-spacing: 0.08em;
  text-align: center;
  padding: 0.25rem 0.6rem;
  margin-top: 0.3rem;
  background: rgba(255, 215, 100, 0.3);
  border-radius: 6px;
  text-transform: uppercase;
}

/* TOP HALF: Champions */
.champions-half {
  position: relative;
  flex: 1;
  min-height: 33%;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.champions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  width: 100%;
  height: 100%;
  gap: 2px;
}

.champion-splash {
  position: relative;
  background-size: cover;
  background-position: center;
  overflow: hidden;
}

.champion-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(10, 20, 40, 0.95), transparent);
  padding: 0.8rem 0.7rem;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.champion-rank {
  font-size: 1.8rem;
  font-weight: 900;
  color: var(--lol-gold);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
}

.champion-info {
  text-align: right;
  flex: 1;
}

.champion-name {
  font-size: 0.95rem;
  font-weight: 900;
  color: var(--lol-gold-light);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
  letter-spacing: 0.05em;
  line-height: 1.1;
  margin-bottom: 0.15rem;
}

.champion-games-count {
  font-size: 0.65rem;
  color: var(--lol-gold);
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
}

/* BOTTOM HALF: Stats */
.stats-half {
  flex: 1.15;
  background: linear-gradient(to bottom, var(--lol-dark), rgba(10, 20, 40, 1));
  padding: 0.5rem 1rem 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Rank Display */
.rank-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.7rem;
  padding: 0.6rem 0.6rem;
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.3), rgba(200, 155, 60, 0.1));
  border: 2px solid var(--lol-gold);
  border-radius: 10px;
}

.rank-icon {
  width: 40px;
  height: 40px;
  object-fit: contain;
  filter: drop-shadow(0 2px 8px rgba(200, 155, 60, 0.5));
}

.rank-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.1rem;
}

.rank-tier {
  font-size: 0.95rem;
  font-weight: 900;
  color: var(--lol-gold);
  letter-spacing: 0.05em;
  text-transform: capitalize;
  line-height: 1;
}

.rank-lp {
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--lol-gold-light);
  opacity: 0.9;
}

/* Compact Role Display */
.role-display-compact {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.6rem 1rem;
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.2), rgba(3, 151, 171, 0.1));
  border: 2px solid var(--lol-gold);
  border-radius: 10px;
}

.role-icon-compact {
  width: 18px;
  height: 18px;
  object-fit: contain;
  filter: brightness(1.2);
}

.role-text-compact {
  font-size: 0.8rem;
  font-weight: 900;
  color: var(--lol-gold);
  letter-spacing: 0.1em;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.4rem;
}

.stat-box {
  background: rgba(10, 20, 40, 0.7);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(200, 155, 60, 0.4);
  border-radius: 12px;
  padding: 0.23rem 0.4rem;
  text-align: center;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--lol-gold);
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-number.kda-breakdown {
  font-size: 0.9rem;
  line-height: 1.1;
}

.stat-label {
  font-size: 0.55rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  opacity: 0.9;
  line-height: 1.2;
}

.stat-sublabel {
  font-size: 0.4rem;
  color: var(--lol-gold-light);
  opacity: 0.6;
  margin-top: 0.15rem;
  line-height: 1;
  text-transform: capitalize;
}

.kda-ratio {
  font-size: 0.5rem;
  color: var(--lol-gold);
  font-weight: 700;
  margin-top: 0.2rem;
  opacity: 0.8;
}

/* Performance Stats */
.performance-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.4rem;
}

.stat-box.performance {
  border: 2px solid rgba(200, 155, 60, 0.5);
  background: rgba(10, 20, 40, 0.8);
}

/* Activity Chart */
.activity-chart {
  background: rgba(10, 20, 40, 0.7);
  backdrop-filter: blur(20px);
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: 2px solid rgba(200, 155, 60, 0.3);
}

.chart-title {
  font-size: 0.6rem;
  color: var(--lol-gold);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.4rem;
  text-align: center;
  font-weight: 700;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 0.15rem;
  height: 38px;
}

.bar-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
}

.bar-wrapper {
  width: 100%;
  height: 30px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.bar {
  width: 100%;
  background: linear-gradient(to top, var(--lol-gold), var(--lol-gold-light));
  border-radius: 1px 1px 0 0;
  min-height: 2px;
  transition: height 0.3s ease;
  box-shadow: 0 0 8px rgba(200, 155, 60, 0.3);
}

.bar-label {
  font-size: 0.42rem;
  color: var(--lol-gold-light);
  text-transform: uppercase;
  opacity: 0.8;
  font-weight: 600;
  line-height: 1;
}

/* Secondary Stats */
.secondary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.4rem;
}

.stat-box.secondary {
  border: 1px solid rgba(200, 155, 60, 0.3);
}

/* Footer */
.card-footer-story {
  text-align: center;
  padding-top: 0.3rem;
}

.footer-watermark {
  font-size: 0.55rem;
  color: rgba(240, 230, 210, 0.5);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

/* Share Instructions */
.share-instructions {
  margin-top: 3rem;
  text-align: center;
}

.instruction-text {
  font-size: 1rem;
  color: var(--lol-gold-light);
  margin-bottom: 1.5rem;
}

.share-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.share-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-gold-light));
  color: var(--lol-dark);
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.share-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.4);
}

.share-btn.secondary {
  background: transparent;
  border: 2px solid var(--lol-gold);
  color: var(--lol-gold);
}

.btn-icon {
  font-size: 1.2rem;
}

/* Scale card down on smaller screens while maintaining exact proportions */
@media (max-width: 768px) {
  .shareable-section {
    padding: 2rem 1rem;
  }

  .content-wrapper {
    max-width: 100%;
    padding: 0;
  }

  .section-title {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
  }

  .story-card {
    transform: scale(0.9);
  }

  .share-instructions {
    margin-top: 1rem;
  }

  .share-buttons {
    flex-direction: column;
    gap: 0.8rem;
  }
}

@media (max-width: 480px) {
  .shareable-section {
    padding: 1.5rem 0.5rem;
  }

  .section-title {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }

  .story-card {
    transform: scale(0.8);
  }

  .share-instructions {
    margin-top: 0.8rem;
  }

  .instruction-text {
    font-size: 0.9rem;
  }

  .share-btn {
    padding: 0.9rem 1.5rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 400px) {
  .shareable-section {
    padding: 1rem 0.25rem;
  }

  .section-title {
    font-size: 1.3rem;
    margin-bottom: 0.8rem;
  }

  .story-card {
    transform: scale(0.75);
  }

  .share-instructions {
    margin-top: 0.5rem;
  }

  .instruction-text {
    font-size: 0.85rem;
  }

  .share-btn {
    padding: 0.8rem 1.3rem;
    font-size: 0.85rem;
  }
}

@media (max-width: 340px) {
  .shareable-section {
    padding: 0.75rem 0.25rem;
  }

  .section-title {
    font-size: 1.2rem;
    margin-bottom: 0.6rem;
  }

  .story-card {
    transform: scale(0.7);
  }

  .share-instructions {
    margin-top: 0.3rem;
  }

  .instruction-text {
    font-size: 0.8rem;
  }

  .share-btn {
    padding: 0.75rem 1.2rem;
    font-size: 0.8rem;
  }

  .btn-icon {
    font-size: 1rem;
  }
}
</style>
