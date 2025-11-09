<template>
  <section class="section monthly-progress-section">
    <div class="content-wrapper">
      <div class="tag">Monthly Progress</div>
      <h2 class="section-title">Champion Performance Over Time</h2>

      <!-- Champion Selection Grid -->
      <div class="champions-selector">
        <h3 class="selector-title">Select a Champion</h3>
        <div class="champions-grid">
          <div
            v-for="(champion, index) in topChampions"
            :key="champion.name"
            class="champion-selector-card"
            :class="{ active: selectedChampion === champion.name }"
            @click="selectChampion(champion.name)"
          >
            <div class="rank-number">#{{ index + 1 }}</div>
            <div class="champion-mini-portrait">
              <img
                :src="getChampionImage(champion.name)"
                :alt="champion.name"
                @error="handleImageError"
              />
            </div>
            <div class="champion-mini-info">
              <div class="champion-mini-name">{{ formatChampionName(champion.name) }}</div>
              <div class="champion-mini-games">{{ champion.totalGames }} games</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div v-if="selectedChampion" class="charts-container">
        <div class="selected-champion-header">
          <img
            :src="getChampionImage(selectedChampion)"
            :alt="selectedChampion"
            class="selected-champion-portrait"
            @error="handleImageError"
          />
          <h3 class="selected-champion-title">
            {{ formatChampionName(selectedChampion) }} Performance
          </h3>
        </div>

        <!-- Stats Grid -->
        <div class="stats-overview">
          <div class="stat-card">
            <div class="stat-label">Total Games</div>
            <div class="stat-value">{{ championStats.totalGames }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Win Rate</div>
            <div class="stat-value">{{ championStats.avgWinRate.toFixed(1) }}%</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Avg KDA</div>
            <div class="stat-value">{{ championStats.avgKDA.toFixed(2) }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Months Played</div>
            <div class="stat-value">{{ championStats.monthsPlayed }}</div>
          </div>
        </div>

        <!-- Performance Charts -->
        <div class="charts-grid">
          <div class="chart-card">
            <h4 class="chart-title">Win Rate Over Time</h4>
            <canvas ref="winRateChart"></canvas>
          </div>

          <div class="chart-card">
            <h4 class="chart-title">KDA Progression</h4>
            <canvas ref="kdaChart"></canvas>
          </div>

          <div class="chart-card">
            <h4 class="chart-title">Damage to Champions</h4>
            <canvas ref="damageChart"></canvas>
          </div>

          <div class="chart-card">
            <h4 class="chart-title">CS Per Minute</h4>
            <canvas ref="csChart"></canvas>
          </div>

          <div class="chart-card">
            <h4 class="chart-title">Games Played Per Month</h4>
            <canvas ref="gamesChart"></canvas>
          </div>

          <div class="chart-card">
            <h4 class="chart-title">Vision Score</h4>
            <canvas ref="visionChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Initial State -->
      <div v-else class="no-selection">
        <div class="no-selection-icon">📊</div>
        <p>Select a champion to view their monthly performance</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

const DDRAGON_VERSION = '15.22.1'
const selectedChampion = ref(null)
const winRateChart = ref(null)
const kdaChart = ref(null)
const damageChart = ref(null)
const csChart = ref(null)
const gamesChart = ref(null)
const visionChart = ref(null)

let chartInstances = {}

// Get top 10 champions by total games played
const topChampions = computed(() => {
  const championMap = new Map()

  props.data.forEach(entry => {
    const existing = championMap.get(entry.champion)
    if (existing) {
      existing.totalGames += entry.games
    } else {
      championMap.set(entry.champion, {
        name: entry.champion,
        totalGames: entry.games
      })
    }
  })

  return Array.from(championMap.values())
    .sort((a, b) => b.totalGames - a.totalGames)
    .slice(0, 10)
})

// Get data for selected champion, merging entries from different roles in the same month
const selectedChampionData = computed(() => {
  if (!selectedChampion.value) return []

  // Filter entries for selected champion
  const championEntries = props.data.filter(entry => entry.champion === selectedChampion.value)

  // Group by year-month key, merging different roles
  const monthlyMap = new Map()

  championEntries.forEach(entry => {
    const key = `${entry.year}-${entry.month_number}`
    const existing = monthlyMap.get(key)

    if (existing) {
      // Merge data from different roles in the same month
      const totalGames = existing.games + entry.games

      // Weighted averages based on number of games
      existing.games = totalGames
      existing.winrate = ((existing.winrate * existing.totalGamesForAvg) + (entry.winrate * entry.games)) / totalGames
      existing.avg_kda = ((existing.avg_kda * existing.totalGamesForAvg) + (entry.avg_kda * entry.games)) / totalGames
      existing.avg_dmg_to_champs = ((existing.avg_dmg_to_champs * existing.totalGamesForAvg) + (entry.avg_dmg_to_champs * entry.games)) / totalGames
      existing.avg_cs_per_min = ((existing.avg_cs_per_min * existing.totalGamesForAvg) + (entry.avg_cs_per_min * entry.games)) / totalGames
      existing.avg_vision_score = ((existing.avg_vision_score * existing.totalGamesForAvg) + (entry.avg_vision_score * entry.games)) / totalGames
      existing.totalGamesForAvg = totalGames
    } else {
      // First entry for this month
      monthlyMap.set(key, {
        ...entry,
        totalGamesForAvg: entry.games // Track for weighted average calculations
      })
    }
  })

  // Convert map to array and sort by date
  return Array.from(monthlyMap.values())
    .sort((a, b) => {
      if (a.year !== b.year) return a.year - b.year
      return a.month_number - b.month_number
    })
})

// Calculate stats for selected champion
const championStats = computed(() => {
  if (!selectedChampionData.value.length) {
    return {
      totalGames: 0,
      avgWinRate: 0,
      avgKDA: 0,
      monthsPlayed: 0
    }
  }

  const data = selectedChampionData.value
  const totalGames = data.reduce((sum, entry) => sum + entry.games, 0)
  const avgWinRate = data.reduce((sum, entry) => sum + entry.winrate, 0) / data.length
  const avgKDA = data.reduce((sum, entry) => sum + entry.avg_kda, 0) / data.length

  return {
    totalGames,
    avgWinRate,
    avgKDA,
    monthsPlayed: data.length
  }
})

const getChampionImage = (championName) => {
  const cleanName = championName.replace(/[^a-zA-Z]/g, '')
  return `https://ddragon.leagueoflegends.com/cdn/${DDRAGON_VERSION}/img/champion/${cleanName}.png`
}

const handleImageError = (event) => {
  event.target.src = 'https://ddragon.leagueoflegends.com/cdn/15.22.1/img/profileicon/29.png'
}

const formatChampionName = (name) => {
  return name.replace(/([A-Z])/g, ' $1').trim()
}

const selectChampion = (championName) => {
  selectedChampion.value = championName
}

// Destroy all existing charts
const destroyCharts = () => {
  Object.values(chartInstances).forEach(chart => {
    if (chart) chart.destroy()
  })
  chartInstances = {}
}

// Create charts
const createCharts = async () => {
  await nextTick()
  destroyCharts()

  const data = selectedChampionData.value
  if (!data.length) return

  const labels = data.map(entry => `${entry.month_name.substring(0, 3)} ${entry.year}`)

  // Chart.js default options
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 2,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        backgroundColor: 'rgba(10, 20, 40, 0.9)',
        titleColor: '#c89b3c',
        bodyColor: '#f0e6d2',
        borderColor: '#c89b3c',
        borderWidth: 1,
        padding: 12,
        displayColors: false
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(200, 155, 60, 0.1)'
        },
        ticks: {
          color: '#c89b3c'
        }
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(200, 155, 60, 0.1)'
        },
        ticks: {
          color: '#c89b3c'
        }
      }
    }
  }

  // Win Rate Chart
  if (winRateChart.value) {
    chartInstances.winRate = new Chart(winRateChart.value, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Win Rate (%)',
          data: data.map(entry => entry.winrate),
          borderColor: '#0397ab',
          backgroundColor: 'rgba(3, 151, 171, 0.1)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#0397ab',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: {
        ...defaultOptions,
        scales: {
          ...defaultOptions.scales,
          y: {
            ...defaultOptions.scales.y,
            min: 0,
            max: 100
          }
        }
      }
    })
  }

  // KDA Chart
  if (kdaChart.value) {
    chartInstances.kda = new Chart(kdaChart.value, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'KDA',
            data: data.map(entry => entry.avg_kda),
            borderColor: '#c89b3c',
            backgroundColor: 'rgba(200, 155, 60, 0.1)',
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#c89b3c',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7
          }
        ]
      },
      options: defaultOptions
    })
  }

  // Damage Chart
  if (damageChart.value) {
    chartInstances.damage = new Chart(damageChart.value, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Avg Damage',
          data: data.map(entry => entry.avg_dmg_to_champs),
          backgroundColor: 'rgba(255, 70, 85, 0.7)',
          borderColor: '#ff4655',
          borderWidth: 2
        }]
      },
      options: defaultOptions
    })
  }

  // CS Chart
  if (csChart.value) {
    chartInstances.cs = new Chart(csChart.value, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'CS/min',
          data: data.map(entry => entry.avg_cs_per_min),
          borderColor: '#5bc0de',
          backgroundColor: 'rgba(91, 192, 222, 0.1)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#5bc0de',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: defaultOptions
    })
  }

  // Games Chart
  if (gamesChart.value) {
    chartInstances.games = new Chart(gamesChart.value, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Games Played',
          data: data.map(entry => entry.games),
          backgroundColor: 'rgba(200, 155, 60, 0.7)',
          borderColor: '#c89b3c',
          borderWidth: 2
        }]
      },
      options: {
        ...defaultOptions,
        scales: {
          ...defaultOptions.scales,
          y: {
            ...defaultOptions.scales.y,
            ticks: {
              ...defaultOptions.scales.y.ticks,
              stepSize: 1
            }
          }
        }
      }
    })
  }

  // Vision Chart
  if (visionChart.value) {
    chartInstances.vision = new Chart(visionChart.value, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Vision Score',
          data: data.map(entry => entry.avg_vision_score),
          borderColor: '#f39c12',
          backgroundColor: 'rgba(243, 156, 18, 0.1)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#f39c12',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: defaultOptions
    })
  }
}

// Watch for champion selection changes
watch(selectedChampion, () => {
  if (selectedChampion.value) {
    createCharts()
  }
})

// Select first champion on mount
onMounted(() => {
  if (topChampions.value.length > 0) {
    selectedChampion.value = topChampions.value[0].name
  }
})
</script>

<style scoped>
.monthly-progress-section {
  background: radial-gradient(circle at 50% 50%, rgba(200, 155, 60, 0.05) 0%, transparent 50%);
  min-height: auto;
  padding: 4rem 2rem;
}

.content-wrapper {
  max-width: 1400px;
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
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 900;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-gold-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Champion Selector */
.champions-selector {
  margin-bottom: 3rem;
}

.selector-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--lol-gold-light);
  margin-bottom: 1.5rem;
}

.champions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.champion-selector-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.6), rgba(10, 20, 40, 0.4));
  border: 2px solid rgba(200, 155, 60, 0.2);
  border-radius: 12px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.champion-selector-card:hover {
  border-color: var(--lol-gold);
  transform: translateX(5px);
  box-shadow: 0 5px 20px rgba(200, 155, 60, 0.3);
}

.champion-selector-card.active {
  border-color: var(--lol-gold);
  background: linear-gradient(135deg, rgba(200, 155, 60, 0.2), rgba(200, 155, 60, 0.1));
  box-shadow: 0 5px 20px rgba(200, 155, 60, 0.4);
}

.rank-number {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: var(--lol-gold);
  color: var(--lol-dark);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.7rem;
}

.champion-mini-portrait {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid var(--lol-gold);
  flex-shrink: 0;
}

.champion-mini-portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.champion-mini-info {
  flex: 1;
  min-width: 0;
}

.champion-mini-name {
  font-size: 1rem;
  font-weight: 700;
  color: var(--lol-gold-light);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.champion-mini-games {
  font-size: 0.85rem;
  color: var(--lol-gold);
}

/* Selected Champion Header */
.selected-champion-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(10, 20, 40, 0.6));
  border: 2px solid var(--lol-gold);
  border-radius: 15px;
}

.selected-champion-portrait {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid var(--lol-gold);
}

.selected-champion-title {
  font-size: 2rem;
  font-weight: 900;
  color: var(--lol-gold);
}

/* Stats Overview */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.6), rgba(10, 20, 40, 0.4));
  border: 2px solid rgba(200, 155, 60, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: var(--lol-gold);
  transform: translateY(-3px);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--lol-gold-light);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 2rem;
  font-weight: 900;
  color: var(--lol-gold);
}

/* Charts */
.charts-container {
  margin-top: 3rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
}

.chart-card {
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(10, 20, 40, 0.6));
  border: 2px solid rgba(200, 155, 60, 0.2);
  border-radius: 15px;
  padding: 2rem;
  transition: all 0.3s ease;
}

.chart-card:hover {
  border-color: var(--lol-gold);
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.2);
}

.chart-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--lol-gold-light);
  margin-bottom: 1.5rem;
  text-align: center;
}

/* No Selection State */
.no-selection {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--lol-gold-light);
}

.no-selection-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.no-selection p {
  font-size: 1.2rem;
}

@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .champions-grid {
    grid-template-columns: 1fr;
  }

  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }

  .selected-champion-header {
    flex-direction: column;
    text-align: center;
  }
}
</style>
