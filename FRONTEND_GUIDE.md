# Frontend Development Guide

## Where to Add New Features

### Current Structure
```
frontend/src/
├── components/          # UI Components
│   ├── StatCard.tsx    ✅ DONE - Individual stat card
│   └── CardDeck.tsx    ✅ DONE - Year-end recap view
│
├── services/
│   └── api.ts          ✅ DONE - API client
│
├── types/
│   └── stats.ts        ✅ DONE - TypeScript types
│
├── data/
│   └── mockCards.ts    ✅ DONE - Sample data
│
├── App.tsx             ✅ DONE - Main app (currently shows cards only)
└── main.tsx            ✅ DONE - Entry point
```

---

## How to Add the Other Features

### 1. **Progression Tracking** 📈

Create these new components:

#### A. Time Series Chart Component
**File:** `src/components/ProgressionChart.tsx`
```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { ProgressionTimeSeries } from '../types/stats';

// Shows KDA, vision score, CS/min over time
// Use recharts for visualization
```

#### B. Skill Radar Component
**File:** `src/components/SkillRadar.tsx`
```tsx
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';
import { SkillRadar } from '../types/stats';

// 6-point radar: combat, vision, farming, objectives, positioning, teamfight
```

#### C. Champion Progression Component
**File:** `src/components/ChampionProgression.tsx`
```tsx
// List of champions with:
// - Win rate trend
// - Games played
// - First 10 games vs recent 10 games comparison
```

#### D. Main Progression Page
**File:** `src/pages/ProgressionPage.tsx`
```tsx
import ProgressionChart from '../components/ProgressionChart';
import SkillRadar from '../components/SkillRadar';
import ChampionProgression from '../components/ChampionProgression';

export default function ProgressionPage() {
  // Fetch progression data from API
  // Display all charts and metrics
}
```

---

### 2. **AI Coaching** 🤖

Create these components:

#### A. Chat Interface
**File:** `src/components/CoachingChat.tsx`
```tsx
import { ChatMessage } from '../types/stats';

// ChatGPT-style interface
// - Message list (user + AI messages)
// - Input field
// - Send button
// - Display insights and recommendations inline
```

#### B. Insight Card Component
**File:** `src/components/InsightCard.tsx`
```tsx
import { CoachingInsight } from '../types/stats';

// Display a single insight with:
// - Priority badge (critical/high/medium/low)
// - Type icon (strength/weakness/improvement)
// - Evidence list
// - Recommended actions
```

#### C. Recommendation Card Component
**File:** `src/components/RecommendationCard.tsx`
```tsx
import { Recommendation } from '../types/stats';

// Display recommendation with:
// - Category badge
// - Difficulty & impact indicators
// - Progress bar
// - Steps checklist
// - Mark as complete button
```

#### D. Goal Tracker Component
**File:** `src/components/GoalTracker.tsx`
```tsx
import { Goal } from '../types/stats';

// Display active goals with:
// - Progress percentage
// - AI checkpoints
// - Target date
// - Related insights
```

#### E. Main Coaching Page
**File:** `src/pages/CoachingPage.tsx`
```tsx
import CoachingChat from '../components/CoachingChat';
import InsightCard from '../components/InsightCard';
import RecommendationCard from '../components/RecommendationCard';
import GoalTracker from '../components/GoalTracker';

export default function CoachingPage() {
  // Layout:
  // - Left: Chat interface
  // - Right: Active insights, recommendations, goals
}
```

---

### 3. **Navigation & Routing**

#### Update App.tsx to include routing:
**File:** `src/App.tsx`
```tsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import RecapPage from './pages/RecapPage';
import ProgressionPage from './pages/ProgressionPage';
import CoachingPage from './pages/CoachingPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gradient-to-br from-lol-dark via-lol-dark-light to-lol-dark-lighter">
        {/* Navigation Bar */}
        <nav className="bg-lol-dark-lighter border-b border-lol-gold/20">
          <div className="max-w-7xl mx-auto px-4 py-4 flex gap-6">
            <Link to="/" className="text-lol-gold hover:text-lol-gold-light">
              Year-End Recap
            </Link>
            <Link to="/progression" className="text-white hover:text-lol-gold">
              Progression
            </Link>
            <Link to="/coaching" className="text-white hover:text-lol-gold">
              AI Coaching
            </Link>
          </div>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<RecapPage />} />
          <Route path="/progression" element={<ProgressionPage />} />
          <Route path="/coaching" element={<CoachingPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
```

#### Move current card view to a page:
**File:** `src/pages/RecapPage.tsx`
```tsx
import CardDeck from '../components/CardDeck';
import { mockPrimaryDeck, mockSecondaryDeck } from '../data/mockCards';

export default function RecapPage() {
  // Current CardDeck component goes here
  return <CardDeck primaryDeck={mockPrimaryDeck} secondaryDeck={mockSecondaryDeck} />;
}
```

---

## Recommended File Structure (After Adding Features)

```
frontend/src/
├── components/
│   ├── cards/                  # Year-end recap
│   │   ├── StatCard.tsx       ✅ DONE
│   │   └── CardDeck.tsx       ✅ DONE
│   │
│   ├── progression/            # Progression tracking
│   │   ├── ProgressionChart.tsx    ⬜ TODO
│   │   ├── SkillRadar.tsx          ⬜ TODO
│   │   ├── ChampionProgression.tsx ⬜ TODO
│   │   └── MetricSelector.tsx      ⬜ TODO (choose which metric to view)
│   │
│   ├── coaching/               # AI coaching
│   │   ├── CoachingChat.tsx        ⬜ TODO
│   │   ├── InsightCard.tsx         ⬜ TODO
│   │   ├── RecommendationCard.tsx  ⬜ TODO
│   │   ├── GoalTracker.tsx         ⬜ TODO
│   │   └── MessageBubble.tsx       ⬜ TODO
│   │
│   └── shared/                 # Shared components
│       ├── NavBar.tsx              ⬜ TODO
│       ├── LoadingSpinner.tsx      ⬜ TODO
│       └── ErrorMessage.tsx        ⬜ TODO
│
├── pages/
│   ├── RecapPage.tsx           ⬜ TODO (move current App content here)
│   ├── ProgressionPage.tsx     ⬜ TODO
│   └── CoachingPage.tsx        ⬜ TODO
│
├── hooks/                      # Custom React hooks
│   ├── usePlayerStats.ts       ⬜ TODO
│   ├── useProgression.ts       ⬜ TODO
│   └── useCoaching.ts          ⬜ TODO
│
├── services/
│   └── api.ts                  ✅ DONE
│
├── types/
│   └── stats.ts                ✅ DONE
│
├── data/                       # Mock data (for development)
│   ├── mockCards.ts            ✅ DONE
│   ├── mockProgression.ts      ⬜ TODO
│   └── mockCoaching.ts         ⬜ TODO
│
├── utils/                      # Helper functions
│   ├── formatters.ts           ⬜ TODO (format numbers, dates, etc.)
│   └── colors.ts               ⬜ TODO (color utilities)
│
├── App.tsx                     ✅ DONE (needs routing update)
└── main.tsx                    ✅ DONE
```

---

## Quick Start: Add a New Feature (Example)

### Let's add the Progression page step by step:

1. **Create mock data:**
```bash
# File: src/data/mockProgression.ts
```

2. **Create the chart component:**
```bash
# File: src/components/progression/ProgressionChart.tsx
```

3. **Create the radar component:**
```bash
# File: src/components/progression/SkillRadar.tsx
```

4. **Create the page:**
```bash
# File: src/pages/ProgressionPage.tsx
```

5. **Add routing in App.tsx**

6. **Test with mock data**

7. **Connect to real API when backend is ready**

---

## Mock Data Examples

### For Progression (create `src/data/mockProgression.ts`):
```typescript
export const mockProgressionData = {
  metrics: [
    {
      metric: 'kda',
      data_points: [
        { timestamp: '2024-01', value: 2.5, match_count: 10 },
        { timestamp: '2024-02', value: 2.8, match_count: 15 },
        // ...
      ],
      trend: 'improving',
      change_percentage: 12.0
    }
  ],
  current_skill_radar: {
    combat: 75,
    vision: 82,
    farming: 68,
    objectives: 71,
    positioning: 79,
    teamfight: 85
  }
};
```

### For Coaching (create `src/data/mockCoaching.ts`):
```typescript
export const mockInsights = [
  {
    id: 'insight_1',
    type: 'improvement',
    priority: 'high',
    title: 'Your vision score improved by 35%',
    description: '...',
    evidence: ['Vision: 28 → 38', 'Wards: 12 → 16'],
    recommended_actions: ['Keep buying control wards early'],
    confidence_score: 0.92
  }
];
```

---

## Integration with Backend

When backend APIs are ready:

1. **Remove mock data imports**
2. **Use React Query hooks:**

```tsx
// In ProgressionPage.tsx
import { useQuery } from '@tanstack/react-query';
import { progressionApi } from '../services/api';

function ProgressionPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['progression', puuid],
    queryFn: () => progressionApi.getProgression(puuid)
  });

  if (isLoading) return <LoadingSpinner />;

  return <ProgressionChart data={data.metrics} />;
}
```

---

## Design Tips

### Color Scheme (Already in tailwind.config.js)
- **Gold:** `bg-lol-gold` - Highlights, CTAs
- **Blue:** `bg-lol-blue` - Links, secondary actions
- **Dark:** `bg-lol-dark` - Backgrounds

### Component Patterns
- Use Framer Motion for animations
- Use Lucide React for icons
- Keep components small and focused
- Use TypeScript strictly

### Responsive Design
- Mobile-first approach
- Use Tailwind's responsive classes: `md:`, `lg:`
- Test on different screen sizes

---

## Next Steps

1. **Choose which feature to build first** (Progression or Coaching)
2. **Create the mock data file**
3. **Build components one by one**
4. **Add routing**
5. **Test with mock data**
6. **Connect to backend APIs when ready**

Would you like me to scaffold any of these features for you?
