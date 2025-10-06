"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import players, matches, stats, cards, progression, coaching

app = FastAPI(
    title="League of Legends AI Analytics",
    description="AI-powered analytics platform for League of Legends players",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and Create React App defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(players.router, prefix="/api/players", tags=["players"])
app.include_router(matches.router, prefix="/api/matches", tags=["matches"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])
app.include_router(cards.router, prefix="/api/cards", tags=["cards"])
app.include_router(progression.router, prefix="/api/progression", tags=["progression"])
app.include_router(coaching.router, prefix="/api/coaching", tags=["coaching"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "League of Legends AI Analytics",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "ok",
            "database": "ok",  # Add actual health checks
            "riot_api": "ok",
            "aws": "ok"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
