# League of Legends Wrapped 2025

A beautiful, interactive year-in-review experience for League of Legends players. Built with Vue 3, GSAP animations, Chart.js visualizations, and Riot DataDragon assets.

## Features

- **Spotify Wrapped-style Experience**: Smooth scrolling sections revealing player statistics
- **Beautiful Animations**: GSAP-powered scroll triggers and transitions
- **Interactive Visualizations**: Chart.js graphs showing play patterns over time
- **Riot DataDragon Integration**: Official champion images and assets
- **Particle Effects**: Dynamic background particles for visual appeal
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **League of Legends Theme**: Authentic colors, fonts, and styling

## Tech Stack

- **Vue 3** - Progressive JavaScript framework with Composition API
- **Vite** - Fast build tool and dev server
- **GSAP** - Professional-grade animation library with ScrollTrigger
- **Chart.js** - Flexible charting library for data visualization
- **Particles.vue3** - Particle system for background effects
- **Riot DataDragon** - Official LoL champion assets

## Installation

1. **Install dependencies**:
```bash
npm install
```

2. **Start development server**:
```bash
npm run dev
```

The app will open at `http://localhost:3000`

3. **Build for production**:
```bash
npm run build
```

4. **Preview production build**:
```bash
npm run preview
```

## Project Structure

```
lol-wrapped/
├── src/
│   ├── components/
│   │   ├── GameDurationSection.vue    # Time played stats
│   │   ├── ChampionsSection.vue       # Top champions & roles
│   │   ├── PlayTimeChart.vue          # Monthly activity chart
│   │   ├── DeathsSection.vue          # Death statistics
│   │   ├── KillsSection.vue           # Kills & multikills
│   │   ├── MetricsSection.vue         # Performance metrics
│   │   └── ObjectivesSection.vue      # Objectives & vision
│   ├── App.vue                         # Main component
│   ├── main.js                         # App entry point
│   └── style.css                       # Global styles
├── index.html
├── vite.config.js
└── package.json
```

## Connecting to Your Backend

The app is already configured to connect to your AWS API Gateway endpoint. The API integration is ready to use!

### How It Works

1. User enters their **Summoner Name** and **Tag** (e.g., "Reive" and "EUW")
2. App sends a POST request to your backend:
   ```
   POST https://xe653skfef.execute-api.eu-west-3.amazonaws.com/getWrapped
   {
     "name": "Reive",
     "gametag": "EUW"
   }
   ```
3. Backend returns player stats JSON
4. App displays the Wrapped experience with animations

### Configuration

The API endpoint is configured in `.env`:
```env
VITE_API_URL=https://xe653skfef.execute-api.eu-west-3.amazonaws.com
```

To change the endpoint, update this file and restart the dev server.

### Expected Data Format

Your backend should return JSON matching this structure:

```json
{
  "game_duration": {
    "gameplayed": 129,
    "timespend_hh_mm_ss": "02 day(s) 16 hour(s) 45 minute(s)",
    "longest_game": "00 day(s) 00 hour(s) 44 minute(s)",
    "victory": { "true": 68, "false": 61 },
    "winrate": 0.53,
    "amount_played_year": {
      "January 2025": 26,
      "November 2024": 23
    },
    "tag_comment1": "League Addict",
    "comment1": "Your witty comment here"
  },
  "role_champs_played": {
    "most_played_champ": {
      "Yasuo": 18,
      "Zed": 14
    },
    "most_played_role": {
      "MIDDLE": 61,
      "BOTTOM": 44
    }
  },
  "deaths_stats": { ... },
  "kills_assists_stats": { ... },
  "metrics": { ... },
  "objectives": { ... }
}
```

See the sample data in `App.vue` for the complete structure.

## DataDragon Assets

The app uses Riot's DataDragon CDN for champion images:

```
https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{championName}.png
```

Update the version in `src/components/ChampionsSection.vue` (line 67) to match the latest LoL patch:

```javascript
const DDRAGON_VERSION = '14.1.1' // Update to latest version
```

Find the latest version at: https://ddragon.leagueoflegends.com/api/versions.json

## Customization

### Colors

Edit color variables in `src/style.css`:

```css
:root {
  --lol-gold: #c89b3c;
  --lol-blue: #0397ab;
  --lol-dark: #010a13;
  /* ... */
}
```

### Fonts

The app uses Montserrat from Google Fonts. Change it in `index.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@...&display=swap" rel="stylesheet">
```

Then update in `src/style.css`:

```css
font-family: 'YourFont', sans-serif;
```

### Animations

Adjust GSAP animations in component `onMounted` hooks or in `src/App.vue`:

```javascript
gsap.from('.element', {
  opacity: 0,
  y: 50,
  duration: 1,
  ease: 'power3.out'
})
```

### Particle Effects

Modify particle configuration in `src/App.vue` under `particlesOptions`.

## Performance Tips

- The app uses lazy-loaded components via Vue's async components if needed
- Images from DataDragon are cached by the browser
- Chart.js animations are optimized for 60fps
- GSAP uses GPU acceleration for smooth scrolling

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

This project uses Riot Games' assets under their Legal Jibber Jabber policy for community projects.

## Credits

- Built with Vue.js, GSAP, Chart.js, and Particles.vue3
- Champion data and assets from Riot Games DataDragon
- Inspired by Spotify Wrapped

## Support

For issues or questions:
1. Check the browser console for errors
2. Verify your data format matches the expected structure
3. Ensure DataDragon assets are accessible
4. Check that all dependencies are installed correctly

---

**Have fun showcasing your League of Legends journey!** ⚔️✨
