<template>
  <section class="section chart-section">
    <div class="content-wrapper">
      <div class="tag">Activity Timeline</div>
      <h2 class="section-title">Your Journey Through the Year</h2>
      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
      <p class="chart-description">
        Your most active month: <span class="highlight">{{ mostActiveMonth }}</span> with {{ mostActiveGames }} games
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const parseMonthYear = (key) => {
      if (!key) return null

      // MM/YY or MM/YYYY
      const slashMatch = key.match(/^(\d{1,2})\/(\d{2,4})$/)
      if (slashMatch) {
      const month = parseInt(slashMatch[1], 10) - 1
      let year = parseInt(slashMatch[2], 10)
      if (slashMatch[2].length === 2) year += 2000
      return { year, month }
      }

      // ISO or JS-parsable date
      const d = new Date(key)
      if (!isNaN(d)) return { year: d.getFullYear(), month: d.getMonth() }

      // Fallback for other formats like MM-YY, MM-YYYY, YYYY-MM
      const parts = key.split(/[-_]/)
      if (parts.length >= 2) {
      // YYYY-MM or YYYY/MM
      if (parts[0].length === 4) {
        return { year: parseInt(parts[0], 10), month: parseInt(parts[1], 10) - 1 }
      }
      // MM-YY or MM-YYYY
      let month = parseInt(parts[0], 10) - 1
      let year = parseInt(parts[1], 10)
      if (parts[1].length === 2) year += 2000
      return { year, month }
      }

      return null
    }

const chartCanvas = ref(null)
let chartInstance = null

const mostActiveMonth = computed(() => {
  const entries = Object.entries(props.data).filter(([_, games]) => games > 0)
  if (entries.length === 0) return 'N/A'

  const maxEntry = entries.reduce((max, entry) => entry[1] > max[1] ? entry : max)
  const date = parseMonthYear(maxEntry[0])
  if (!date) return 'N/A'
  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  return `${monthNames[date.month]} ${date.year}`
})

const mostActiveGames = computed(() => {
  const values = Object.values(props.data)
  return values.length > 0 ? Math.max(...values) : 0
})

onMounted(() => {
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext('2d')

    

    // Determine year from the first key (supports "MM/YY" like "05/25")
    const firstKey = Object.keys(props.data)[0]
    const parsedFirst = parseMonthYear(firstKey)
    const year = parsedFirst ? parsedFirst.year : new Date().getFullYear()

    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    const labels = monthNames.map(month => `${month} ${year}`)

    const values = monthNames.map((_, index) => {
      for (const [key, value] of Object.entries(props.data)) {
      const p = parseMonthYear(key)
      if (p && p.year === year && p.month === index) {
        return value
      }
      }
      return 0
    })

    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Games Played',
          data: values,
          backgroundColor: (context) => {
            const ctx = context.chart.ctx
            const gradient = ctx.createLinearGradient(0, 0, 0, 400)
            gradient.addColorStop(0, 'rgba(200, 155, 60, 0.8)')
            gradient.addColorStop(1, 'rgba(3, 151, 171, 0.3)')
            return gradient
          },
          borderColor: 'rgba(200, 155, 60, 1)',
          borderWidth: 2,
          borderRadius: 10,
          borderSkipped: false,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 2,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(10, 20, 40, 0.95)',
            titleColor: '#f0e6d2',
            bodyColor: '#c89b3c',
            borderColor: '#c89b3c',
            borderWidth: 2,
            padding: 12,
            displayColors: false,
            callbacks: {
              label: function(context) {
                return `${context.parsed.y} games played`
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              color: '#f0e6d2',
              font: {
                size: 12,
                weight: '600'
              },
              stepSize: 1,
              precision: 0
            },
            grid: {
              color: 'rgba(200, 155, 60, 0.1)',
              drawBorder: false
            }
          },
          x: {
            ticks: {
              color: '#c89b3c',
              font: {
                size: 10,
                weight: '600'
              },
              maxRotation: 45,
              minRotation: 45,
              autoSkip: false
            },
            grid: {
              display: false,
              drawBorder: false
            }
          }
        },
        animation: {
          duration: 2000,
          easing: 'easeInOutQuart',
          delay: (context) => {
            return context.dataIndex * 100
          }
        }
      }
    })
  }
})
</script>

<style scoped>
.chart-section {
  background: radial-gradient(circle at 50% 30%, rgba(200, 155, 60, 0.03) 0%, transparent 50%);
}

.content-wrapper {
  max-width: 1200px;
  width: 100%;
}

.tag {
  display: inline-block;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-blue));
  color: white;
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
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 900;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, var(--lol-gold), var(--lol-blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.chart-container {
  background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(10, 20, 40, 0.6));
  border: 2px solid rgba(200, 155, 60, 0.2);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
}

.chart-description {
  text-align: center;
  font-size: 1.2rem;
  color: var(--lol-gold-light);
}

.highlight {
  color: var(--lol-gold);
  font-weight: 700;
}

@media (max-width: 768px) {
  .chart-container {
    padding: 1rem;
  }
}
</style>
