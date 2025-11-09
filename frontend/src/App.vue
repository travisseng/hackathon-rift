<template>
  <div class="lol-wrapped">
    <Particles id="particles" :options="particlesOptions" />

    <!-- Input Form - Show when no data loaded -->
    <SummonerInput
      v-if="!statsData"
      ref="summonerInputRef"
      @submit="handleFetchStats"
    />

    <!-- Main Content - Show when data is loaded -->
    <template v-else>
      <!-- Tab Navigation -->
      <div class="tabs-container">
        <button class="mobile-menu-toggle" @click="toggleMobileMenu">
          <span class="hamburger-icon" :class="{ open: mobileMenuOpen }">
            <span></span>
            <span></span>
            <span></span>
          </span>
          <span class="current-tab-label">{{ getCurrentTabLabel() }}</span>
        </button>
        <div class="tabs-wrapper" :class="{ 'mobile-open': mobileMenuOpen }">
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'wrapped' }"
            @click="switchTab('wrapped')"
          >
            <span class="tab-icon">🎁</span>
            <span class="tab-text">Wrapped</span>
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'analysis' }"
            @click="switchTab('analysis')"
          >
            <span class="tab-icon">📊</span>
            <span class="tab-text">Game Analysis</span>
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'monthly' }"
            @click="switchTab('monthly')"
          >
            <span class="tab-icon">📈</span>
            <span class="tab-text">Monthly Progress</span>
          </button>
          <button class="reset-btn" @click="resetApp">
            <span>↻</span> New Search
          </button>
        </div>
      </div>

      <!-- Wrapped Tab Content -->
      <template v-if="activeTab === 'wrapped'">
        <!-- Hero Section -->
        <section ref="heroSection" class="section hero-section">
          <div class="hero-content">
            <h1 class="hero-title">Your League of Legends</h1>
            <h2 class="hero-subtitle gradient-text">2025 RANKED WRAPPED</h2>
            <div class="scroll-indicator">
              <span>Scroll to reveal</span>
              <div class="scroll-arrow"></div>
            </div>
          </div>
        </section>

        <!-- Overview Section -->
        <OverviewSection
          ref="overviewSection"
          :data="statsData.overview"
          :insights="statsData.aiInsights?.overview || []"
          :title="statsData.aiInsights?.player_title || ''"
        />

        <!-- Most Played & Role Performance Section -->
        <MostPlayedRoleSection
          ref="mostPlayedRoleSection"
          :most-played-data="statsData.most_played"
          :role-performance-data="statsData.role_performance"
          :insights="[
            ...(statsData.aiInsights?.most_played || []),
            ...(statsData.aiInsights?.role_performance || [])
          ]"
        />

        <!-- Time Stats Section -->
        <TimeStatsSection
          ref="timeStatsSection"
          :data="statsData.time_stats"
          :insights="statsData.aiInsights?.time_stats || []"
        />

        <!-- Combat Stats Section -->
        <CombatStatsSection
          ref="combatStatsSection"
          :data="statsData.combat_stats"
          :insights="statsData.aiInsights?.combat_stats || []"
        />

        <!-- Economy Stats Section -->
        <EconomyStatsSection
          ref="economyStatsSection"
          :data="statsData.economy_stats"
          :insights="statsData.aiInsights?.economy_stats || []"
        />

        <!-- Damage Stats Section -->
        <DamageStatsSection
          ref="damageStatsSection"
          :data="statsData.damage_stats"
          :insights="statsData.aiInsights?.damage_stats || []"
        />

        <!-- Vision Stats Section -->
        <VisionStatsSection
          ref="visionStatsSection"
          :data="statsData.vision_stats"
          :insights="statsData.aiInsights?.vision_stats || []"
        />

        <!-- Objectives Section -->
        <ObjectivesSection
          ref="objectivesSection"
          :data="statsData.objectives"
          :insights="statsData.aiInsights?.objectives || statsData.aiInsights?.objective || []"
        />

        <!-- Communication Section -->
        <CommunicationSection
          ref="communicationSection"
          :data="statsData.ping_stats"
          :insights="statsData.aiInsights?.ping_stats || []"
        />

        

        <!-- Shareable Card Section -->
        <ShareableCard
          v-if="statsData"
          :data="statsData"
          :account-data="accountData"
          :summoner-name="summonerDetails.summonerName"
          :summoner-tag="summonerDetails.tagLine"
          @reset="resetApp"
        />
      </template>

      <!-- Analysis Tab Content -->
      <template v-if="activeTab === 'analysis'">
        <!-- Loading State -->
        <section v-if="gamesLoading" class="section analysis-section">
          <div class="analysis-message">
            <div class="loading-spinner"></div>
            <p>Loading game history...</p>
          </div>
        </section>

        <!-- Error State -->
        <section v-else-if="gamesError" class="section analysis-section">
          <div class="analysis-message error">
            <span class="error-icon">⚠️</span>
            <p>{{ gamesError }}</p>
            <button class="retry-btn" @click="fetchGames">Try Again</button>
          </div>
        </section>

        <!-- Game History or Analysis -->
        <template v-else>
          <GameHistory
            v-if="!selectedGame"
            :games="gamesData"
            :game-tag="summonerDetails.tagLine"
            :score-summaries="scoreSummaries"
            :loading-scores="loadingScores"
            :current-page="gamesCurrentPage"
            :page-size="gamesPageSize"
            :has-more="gamesHasMore"
            :total-games="gamesTotalCount"
            @analyze="handleAnalyzeGame"
            @update-score="handleScoreUpdate"
            @update-loading="handleLoadingUpdate"
            @page-change="handlePageChange"
          />

          <!-- Analysis Loading State -->
          <section v-else-if="analysisLoading" class="section analysis-section">
            <div class="analysis-message">
              <div class="loading-spinner"></div>
              <p class="loading-text">{{ analysisLoadingMessage }}</p>
            </div>
          </section>

          <!-- Analysis Error State -->
          <section v-else-if="analysisError" class="section analysis-section">
            <div class="analysis-message error">
              <span class="error-icon">⚠️</span>
              <p>{{ analysisError }}</p>
              <button class="retry-btn" @click="handleAnalyzeGame(selectedGame.matchId)">Try Again</button>
              <button class="back-btn" @click="handleBackToGames">Back to Games</button>
            </div>
          </section>

          <!-- Game Analysis -->
          <GameAnalysis v-else-if="selectedGame && analysisData" :analysisData="analysisData" :gameData="selectedGame" @back="handleBackToGames" />
        </template>
      </template>

      <!-- Monthly Progress Tab Content -->
      <template v-if="activeTab === 'monthly'">
        <!-- Loading State -->
        <section v-if="monthlyLoading" class="section monthly-section">
          <div class="analysis-message">
            <div class="loading-spinner"></div>
            <p>Loading monthly progress...</p>
          </div>
        </section>

        <!-- Error State -->
        <section v-else-if="monthlyError" class="section monthly-section">
          <div class="analysis-message error">
            <span class="error-icon">⚠️</span>
            <p>{{ monthlyError }}</p>
            <button class="retry-btn" @click="fetchMonthly">Try Again</button>
          </div>
        </section>

        <!-- Monthly Progress Data -->
        <MonthlyProgressSection v-else-if="monthlyData.length > 0" :data="monthlyData" />

        <!-- No Data State -->
        <section v-else class="section monthly-section">
          <div class="analysis-message">
            <span class="error-icon">📊</span>
            <p>No monthly progress data available</p>
          </div>
        </section>
      </template>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SummonerInput from './components/SummonerInput.vue'
import OverviewSection from './components/OverviewSection.vue'
import TimeStatsSection from './components/TimeStatsSection.vue'
import CombatStatsSection from './components/CombatStatsSection.vue'
import EconomyStatsSection from './components/EconomyStatsSection.vue'
import DamageStatsSection from './components/DamageStatsSection.vue'
import VisionStatsSection from './components/VisionStatsSection.vue'
import ObjectivesSection from './components/ObjectivesSection.vue'
import CommunicationSection from './components/CommunicationSection.vue'
import MostPlayedRoleSection from './components/MostPlayedRoleSection.vue'
import ShareableCard from './components/ShareableCard.vue'
import GameHistory from './components/GameHistory.vue'
import GameAnalysis from './components/GameAnalysis.vue'
import MonthlyProgressSection from './components/MonthlyProgressSection.vue'
import { fetchPlayerStats, fetchAllGames, analyzeGame, fetchMonthlyProgress, fetchAccountData } from './utils/api'

gsap.registerPlugin(ScrollTrigger)

// Refs
const summonerInputRef = ref(null)
const statsData = ref(null)
const activeTab = ref('wrapped')
const selectedGame = ref(null)
const gamesData = ref([])
const gamesLoading = ref(false)
const gamesError = ref(null)
const mobileMenuOpen = ref(false)

// Pagination state
const gamesCurrentPage = ref(1)
const gamesPageSize = ref(10)
const gamesHasMore = ref(false)
const gamesTotalCount = ref(0)

// Cache for fetched game pages
const gamesPagesCache = ref(new Map())

// Score summaries cache
const scoreSummaries = ref({})
const loadingScores = ref({})

// Analysis state
const analysisData = ref(null)
const analysisLoading = ref(false)
const analysisError = ref(null)
const analysisLoadingMessage = ref('')

// Funny League of Legends themed loading messages
const loadingMessages = [
  "Calculating your int score...",
  "Summoning Faker's ghost for analysis...",
  "Blaming the jungler...",
  "Checking if you actually warded...",
  "Analyzing Flash usage... why didn't you Flash?",
  "Questioning your build choices...",
  "Reviewing your ? ping frequency...",
  "Calculating LP loss... probably -18",
  "Checking respawn timers... you were grey a lot",
  "Analyzing all-chat messages... oh no",
  "Detecting face-checking bushes...",
  "Counting times you chased Singed...",
  "Checking if you honored your support...",
  "Analyzing CS per minute... yikes",
  "Reviewing your ult usage... or lack thereof",
  "Calculating toxicity levels in chat...",
  "Checking if you invaded without vision...",
  "Analyzing your 0/10 powerspike timing...",
  "Detecting rage quit probability...",
  "Checking if you took Gromp from your jungler...",
  "Analyzing whether you greeted your team...",
  "Counting your missed skill shots...",
  "Reviewing your mastery 7 emote spam...",
  "Checking if you helped your jungler with scuttle...",
  "Analyzing your ability to dodge skill shots...",
  "Calculating how many objectives you slept through...",
  "Checking if you pinged 'enemy missing'... you didn't",
  "Analyzing your klepto addiction...",
  "Reviewing your attempt to 1v5...",
  "Checking if you bought control wards... narrator: they didn't"
]

// Randomly select and rotate loading messages
const startLoadingMessageRotation = () => {
  // Set initial random message
  analysisLoadingMessage.value = loadingMessages[Math.floor(Math.random() * loadingMessages.length)]

  // Rotate messages every 2.5 seconds
  const interval = setInterval(() => {
    if (!analysisLoading.value) {
      clearInterval(interval)
      return
    }
    analysisLoadingMessage.value = loadingMessages[Math.floor(Math.random() * loadingMessages.length)]
  }, 2500)

  return interval
}

let loadingMessageInterval = null

// Monthly progress state
const monthlyData = ref([])
const monthlyLoading = ref(false)
const monthlyError = ref(null)

// Account data state (rank, etc.)
const accountData = ref(null)

// Store summoner details for API calls
const summonerDetails = ref({
  summonerName: '',
  tagLine: '',
  region: '',
  puuid: ''
})

// Fetch games from API with pagination
const fetchGames = async (page = 1) => {
  if (!summonerDetails.value.summonerName) {
    return // Don't fetch if no summoner
  }

  // Check if this page is already cached
  if (gamesPagesCache.value.has(page)) {
    console.log(`Page ${page} already cached, using cached data`)
    const cachedData = gamesPagesCache.value.get(page)
    gamesData.value = cachedData.files
    gamesCurrentPage.value = cachedData.page
    gamesHasMore.value = cachedData.has_more
    gamesTotalCount.value = cachedData.total_files
    return
  }

  gamesLoading.value = true
  gamesError.value = null

  try {
    const result = await fetchAllGames(
      summonerDetails.value.summonerName,
      summonerDetails.value.tagLine,
      summonerDetails.value.region,
      summonerDetails.value.puuid,
      page,
      gamesPageSize.value
    )

    // Sort games by gameCreation timestamp (most recent first)
    const sortedGames = result.files.sort((a, b) => {
      const timestampA = a.gameCreation || 0
      const timestampB = b.gameCreation || 0
      return timestampB - timestampA // Descending order
    })

    // Update state
    gamesData.value = sortedGames
    gamesCurrentPage.value = result.page
    gamesHasMore.value = result.has_more
    gamesTotalCount.value = result.total_files

    // Cache the page data
    gamesPagesCache.value.set(page, {
      files: sortedGames,
      page: result.page,
      has_more: result.has_more,
      total_files: result.total_files
    })
  } catch (error) {
    console.error('Error fetching games:', error)
    gamesError.value = error.message || 'Failed to fetch game history'
  } finally {
    gamesLoading.value = false
  }
}

// Fetch monthly progress from API
const fetchMonthly = async () => {
  if (!summonerDetails.value.summonerName || monthlyData.value.length > 0) {
    return // Don't fetch if no summoner or already fetched
  }

  monthlyLoading.value = true
  monthlyError.value = null

  try {
    const data = await fetchMonthlyProgress(
      summonerDetails.value.summonerName,
      summonerDetails.value.tagLine
    )

    monthlyData.value = data
  } catch (error) {
    console.error('Error fetching monthly progress:', error)
    monthlyError.value = error.message || 'Failed to fetch monthly progress'
  } finally {
    monthlyLoading.value = false
  }
}

// Fetch account data (rank, profile icon, etc.)
const fetchAccount = async () => {
  if (!summonerDetails.value.summonerName || accountData.value) {
    return // Don't fetch if no summoner or already fetched
  }

  try {
    const data = await fetchAccountData(
      summonerDetails.value.summonerName,
      summonerDetails.value.tagLine
    )

    accountData.value = data
  } catch (error) {
    console.error('Error fetching account data:', error)
    // Non-critical, so we don't show error to user
  }
}

// API Handler Functions
const handleFetchStats = async ({ summonerName, tagLine, region, puuid }) => {
  try {
    const data = await fetchPlayerStats(summonerName, tagLine, region)
    statsData.value = data

    // Store summoner details for future API calls
    summonerDetails.value = { summonerName, tagLine, region, puuid }

    // Wait for DOM update, then initialize animations
    await nextTick()
    initializeAnimations()

    // Fetch games, monthly data, and account data in the background
    fetchGames()
    fetchMonthly()
    fetchAccount()
  } catch (error) {
    const errorMessage = error.message || 'Failed to fetch player stats. Please check the summoner name and try again.'
    summonerInputRef.value?.setError(errorMessage)
    summonerInputRef.value?.setLoading(false)
  }
}

const resetApp = () => {
  statsData.value = null
  activeTab.value = 'wrapped'
  selectedGame.value = null
  gamesData.value = []
  gamesError.value = null
  gamesCurrentPage.value = 1
  gamesPageSize.value = 10
  gamesHasMore.value = false
  gamesTotalCount.value = 0
  gamesPagesCache.value.clear()
  analysisData.value = null
  analysisError.value = null
  monthlyData.value = []
  monthlyError.value = null
  scoreSummaries.value = {}
  loadingScores.value = {}
  accountData.value = null
  summonerDetails.value = { summonerName: '', tagLine: '', region: '', puuid: '' }
  mobileMenuOpen.value = false
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const switchTab = (tab) => {
  activeTab.value = tab
  selectedGame.value = null
  analysisData.value = null
  analysisError.value = null
  mobileMenuOpen.value = false // Close mobile menu when switching tabs

  // Fetch games when switching to analysis tab if not already loaded
  if (tab === 'analysis' && gamesPagesCache.value.size === 0 && !gamesLoading.value) {
    fetchGames(1)
  }

  // Fetch monthly data when switching to monthly tab if not already loaded
  if (tab === 'monthly' && monthlyData.value.length === 0 && !monthlyLoading.value) {
    fetchMonthly()
  }

  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const getCurrentTabLabel = () => {
  const labels = {
    'wrapped': '🎁 Wrapped',
    'analysis': '📊 Game Analysis',
    'monthly': '📈 Monthly Progress'
  }
  return labels[activeTab.value] || 'Menu'
}

// Close mobile menu on scroll
const handleScroll = () => {
  if (mobileMenuOpen.value) {
    mobileMenuOpen.value = false
  }
}

// Setup scroll listener
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// Handle page change from GameHistory
const handlePageChange = (page) => {
  fetchGames(page)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleBackToGames = () => {
  selectedGame.value = null
  analysisData.value = null
  analysisError.value = null
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleAnalyzeGame = async (gameId) => {
  // Find the full game object
  const gameObject = gamesData.value.find(game => game.matchId === gameId)
  selectedGame.value = gameObject

  analysisLoading.value = true
  analysisError.value = null
  analysisData.value = null

  // Start rotating funny loading messages
  loadingMessageInterval = startLoadingMessageRotation()

  window.scrollTo({ top: 0, behavior: 'smooth' })

  try {
    const analysis = await analyzeGame(
      summonerDetails.value.summonerName,
      summonerDetails.value.tagLine,
      summonerDetails.value.region,
      gameId,
      summonerDetails.value.puuid
    )
    analysisData.value = analysis

    // Update the score summary cache with the analysis result
    if (analysis && analysis.final_verdict) {
      scoreSummaries.value[gameId] = {
        score: analysis.final_verdict.score,
        tags: analysis.final_verdict.tags || [],
        summary: analysis.final_verdict.summary || 'Analysis complete',
        error: false
      }
    }
  } catch (error) {
    console.error('Error analyzing game:', error)
    analysisError.value = error.message || 'Failed to analyze game'
  } finally {
    analysisLoading.value = false
    // Clear the loading message interval
    if (loadingMessageInterval) {
      clearInterval(loadingMessageInterval)
      loadingMessageInterval = null
    }
  }
}

// Handle score summary updates from GameHistory
const handleScoreUpdate = (matchId, scoreData) => {
  scoreSummaries.value[matchId] = scoreData
}

// Handle loading state updates from GameHistory
const handleLoadingUpdate = (matchId, isLoading) => {
  loadingScores.value[matchId] = isLoading
}

const initializeAnimations = () => {
  // Hero section animation
  gsap.from('.hero-title', {
    opacity: 0,
    y: -50,
    duration: 1,
    ease: 'power3.out'
  })

  gsap.from('.hero-subtitle', {
    opacity: 0,
    y: 50,
    duration: 1,
    delay: 0.3,
    ease: 'power3.out'
  })

  gsap.from('.scroll-indicator', {
    opacity: 0,
    y: 20,
    duration: 1,
    delay: 0.6,
    ease: 'power3.out'
  })

  // Scroll indicator animation
  gsap.to('.scroll-arrow', {
    y: 10,
    duration: 0.8,
    repeat: -1,
    yoyo: true,
    ease: 'power1.inOut'
  })

  // Section fade-in animations
  const sections = document.querySelectorAll('.section:not(.hero-section)')
  sections.forEach((section) => {
    gsap.from(section, {
      scrollTrigger: {
        trigger: section,
        start: 'top 80%',
        toggleActions: 'play none none reverse'
      },
      opacity: 0,
      y: 50,
      duration: 1,
      ease: 'power3.out'
    })
  })
}

// Particles configuration
const particlesOptions = {
  background: {
    color: {
      value: 'transparent'
    }
  },
  fpsLimit: 60,
  particles: {
    color: {
      value: ['#c89b3c', '#0397ab', '#f0e6d2']
    },
    links: {
      enable: false
    },
    move: {
      enable: true,
      speed: 1,
      direction: 'none',
      random: true,
      straight: false,
      outModes: {
        default: 'out'
      }
    },
    number: {
      value: 50,
      density: {
        enable: true,
        area: 800
      }
    },
    opacity: {
      value: { min: 0.1, max: 0.5 },
      animation: {
        enable: true,
        speed: 1,
        minimumValue: 0.1
      }
    },
    shape: {
      type: 'circle'
    },
    size: {
      value: { min: 1, max: 3 }
    }
  },
  detectRetina: true
}

// Refs for sections (used for animations)
const heroSection = ref(null)
const overviewSection = ref(null)
const timeStatsSection = ref(null)
const combatStatsSection = ref(null)
const economyStatsSection = ref(null)
const damageStatsSection = ref(null)
const visionStatsSection = ref(null)
const objectivesSection = ref(null)
const communicationSection = ref(null)
const mostPlayedRoleSection = ref(null)
</script>

<style scoped>
.lol-wrapped {
  position: relative;
  width: 100%;
}

#particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  z-index: 1;
}

/* Hero Section */
.hero-section {
  background: radial-gradient(circle at center, rgba(200, 155, 60, 0.1) 0%, transparent 70%);
}

.hero-content {
  text-align: center;
  max-width: 800px;
}

.hero-title {
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 300;
  letter-spacing: 0.1em;
  margin-bottom: 1rem;
  color: var(--lol-gold-light);
}

.hero-subtitle {
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 900;
  letter-spacing: 0.05em;
  margin-bottom: 3rem;
}

.scroll-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 4rem;
  color: var(--lol-gold);
  font-size: 0.9rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.scroll-arrow {
  width: 2px;
  height: 30px;
  background: linear-gradient(to bottom, var(--lol-gold), transparent);
}

/* Tab Navigation */
.tabs-container {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10, 20, 40, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 2px solid rgba(200, 155, 60, 0.3);
  padding: 1rem 2rem;
}

.mobile-menu-toggle {
  display: none;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 0.8rem 1rem;
  background: rgba(200, 155, 60, 0.1);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 10px;
  color: var(--lol-gold-light);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-menu-toggle:hover {
  background: rgba(200, 155, 60, 0.15);
  border-color: var(--lol-gold);
}

.hamburger-icon {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 24px;
  height: 20px;
  position: relative;
}

.hamburger-icon span {
  display: block;
  width: 100%;
  height: 3px;
  background: var(--lol-gold);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.hamburger-icon.open span:nth-child(1) {
  transform: rotate(45deg) translate(8px, 8px);
}

.hamburger-icon.open span:nth-child(2) {
  opacity: 0;
}

.hamburger-icon.open span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -7px);
}

.current-tab-label {
  flex: 1;
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.tabs-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 1rem 2rem;
  background: transparent;
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 10px;
  color: var(--lol-gold-light);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.tab-btn:hover {
  background: rgba(200, 155, 60, 0.1);
  border-color: var(--lol-gold);
  transform: translateY(-2px);
}

.tab-btn.active {
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-gold-light));
  border-color: var(--lol-gold);
  color: var(--lol-dark);
  box-shadow: 0 5px 20px rgba(200, 155, 60, 0.4);
}

.tab-icon {
  font-size: 1.3rem;
}

.tab-text {
  font-size: 0.9rem;
}

.reset-btn {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  background: transparent;
  border: 2px solid rgba(255, 70, 85, 0.5);
  border-radius: 10px;
  color: #ff4655;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.reset-btn:hover {
  background: rgba(255, 70, 85, 0.1);
  border-color: #ff4655;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .section {
    padding: 2rem 1rem;
  }

  .tabs-container {
    padding: 0.5rem;
  }

  .mobile-menu-toggle {
    display: flex;
  }

  .tabs-wrapper {
    flex-direction: column;
    gap: 0.6rem;
    max-height: 0;
    overflow: hidden;
    opacity: 0;
    margin-top: 0;
    transition: all 0.3s ease;
  }

  .tabs-wrapper.mobile-open {
    max-height: 500px;
    opacity: 1;
    margin-top: 0.8rem;
  }

  .tab-btn {
    width: 100%;
    justify-content: center;
    padding: 0.9rem 1rem;
    font-size: 0.8rem;
  }

  .tab-icon {
    font-size: 1.2rem;
  }

  .tab-text {
    font-size: 0.8rem;
  }

  .reset-btn {
    width: 100%;
    justify-content: center;
    margin-left: 0;
    padding: 0.9rem 1rem;
  }
}

@media (max-width: 480px) {
  .section {
    padding: 1.5rem 0.75rem;
  }

  .tabs-container {
    padding: 0.4rem;
  }

  .mobile-menu-toggle {
    padding: 0.7rem 0.8rem;
    font-size: 0.9rem;
  }

  .current-tab-label {
    font-size: 0.85rem;
  }

  .hamburger-icon {
    width: 20px;
    height: 16px;
    gap: 3px;
  }

  .hamburger-icon span {
    height: 2.5px;
  }

  .tab-btn {
    padding: 0.8rem 0.8rem;
    font-size: 0.75rem;
  }

  .tab-icon {
    font-size: 1.1rem;
  }

  .tab-text {
    font-size: 0.75rem;
  }

  .reset-btn {
    padding: 0.8rem 0.8rem;
    font-size: 0.75rem;
  }
}

/* Analysis Section Messages */
.analysis-section {
  background: radial-gradient(circle at 50% 50%, rgba(3, 151, 171, 0.08) 0%, transparent 60%);
}

/* Monthly Section Messages */
.monthly-section {
  background: radial-gradient(circle at 50% 50%, rgba(200, 155, 60, 0.08) 0%, transparent 60%);
}

.analysis-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 3rem;
  text-align: center;
}

.analysis-message p {
  font-size: 1.2rem;
  color: var(--lol-gold-light);
}

/* Loading text animation */
.loading-text {
  animation: fadeInOut 2.5s ease-in-out infinite;
  min-height: 1.5em;
}

@keyframes fadeInOut {
  0%, 100% {
    opacity: 0.7;
  }
  50% {
    opacity: 1;
  }
}

/* Loading Spinner */
.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(200, 155, 60, 0.2);
  border-top-color: var(--lol-gold);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Error State */
.analysis-message.error {
  color: #ff4655;
}

.error-icon {
  font-size: 3rem;
}

.analysis-message.error p {
  color: #ff4655;
}

.retry-btn {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-gold-light));
  color: var(--lol-dark);
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.retry-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 20px rgba(200, 155, 60, 0.4);
}

.back-btn {
  padding: 1rem 2rem;
  background: transparent;
  color: var(--lol-gold-light);
  border: 2px solid rgba(200, 155, 60, 0.5);
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.back-btn:hover {
  background: rgba(200, 155, 60, 0.1);
  border-color: var(--lol-gold);
  transform: scale(1.05);
}
</style>
