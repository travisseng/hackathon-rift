/**
 * API utility for fetching League of Legends player stats
 *
 * Usage:
 * import { fetchPlayerStats } from './utils/api'
 *
 * const stats = await fetchPlayerStats('playerName', 'region')
 */

// Configure your backend API endpoint
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://xe653skfef.execute-api.eu-west-3.amazonaws.com'

/**
 * Fetch player statistics from your backend
 * @param {string} summonerName - Summoner name
 * @param {string} tagLine - Tag line (e.g., 'EUW')
 * @param {string} region - Region (optional, not currently used)
 * @returns {Promise<Object>} Player statistics
 */
export async function fetchPlayerStats(summonerName, tagLine, region = null) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/getWrapped`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: summonerName,
          gametag: tagLine
        })
      }
    )

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(errorText || `Failed to fetch stats: ${response.statusText}`)
    }

    const data = await response.json()

    return validateStatsData(data.content)
  } catch (error) {
    console.error('Error fetching player stats:', error)
    throw error
  }
}

/**
 * Fetch all games for a player with pagination
 * @param {string} gameName - Game name
 * @param {string} gameTag - Game tag (e.g., 'EUW')
 * @param {string} region - Region (e.g., 'euw1')
 * @param {string|null} puuid - Player UUID (optional)
 * @param {number} page - Page number (default: 1)
 * @param {number} pageSize - Number of games per page (default: 10)
 * @returns {Promise<Object>} Object containing { files, page, page_size, has_more, total_files }
 */
export async function fetchAllGames(gameName, gameTag, region = 'euw1', puuid = null, page = 1, pageSize = 10) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/getAllGames`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          region: region.toLowerCase(),
          gamename: gameName,
          gametag: gameTag,
          puuid: puuid,
          page: page,
          page_size: pageSize
        })
      }
    )

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(errorText || `Failed to fetch games: ${response.statusText}`)
    }

    const data = await response.json()

    // API returns { files: [...games], page, page_size, has_more, total_files }
    return {
      files: data.files || [],
      page: data.page || page,
      page_size: data.page_size || pageSize,
      has_more: data.has_more || false,
      total_files: data.total_files || 0
    }
  } catch (error) {
    console.error('Error fetching games:', error)
    throw error
  }
}

/**
 * Validate that the stats data has the required structure
 * @param {Object} data - Stats data from API
 * @returns {Object} Validated data
 * @throws {Error} If data is invalid
 */
function validateStatsData(data) {
  const requiredSections = [
    'overview',
    'time_stats',
    'combat_stats',
    'economy_stats',
    'damage_stats',
    'vision_stats',
    'objectives',
    'ping_stats',
    'most_played',
    'role_performance'
  ]

  for (const section of requiredSections) {
    if (!data[section]) {
      throw new Error(`Missing required section: ${section}`)
    }
  }

  return data
}

/**
 * Fetch the latest DataDragon version
 * @returns {Promise<string>} Latest version string (e.g., '14.1.1')
 */
export async function getLatestDataDragonVersion() {
  try {
    const response = await fetch('https://ddragon.leagueoflegends.com/api/versions.json')
    const versions = await response.json()
    return versions[0] // First item is the latest version
  } catch (error) {
    console.error('Error fetching DataDragon version:', error)
    return '15.22.1' // Fallback version
  }
}

/**
 * Get champion image URL from DataDragon
 * @param {string} championName - Champion name
 * @param {string} version - DataDragon version
 * @returns {string} Image URL
 */
export function getChampionImageUrl(championName, version = '15.22.1') {
  // Clean champion name (remove spaces, special characters)
  const cleanName = championName.replace(/[^a-zA-Z]/g, '')
  return `https://ddragon.leagueoflegends.com/cdn/${version}/img/champion/${cleanName}.png`
}

/**
 * Format time duration to readable string
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration (e.g., '02 day(s) 16 hour(s) 45 minute(s)')
 */
export function formatDuration(seconds) {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)

  return `${String(days).padStart(2, '0')} day(s) ${String(hours).padStart(2, '0')} hour(s) ${String(minutes).padStart(2, '0')} minute(s)`
}

/**
 * Calculate win rate
 * @param {number} wins - Number of wins
 * @param {number} losses - Number of losses
 * @returns {number} Win rate as decimal (0-1)
 */
export function calculateWinRate(wins, losses) {
  const total = wins + losses
  return total > 0 ? wins / total : 0
}

/**
 * Analyze a specific game
 * @param {string} gameName - Game name
 * @param {string} gameTag - Game tag (e.g., 'EUW')
 * @param {string} region - Region (e.g., 'euw1')
 * @param {string} gameId - Match ID
 * @returns {Promise<Object>} Game analysis data
 */
export async function analyzeGame(gameName, gameTag, region, gameId, puuid) {
  try {
    const response = await fetch(
      'https://eo5yg2jjm8.execute-api.eu-west-3.amazonaws.com/analyze',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          region: region.toLowerCase(),
          gamename: gameName,
          gametag: gameTag,
          gameid: gameId,
          puuid: puuid
        })
      }
    )

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(errorText || `Failed to analyze game: ${response.statusText}`)
    }

    const data = await response.json()

    // Check if the response contains an error field
    if (data.error) {
      throw new Error(data.error)
    }

    return data
  } catch (error) {
    console.error('Error analyzing game:', error)
    throw error
  }
}

/**
 * Fetch account data including rank information
 * @param {string} gameName - Game name
 * @param {string} gameTag - Game tag (e.g., 'EUW')
 * @returns {Promise<Object>} Account data including rank
 */
export async function fetchAccountData(gameName, gameTag) {
  try {
    const response = await fetch(
      `https://1xyj0oxw65.execute-api.eu-west-3.amazonaws.com/accountdata?gamename=${gameName}&gametag=${gameTag}`
    )

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(errorText || `Failed to fetch account data: ${response.statusText}`)
    }

    const data = await response.json()

    // Check if the response contains an error field
    if (data.error) {
      throw new Error(data.error)
    }

    return data
  } catch (error) {
    console.error('Error fetching account data:', error)
    throw error
  }
}

/**
 * Fetch monthly progress summary for a player
 * @param {string} gameName - Game name
 * @param {string} gameTag - Game tag (e.g., 'EUW')
 * @returns {Promise<Array>} Monthly progress data
 */
export async function fetchMonthlyProgress(gameName, gameTag) {
  try {
    const response = await fetch(
      `https://1xyj0oxw65.execute-api.eu-west-3.amazonaws.com/summary_year?gamename=${gameName}&gametag=${gameTag}`
    )

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(errorText || `Failed to fetch monthly progress: ${response.statusText}`)
    }

    const data = await response.json()

    // Check if the response contains an error field
    if (data.error) {
      throw new Error(data.error)
    }

    return data
  } catch (error) {
    console.error('Error fetching monthly progress:', error)
    throw error
  }
}

/**
 * Example usage in a Vue component:
 *
 * <script setup>
 * import { ref, onMounted } from 'vue'
 * import { fetchPlayerStats } from './utils/api'
 *
 * const statsData = ref(null)
 * const loading = ref(true)
 * const error = ref(null)
 *
 * onMounted(async () => {
 *   try {
 *     statsData.value = await fetchPlayerStats('YourSummonerName', 'na1')
 *   } catch (err) {
 *     error.value = err.message
 *   } finally {
 *     loading.value = false
 *   }
 * })
 * </script>
 */
