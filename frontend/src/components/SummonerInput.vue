<template>
  <div class="summoner-input-container">
    <div class="input-content">
      <div class="logo-section">
        <h1 class="title gradient-text">League of Legends</h1>
        <h2 class="subtitle">YOUR YEAR</h2>
      </div>

      <div class="input-form">
        <h3 class="form-title">Enter Your Summoner Info</h3>
        <p class="form-description">Discover your year in ranked in the Rift</p>

        <div v-if="searchHistory.length > 0" class="history-section">
          <button
            class="history-toggle"
            @click="showHistory = !showHistory"
            type="button"
          >
            <span>{{ showHistory ? '▼' : '▶' }} Recent Searches</span>
            <span class="history-count">{{ searchHistory.length }}</span>
          </button>

          <div v-if="showHistory" class="history-dropdown">
            <div class="history-items">
              <button
                v-for="(item, index) in searchHistory"
                :key="index"
                class="history-item"
                @click="loadFromHistory(item)"
                type="button"
              >
                <div class="history-item-main">
                  <span class="history-name">{{ item.summonerName }}#{{ item.tagLine }}</span>
                  <span class="history-region">{{ item.region.toUpperCase() }}</span>
                </div>
                <span class="history-type">{{ item.rankedType === 'solo' ? 'Solo/Duo' : item.rankedType === 'flex' ? 'Flex' : 'Both' }}</span>
              </button>
            </div>
            <button class="clear-history-btn" @click="clearHistory" type="button">
              Clear History
            </button>
          </div>
        </div>

        <div class="input-group">
          <div class="input-wrapper">
            <label for="summonerName">Summoner Name</label>
            <input
              id="summonerName"
              v-model="summonerName"
              type="text"
              placeholder="e.g., Reive"
              @keyup.enter="handleSubmit"
              :disabled="loading"
            />
          </div>

          <div class="input-wrapper">
            <label for="tagLine">Tag</label>
            <input
              id="tagLine"
              v-model="tagLine"
              type="text"
              placeholder="e.g., EUW"
              @keyup.enter="handleSubmit"
              :disabled="loading"
            />
          </div>
        </div>

        <div class="region-select">
          <label for="region">Region</label>
          <select id="region" v-model="region" :disabled="loading">
            <optgroup label="Americas">
              <option value="na1">North America</option>
              <option value="br1">Brazil</option>
              <option value="la1">Latin America North</option>
              <option value="la2">Latin America South</option>
            </optgroup>
            <optgroup label="Europe">
              <option value="euw1">Europe West</option>
              <option value="eun1">Europe Nordic & East</option>
              <option value="tr1">Turkey</option>
              <option value="ru">Russia</option>
            </optgroup>
            <optgroup label="Asia">
              <option value="kr">Korea</option>
              <option value="jp1">Japan</option>
            </optgroup>
            <optgroup label="Southeast Asia">
              <option value="oc1">Oceania</option>
              <option value="ph2">Philippines</option>
              <option value="sg2">Singapore</option>
              <option value="th2">Thailand</option>
              <option value="tw2">Taiwan</option>
              <option value="vn2">Vietnam</option>
            </optgroup>
          </select>
        </div>

        <div class="ranked-type-select">
          <label for="rankedType">Queue Type</label>
          <select id="rankedType" v-model="rankedType" :disabled="loading">
            <option value="solo">Solo/Duo Queue</option>
            <option value="flex">Flex Queue</option>
            <option value="solo_and_flex">Both Queues</option>
          </select>
        </div>

        <button
          class="submit-button"
          @click="handleSubmit"
          :disabled="!canSubmit || loading"
        >
          <span v-if="!loading">Generate My Analysis</span>
          <span v-else class="loading-text">
            <span class="spinner"></span>
            Loading...
          </span>
        </button>

        <div v-if="loading" class="progress-container">
          <p v-if="funnyMessage" class="funny-message">{{ funnyMessage }}</p>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
          </div>
          <p class="progress-text">{{ progressMessage }}</p>
        </div>

        <p v-if="error" class="error-message">{{ error }}</p>

        <p class="privacy-note">
          We use the Riot Games API to fetch your match history. Your data is not stored.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, onMounted } from 'vue'

const emit = defineEmits(['submit'])

const summonerName = ref('')
const tagLine = ref('')
const region = ref('na1')
const rankedType = ref('solo')
const loading = ref(false)
const error = ref('')
const progress = ref(0)
const progressMessage = ref('')
const funnyMessage = ref('')
const showHistory = ref(false)
const searchHistory = ref([])

let ws = null
let funnyMessageInterval = null

const MAX_HISTORY_ITEMS = 10
const HISTORY_STORAGE_KEY = 'lol-wrapped-search-history'

// Funny League of Legends themed loading messages
const funnyLoadingMessages = [
  "Summoning the Rift Scuttler for data...",
  "Asking Teemo for your match history...",
  "Diving into the Nexus database...",
  "Checking if you bought boots...",
  "Calculating your Flash key placement...",
  "Consulting with the Ancient Rift Historians...",
  "Analyzing your ping excuse validity...",
  "Reviewing your 'my team held me back' claims...",
  "Counting how many times you died to red buff...",
  "Checking if you ever thanked your support...",
  "Analyzing your 'top diff' frequency...",
  "Summoning Baron to review your smite timings...",
  "Asking Ryze for another rework... I mean your stats...",
  "Checking if you ever played for objectives...",
  "Analyzing your 'JG diff' spam patterns...",
  "Reviewing your mastery 7 flex moments...",
  "Calculating your rage quit probability per game...",
  "Checking if you ever roamed as mid laner...",
  "Analyzing your ability to CS under tower...",
  "Reviewing your 'I'm smurfing' claims...",
  "Checking how many pentas you stole...",
  "Calculating times you blamed lag...",
  "Analyzing your 'worth' moments... they weren't...",
  "Checking if you ever placed a pink ward...",
  "Reviewing your Yasuo 0/10 powerspike data...",
  "Calculating your 'better jungle wins' ratio...",
  "Analyzing your champion puddle depth...",
  "Checking if you ever used the mute button...",
  "Reviewing your 'just one more game' decisions...",
  "Calculating your tilt trajectory across seasons..."
]

// Rotate funny messages during loading
const startFunnyMessageRotation = () => {
  // Set initial random message
  funnyMessage.value = funnyLoadingMessages[Math.floor(Math.random() * funnyLoadingMessages.length)]

  // Rotate messages every 2.5 seconds
  funnyMessageInterval = setInterval(() => {
    if (!loading.value) {
      clearInterval(funnyMessageInterval)
      funnyMessageInterval = null
      return
    }
    funnyMessage.value = funnyLoadingMessages[Math.floor(Math.random() * funnyLoadingMessages.length)]
  }, 2500)
}

const stopFunnyMessageRotation = () => {
  if (funnyMessageInterval) {
    clearInterval(funnyMessageInterval)
    funnyMessageInterval = null
  }
  funnyMessage.value = ''
}

// Map server regions to routing values
const regionToRouting = {
  'na1': 'americas',
  'br1': 'americas',
  'la1': 'americas',
  'la2': 'americas',
  'euw1': 'europe',
  'eun1': 'europe',
  'tr1': 'europe',
  'ru': 'europe',
  'kr': 'asia',
  'jp1': 'asia',
  'oc1': 'sea',
  'ph2': 'sea',
  'sg2': 'sea',
  'th2': 'sea',
  'tw2': 'sea',
  'vn2': 'sea'
}

// Load search history from localStorage
const loadSearchHistory = () => {
  try {
    const stored = localStorage.getItem(HISTORY_STORAGE_KEY)
    if (stored) {
      searchHistory.value = JSON.parse(stored)
    }
  } catch (e) {
    console.error('Failed to load search history:', e)
  }
}

// Save search history to localStorage
const saveSearchHistory = () => {
  try {
    localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(searchHistory.value))
  } catch (e) {
    console.error('Failed to save search history:', e)
  }
}

// Add a search to history
const addToHistory = (search) => {
  // Remove duplicate if it exists
  searchHistory.value = searchHistory.value.filter(
    item => !(item.summonerName === search.summonerName &&
              item.tagLine === search.tagLine &&
              item.region === search.region)
  )

  // Add to beginning of array
  searchHistory.value.unshift({
    summonerName: search.summonerName,
    tagLine: search.tagLine,
    region: search.region,
    rankedType: search.rankedType,
    timestamp: Date.now()
  })

  // Keep only MAX_HISTORY_ITEMS
  if (searchHistory.value.length > MAX_HISTORY_ITEMS) {
    searchHistory.value = searchHistory.value.slice(0, MAX_HISTORY_ITEMS)
  }

  saveSearchHistory()
}

// Load a search from history
const loadFromHistory = (historyItem) => {
  summonerName.value = historyItem.summonerName
  tagLine.value = historyItem.tagLine
  region.value = historyItem.region
  rankedType.value = historyItem.rankedType
  showHistory.value = false
}

// Clear search history
const clearHistory = () => {
  searchHistory.value = []
  saveSearchHistory()
  showHistory.value = false
}

const canSubmit = computed(() => {
  return summonerName.value.trim() && tagLine.value.trim()
})

const connectWebSocket = () => {
  return new Promise((resolve, reject) => {
    ws = new WebSocket("wss://v19yst44bk.execute-api.eu-west-3.amazonaws.com/production")

    ws.onopen = () => {
      console.log("WebSocket connected")
      // Send a message to start processing
      ws.send(JSON.stringify({
        action: "process",
        region: region.value,
        gamename: summonerName.value.trim(),
        gametag: tagLine.value.trim(),
        ranked_type: rankedType.value
      }))
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'progress') {
        progress.value = data.progress
        progressMessage.value = data.message
      } else if (data.type === 'complete') {
        progress.value = 100
        progressMessage.value = data.message
        ws.close()
        // Resolve with the returned data from the backend
        resolve({
          region: data.region,
          gamename: data.gamename,
          tag: data.tag,
          puuid: data.puuid
        })
      } else if (data.type === 'error') {
        reject(new Error(data.message || 'An error occurred'))
      }
    }

    ws.onerror = (err) => {
      console.error("WebSocket error:", err)
      reject(new Error('WebSocket connection error'))
    }

    ws.onclose = () => {
      console.log("WebSocket disconnected")
    }
  })
}

const handleSubmit = async () => {
  if (!canSubmit.value || loading.value) return

  error.value = ''
  loading.value = true
  progress.value = 0
  progressMessage.value = 'Connecting...'

  // Start funny message rotation
  startFunnyMessageRotation()

  // Add to search history before submitting
  addToHistory({
    summonerName: summonerName.value.trim(),
    tagLine: tagLine.value.trim(),
    region: region.value,
    rankedType: rankedType.value
  })

  try {
    // Connect to WebSocket and wait for processing to complete
    const result = await connectWebSocket()

    // Once complete, emit the submit event with the returned data from the backend
    emit('submit', {
      summonerName: result.gamename,
      tagLine: result.tag,
      region: result.region,
      routingRegion: regionToRouting[result.region],
      rankedType: rankedType.value,
      puuid: result.puuid
    })
  } catch (err) {
    error.value = err.message || 'Failed to process matches. Please try again.'
    loading.value = false
    progress.value = 0
    progressMessage.value = ''
    stopFunnyMessageRotation()

    // Clean up WebSocket connection if it exists
    if (ws) {
      ws.close()
      ws = null
    }
  }
}

const setLoading = (value) => {
  loading.value = value
  if (!value) {
    stopFunnyMessageRotation()
  }
}

const setError = (message) => {
  error.value = message
  loading.value = false
  progress.value = 0
  progressMessage.value = ''
  stopFunnyMessageRotation()
}

// Load search history on mount
onMounted(() => {
  loadSearchHistory()
})

// Clean up WebSocket on component unmount
onUnmounted(() => {
  if (ws) {
    ws.close()
    ws = null
  }
  stopFunnyMessageRotation()
})

defineExpose({
  setLoading,
  setError
})
</script>

<style scoped>
.summoner-input-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  background: radial-gradient(circle at center, rgba(200, 155, 60, 0.1) 0%, transparent 70%);
}

.input-content {
  max-width: 600px;
  width: 100%;
  text-align: center;
}

.logo-section {
  margin-bottom: 3rem;
}

.title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 300;
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
  color: var(--lol-gold-light);
}

.subtitle {
  font-size: clamp(2.5rem, 7vw, 5rem);
  font-weight: 900;
  letter-spacing: 0.05em;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-gold-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.input-form {
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.9), rgba(10, 20, 40, 0.8));
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 25px;
  padding: 3rem 2.5rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.form-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--lol-gold);
  margin-bottom: 0.5rem;
}

.form-description {
  color: var(--lol-gold-light);
  margin-bottom: 2rem;
  opacity: 0.9;
}

.history-section {
  margin-bottom: 2rem;
  text-align: left;
}

.history-toggle {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(10, 20, 40, 0.6);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 12px;
  color: var(--lol-gold-light);
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-toggle:hover {
  border-color: var(--lol-gold);
  background: rgba(10, 20, 40, 0.8);
}

.history-count {
  background: rgba(200, 155, 60, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
}

.history-dropdown {
  margin-top: 0.5rem;
  background: rgba(10, 20, 40, 0.8);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 12px;
  overflow: hidden;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.history-items {
  max-height: 300px;
  overflow-y: auto;
}

.history-items::-webkit-scrollbar {
  width: 8px;
}

.history-items::-webkit-scrollbar-track {
  background: rgba(10, 20, 40, 0.4);
}

.history-items::-webkit-scrollbar-thumb {
  background: rgba(200, 155, 60, 0.4);
  border-radius: 4px;
}

.history-items::-webkit-scrollbar-thumb:hover {
  background: rgba(200, 155, 60, 0.6);
}

.history-item {
  width: 100%;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(200, 155, 60, 0.2);
  color: var(--lol-gold-light);
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.history-item:last-child {
  border-bottom: none;
}

.history-item:hover {
  background: rgba(200, 155, 60, 0.1);
}

.history-item-main {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.history-name {
  font-weight: 600;
  color: var(--lol-gold);
}

.history-region {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  background: rgba(200, 155, 60, 0.2);
  border-radius: 6px;
  text-transform: uppercase;
}

.history-type {
  font-size: 0.8rem;
  opacity: 0.7;
}

.clear-history-btn {
  width: 100%;
  padding: 0.75rem;
  background: rgba(209, 54, 57, 0.1);
  border: none;
  border-top: 1px solid rgba(200, 155, 60, 0.2);
  color: var(--lol-red);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-history-btn:hover {
  background: rgba(209, 54, 57, 0.2);
}

.input-group {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.input-wrapper,
.region-select {
  text-align: left;
}

label {
  display: block;
  color: var(--lol-gold-light);
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

input,
select {
  width: 100%;
  padding: 1rem;
  background: rgba(10, 20, 40, 0.6);
  border: 2px solid rgba(200, 155, 60, 0.3);
  border-radius: 12px;
  color: var(--lol-gold-light);
  font-size: 1rem;
  font-family: 'Montserrat', sans-serif;
  transition: all 0.3s ease;
}

input:focus,
select:focus {
  outline: none;
  border-color: var(--lol-gold);
  box-shadow: 0 0 0 3px rgba(200, 155, 60, 0.1);
}

input::placeholder {
  color: rgba(240, 230, 210, 0.4);
}

input:disabled,
select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.region-select,
.ranked-type-select {
  margin-bottom: 2rem;
}

.submit-button {
  width: 100%;
  padding: 1.2rem 2rem;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-gold-light));
  color: var(--lol-dark);
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(200, 155, 60, 0.3);
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(200, 155, 60, 0.5);
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 3px solid var(--lol-dark);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.progress-container {
  margin-top: 1.5rem;
}

.funny-message {
  margin-bottom: 1rem;
  color: var(--lol-gold);
  font-size: 1rem;
  font-weight: 600;
  font-style: italic;
  text-align: center;
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

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(10, 20, 40, 0.6);
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(200, 155, 60, 0.3);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--lol-gold), var(--lol-gold-light));
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(200, 155, 60, 0.5);
}

.progress-text {
  margin-top: 0.5rem;
  color: var(--lol-gold-light);
  font-size: 0.9rem;
  font-weight: 600;
  text-align: center;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(209, 54, 57, 0.1);
  border: 1px solid var(--lol-red);
  border-radius: 10px;
  color: var(--lol-red);
  font-weight: 600;
}

.privacy-note {
  margin-top: 1.5rem;
  font-size: 0.85rem;
  color: rgba(240, 230, 210, 0.6);
  line-height: 1.5;
}

@media (max-width: 600px) {
  .input-group {
    grid-template-columns: 1fr;
  }

  .input-form {
    padding: 2rem 1.5rem;
  }
}
</style>
