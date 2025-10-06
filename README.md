# League of Legends AI Analytics Platform

AI-powered analytics platform for League of Legends players featuring year-end recaps, progression tracking, and interactive coaching.

## Features

### 1. **Interactive Year-End Recap** 🎴
- TFT-style card reveal system with 3 primary + 3 secondary stat cards
- Themed artwork based on stat categories (champion mastery, survival, movement, etc.)
- Flip/reroll animations with rarity tiers (common, rare, epic, legendary)
- Social sharing capabilities

### 2. **Player Progression Tracking** 📈
- Time series visualization of key metrics (KDA, vision score, CS/min, etc.)
- Skill radar chart showing combat, vision, farming, objectives, positioning, and teamfight
- Champion-specific progression tracking
- Milestone achievements and improvement insights

### 3. **Interactive AI Coaching** 🤖
- Chat interface with AWS Bedrock-powered AI coach
- Personalized insights based on match data
- Actionable recommendations with progress tracking
- Goal setting and tracking with AI-generated checkpoints

## Tech Stack

### Backend
- **FastAPI** - Python web framework
- **Pydantic** - Data validation and serialization
- **AWS Bedrock** - Generative AI for insights and coaching
- **DynamoDB** - Match history and player data storage
- **S3** - Static assets and generated card images

### Frontend
- **React + TypeScript** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Query** - Data fetching and caching
- **Recharts** - Data visualization

## Project Structure

```
hackathon-rift/
├── backend/                # Python FastAPI backend
│   ├── api/
│   │   ├── routes/        # API endpoints
│   │   └── main.py        # FastAPI app entry point
│   ├── models/            # Pydantic data models
│   ├── services/          # Business logic
│   └── utils/             # Helpers and utilities
│
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   └── types/         # TypeScript types
│   └── package.json
│
└── data/                  # Sample data and datasets
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- AWS Account (for Bedrock and other services)
- Riot Games API Key ([Get one here](https://developer.riotgames.com/))

### Backend Setup

1. **Create and activate virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your settings
```

Required environment variables:
```env
RIOT_API_KEY=your_riot_api_key_here
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
DYNAMODB_TABLE_MATCHES=lol-matches
DYNAMODB_TABLE_PLAYERS=lol-players
S3_BUCKET_ASSETS=lol-assets
```

4. **Run the backend:**
```bash
cd backend
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Run the development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### AWS Setup

1. **Create DynamoDB Tables:**
```bash
# Create matches table
aws dynamodb create-table \
    --table-name lol-matches \
    --attribute-definitions AttributeName=match_id,AttributeType=S \
    --key-schema AttributeName=match_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

# Create players table
aws dynamodb create-table \
    --table-name lol-players \
    --attribute-definitions AttributeName=puuid,AttributeType=S \
    --key-schema AttributeName=puuid,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

2. **Create S3 Bucket:**
```bash
aws s3 mb s3://lol-assets
```

3. **Enable AWS Bedrock:**
- Navigate to AWS Bedrock console
- Request access to Claude models
- Wait for approval (usually instant)

## Development Workflow

### Running Both Services

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
uvicorn api.main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Testing the API

Visit `http://localhost:8000/docs` for the interactive API documentation (Swagger UI).

Example API calls:
```bash
# Get player primary cards
curl http://localhost:8000/api/cards/{puuid}/primary

# Generate insights
curl -X POST http://localhost:8000/api/coaching/{puuid}/insights/generate

# Get progression data
curl http://localhost:8000/api/progression/{puuid}
```

## Data Models

### StatCard
```python
{
  "id": "card_most_played_champion_ahri",
  "category": "champion_mastery",
  "title": "Your Most Played Champion",
  "value": "127 games on Ahri",
  "subtitle": "That's 42 hours of charm spam!",
  "theme": {
    "artwork_url": "https://...",
    "background_color": "#c77dff",
    "accent_color": "#9d4edd"
  },
  "rarity": "epic"
}
```

### Card Categories & Themes
- **Champion Mastery** - Champion splash art (purple theme)
- **Funny** - Teemo demon for death stats (red theme)
- **Survival** - Warmog's Armor (green theme)
- **Movement** - Ghost summoner spell (blue theme)
- **Geography** - Rift terrain/golem (gray theme)
- **Milestone** - Trophy/achievement (gold theme)
- **Social** - Team/friends comparison (purple theme)
- **Growth** - Progress charts (teal theme)

## API Endpoints

### Cards
- `GET /api/cards/{puuid}/primary` - Get primary 3 cards
- `GET /api/cards/{puuid}/secondary` - Get secondary 3 cards (reroll)
- `POST /api/cards/{puuid}/generate` - Generate all cards
- `POST /api/cards/{card_id}/share` - Create shareable image

### Progression
- `GET /api/progression/{puuid}` - Get complete progression data
- `GET /api/progression/{puuid}/metrics/{metric}` - Get time series
- `GET /api/progression/{puuid}/skill-radar` - Get skill radar data
- `POST /api/progression/{puuid}/analyze` - Trigger AI analysis

### Coaching
- `GET /api/coaching/{puuid}` - Get all coaching data
- `GET /api/coaching/{puuid}/insights` - Get AI insights
- `POST /api/coaching/{puuid}/insights/generate` - Generate new insights
- `POST /api/coaching/{puuid}/chat` - Chat with AI coach
- `POST /api/coaching/{puuid}/goals` - Create a goal

## Next Steps

### Phase 1: Data Ingestion
- [ ] Implement Riot API integration
- [ ] Build match history fetching
- [ ] Set up data storage in DynamoDB
- [ ] Create data processing pipeline

### Phase 2: Stat Generation
- [ ] Implement stat calculation engine
- [ ] Build card generation logic
- [ ] Create theme mapping system
- [ ] Generate card pools (primary/secondary)

### Phase 3: AI Integration
- [ ] Set up AWS Bedrock integration
- [ ] Design prompts for insight generation
- [ ] Implement coaching chat
- [ ] Build recommendation engine

### Phase 4: Frontend Polish
- [ ] Complete all UI components
- [ ] Add loading states and error handling
- [ ] Implement social sharing
- [ ] Optimize animations and performance

### Phase 5: Deployment
- [ ] Deploy backend to AWS Lambda
- [ ] Deploy frontend to S3 + CloudFront
- [ ] Set up CI/CD pipeline
- [ ] Configure monitoring and logging

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions, please create an issue in the repository.

---

**Built for the League of Legends AI Hackathon** 🎮
