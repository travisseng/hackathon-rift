<template>
  <section class="section champions-section">
    <div class="content-wrapper">
      <div class="tag">Champion Pool</div>
      <h2 class="section-title">Your Main Champions</h2>

      <div class="champions-grid">
        <div
          v-for="(games, champion, index) in data.most_played_champ"
          :key="champion"
          class="champion-card"
          :class="{ 'rank-1': index === 0, 'rank-2': index === 1, 'rank-3': index === 2 }"
        >
          <div class="rank-badge">{{ getRankLabel(index) }}</div>
          <div class="champion-portrait">
            <img
              :src="getChampionImage(champion)"
              :alt="champion"
              @error="handleImageError"
            />
            <div class="champion-shine"></div>
          </div>
          <h3 class="champion-name">{{ formatChampionName(champion) }}</h3>
          <div class="champion-games">{{ games }} games</div>
        </div>
      </div>

      <div class="roles-section">
        <h3 class="roles-title">Preferred Roles</h3>
        <div class="roles-grid">
          <div
            v-for="(games, role) in data.most_played_role"
            :key="role"
            class="role-card"
          >
            <div class="role-icon"><img :src="getRoleIcon(role)" alt="Role Icon" /></div>
            <div class="role-name">{{ formatRole(role) }}</div>
            <div class="role-bar">
              <div class="role-fill" :style="{ width: getRolePercentage(role, games) + '%' }"></div>
            </div>
            <div class="role-games">{{ games }} games</div>
          </div>
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

const DDRAGON_VERSION = '15.22.1' // Update this to latest version

const getChampionImage = (championName) => {
  // Clean champion name (remove special characters, handle special cases)
  const cleanName = championName
    .replace(/[^a-zA-Z]/g, '')

  return `https://ddragon.leagueoflegends.com/cdn/${DDRAGON_VERSION}/img/champion/${cleanName}.png`
}

const handleImageError = (event) => {
  // Fallback to a placeholder if image fails to load
  event.target.src = 'https://ddragon.leagueoflegends.com/cdn/15.22.1/img/profileicon/29.png'
}

const formatChampionName = (name) => {
  // Add space before capital letters for champions like "LeeSin"
  return name.replace(/([A-Z])/g, ' $1').trim()
}

const getRankLabel = (index) => {
  const labels = ['#1', '#2', '#3']
  return labels[index] || ''
}

const getRoleIcon = (role) => {
  const icons = {
    'TOP': 'https://wiki.leagueoflegends.com/en-us/images/Top_icon.png',
    'JUNGLE': 'https://wiki.leagueoflegends.com/en-us/images/Jungle_icon.png',
    'MIDDLE': 'https://wiki.leagueoflegends.com/en-us/images/Middle_icon.png',
    'BOTTOM': 'https://wiki.leagueoflegends.com/en-us/images/Bottom_icon.png',
    'UTILITY': 'https://wiki.leagueoflegends.com/en-us/images/Support_icon.png'
  }
  return icons[role] || '❓'
}

const formatRole = (role) => {
  const names = {
    'TOP': 'Top Lane',
    'JUNGLE': 'Jungle',
    'MIDDLE': 'Mid Lane',
    'BOTTOM': 'ADC',
    'UTILITY': 'Support'
  }
  return names[role] || role
}

const totalRoleGames = computed(() => {
  return Object.values(props.data.most_played_role).reduce((sum, games) => sum + games, 0)
})

const getRolePercentage = (role, games) => {
  return (games / totalRoleGames.value) * 100
}
</script>

<style scoped>
.champions-section {
  background: radial-gradient(circle at 70% 50%, rgba(3, 151, 171, 0.05) 0%, transparent 50%);
}

.content-wrapper {
  max-width: 1200px;
  width: 100%;
}

.tag {
  display: inline-block;
  background: linear-gradient(135deg, var(--lol-blue), var(--lol-gold));
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 2rem;
  box-shadow: 0 5px 15px rgba(3, 151, 171, 0.3);
}

.section-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 900;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, var(--lol-blue), var(--lol-gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.champions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.champion-card {
  position: relative;
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(10, 20, 40, 0.6));
  border: 2px solid rgba(200, 155, 60, 0.2);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  overflow: hidden;
}

.champion-card:hover {
  transform: translateY(-10px) scale(1.02);
  border-color: var(--lol-gold);
  box-shadow: 0 15px 40px rgba(200, 155, 60, 0.4);
}

.champion-card.rank-1 {
  border-color: #FFD700;
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
}

.champion-card.rank-2 {
  border-color: #C0C0C0;
}

.champion-card.rank-3 {
  border-color: #CD7F32;
}

.rank-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: var(--lol-gold);
  color: var(--lol-dark);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 0.9rem;
  box-shadow: 0 5px 15px rgba(200, 155, 60, 0.5);
}

.champion-card.rank-1 .rank-badge {
  background: #FFD700;
}

.champion-card.rank-2 .rank-badge {
  background: #C0C0C0;
}

.champion-card.rank-3 .rank-badge {
  background: #CD7F32;
}

.champion-portrait {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--lol-gold);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}

.champion-portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.champion-card:hover .champion-portrait img {
  transform: scale(1.1);
}

.champion-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transform: rotate(45deg);
  transition: all 0.5s ease;
}

.champion-card:hover .champion-shine {
  left: 100%;
}

.champion-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--lol-gold);
  margin-bottom: 0.5rem;
}

.champion-games {
  color: var(--lol-gold-light);
  font-size: 1rem;
}

.roles-section {
  margin-top: 4rem;
}

.roles-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--lol-gold-light);
  margin-bottom: 2rem;
  text-align: center;
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.role-card {
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.6), rgba(10, 20, 40, 0.4));
  border: 2px solid rgba(200, 155, 60, 0.2);
  border-radius: 15px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.role-card:hover {
  border-color: var(--lol-blue);
  transform: translateY(-3px);
}

.role-icon {
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.role-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--lol-gold-light);
  margin-bottom: 1rem;
}

.role-bar {
  width: 100%;
  height: 8px;
  background: rgba(200, 155, 60, 0.2);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.role-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--lol-blue), var(--lol-gold));
  transition: width 1s ease;
  border-radius: 10px;
}

.role-games {
  color: var(--lol-gold);
  font-size: 0.9rem;
  font-weight: 600;
}

@media (max-width: 768px) {
  .champions-grid,
  .roles-grid {
    grid-template-columns: 1fr;
  }
}
</style>
