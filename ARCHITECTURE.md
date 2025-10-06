# League of Legends Year-End Recap - Architecture

## Overview
AI-powered League of Legends analytics platform with three core features:
1. **Interactive Year-End Recap** - Card-based stat reveals with themed artwork
2. **Player Progression Tracking** - Visualize improvement over time across multiple dimensions
3. **Interactive AI Coaching** - Personalized insights and actionable recommendations

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Frontend (React)                                  │
│  ┌─────────────────────┐ ┌──────────────────┐ ┌──────────────────────────┐ │
│  │  Year-End Recap     │ │  Progression     │ │  AI Coaching             │ │
│  │  - Card flip UI     │ │  - Time series   │ │  - Chat interface        │ │
│  │  - Themed artwork   │ │  - Skill radar   │ │  - Recommendations       │ │
│  │  - Social sharing   │ │  - Trend charts  │ │  - Goal tracking         │ │
│  └─────────────────────┘ └──────────────────┘ └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Layer (FastAPI/Flask)                │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Data Ingestion  │  │  Stat Generator  │                │
│  │  - Riot API      │  │  - Card Builder  │                │
│  │  - Match History │  │  - Theme Mapping │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Analysis & AI Layer (AWS)                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Data Processing Pipeline                              │ │
│  │  - Match aggregation & statistics                      │ │
│  │  - Trend analysis (improvement over time)              │ │
│  │  - Social comparison (friends/similar players)         │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  GenAI Services (AWS Bedrock/SageMaker)                │ │
│  │  - Personalized insights generation                    │ │
│  │  - Narrative creation for achievements                 │ │
│  │  - Surprising pattern discovery                        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Storage Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Match Data  │  │  Player Stats│  │  Generated Cards │  │
│  │  (DynamoDB)  │  │  (DynamoDB)  │  │  (S3/Cache)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Stat Card System

### Card Types & Themes

Each stat is categorized and mapped to thematic artwork:

1. **Champion Mastery** - Champion artwork + key stats
2. **Funny/Death Stats** - Teemo demon theme
3. **Survival Stats** - Warmog item theme
4. **Movement Stats** - Ghost summoner spell theme
5. **Map Geography Stats** - Rift golem/terrain theme
6. **Performance Milestones** - Trophy/achievement theme
7. **Social/Comparison** - Team/friends theme
8. **Improvement/Growth** - Progress bar/chart theme

### Card Structure
```json
{
  "id": "unique_card_id",
  "category": "champion_mastery|funny|survival|movement|geography|milestone|social|growth",
  "title": "Your Most Played Champion",
  "value": "127 games on Ahri",
  "subtitle": "That's 42 hours of charm spam!",
  "theme": {
    "artwork": "ahri_splash_art_url",
    "background_color": "#c77dff",
    "accent_color": "#9d4edd"
  },
  "metadata": {
    "shareable": true,
    "rarity": "common|rare|epic|legendary"
  }
}
```

## Tech Stack

### Frontend
- **React** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for card flip animations
- **React Query** for data fetching
- **Vite** for build tooling

### Backend
- **FastAPI** (Python) - API server
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM (if using relational DB)
- **Celery** - Background job processing

### AWS Services
- **AWS Bedrock** - GenAI for insights (Claude, etc.)
- **DynamoDB** - Match history & player data storage
- **S3** - Static assets, generated card images
- **Lambda** - Serverless data processing
- **API Gateway** - API management
- **CloudFront** - CDN for frontend

### Data Processing
- **Pandas** - Data manipulation
- **NumPy** - Statistical calculations
- **Scikit-learn** - Pattern detection (optional)

## Project Structure

```
hackathon-rift/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── players.py
│   │   │   ├── matches.py
│   │   │   ├── stats.py
│   │   │   └── cards.py
│   │   └── main.py
│   ├── services/
│   │   ├── riot_api.py
│   │   ├── data_processor.py
│   │   ├── stat_generator.py
│   │   ├── card_builder.py
│   │   └── aws_genai.py
│   ├── models/
│   │   ├── match.py
│   │   ├── player.py
│   │   ├── stat_card.py
│   │   └── schemas.py
│   ├── utils/
│   │   ├── card_themes.py
│   │   └── helpers.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StatCard.tsx
│   │   │   ├── CardDeck.tsx
│   │   │   ├── RerollButton.tsx
│   │   │   └── ShareButton.tsx
│   │   ├── hooks/
│   │   │   └── usePlayerStats.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── stats.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│   └── sample_matches.json
│
├── scripts/
│   ├── seed_data.py
│   └── test_riot_api.py
│
└── README.md
```

## Data Flow

### 1. Data Ingestion
```
Riot API → Match History → Raw JSON → DynamoDB
```

### 2. Stat Generation
```
Raw Matches → Aggregation → Statistical Analysis → Stat Cards Pool
```

### 3. AI Enhancement
```
Stat Cards → AWS Bedrock → Personalized Insights → Enhanced Cards
```

### 4. User Interaction
```
Player Request → API → Select 3 Cards → Frontend Display
Reroll Action → Fetch Different 3 Cards → Flip Animation
```

## Key Features to Implement

### Phase 1: Foundation
- [ ] Backend API structure
- [ ] Data models (Match, Player, StatCard)
- [ ] Riot API integration
- [ ] Basic stat calculation

### Phase 2: Stat Generation
- [ ] Card categorization system
- [ ] Theme mapping logic
- [ ] Stat card builder
- [ ] Card pool management (primary/secondary sets)

### Phase 3: Frontend
- [ ] Card flip animation component
- [ ] 3-card display with reroll
- [ ] Theme-based artwork rendering
- [ ] Responsive design

### Phase 4: AI Integration
- [ ] AWS Bedrock integration
- [ ] Prompt engineering for insights
- [ ] Narrative generation for cards
- [ ] Pattern discovery

### Phase 5: Social Features
- [ ] Share card functionality
- [ ] Friend comparison
- [ ] Social media templates
- [ ] Leaderboards

## API Endpoints (Proposed)

```
GET  /api/players/{puuid}                    # Get player profile
GET  /api/players/{puuid}/matches            # Get match history
POST /api/players/{puuid}/generate-recap     # Generate year-end recap
GET  /api/players/{puuid}/cards/primary      # Get 3 primary stat cards
GET  /api/players/{puuid}/cards/secondary    # Get 3 secondary stat cards (reroll)
GET  /api/players/{puuid}/insights           # Get AI-generated insights
POST /api/cards/{card_id}/share              # Generate shareable card image
```

## Next Steps

1. Set up backend API framework
2. Define data models and card schema
3. Create card theme configuration
4. Build frontend card component
5. Integrate with Riot API
6. Implement stat calculation engine
7. Connect AWS GenAI services
