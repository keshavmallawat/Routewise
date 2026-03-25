# Routewise – AI Travel Planning Agent

A production-grade full stack Agentic AI application that generates optimized travel itineraries based on destination, budget, and duration, utilizing a React frontend, FastAPI backend, and a CrewAI-based intelligent agent powered by OpenRouter.

## Architecture
- **Frontend**: React.js
- **Backend**: FastAPI
- **Agent Layer**: CrewAI with OpenRouter LLM, equipped with Tavily Search, CSV Dataset Tool, and Calculator Tool.

## Getting Started

1. Copy `.env.example` to `.env` and fill in your API keys:
   - `OPENROUTER_API_KEY`
   - `TAVILY_API_KEY`
2. Start the Backend API (see `backend/README.md`)
3. Start the Frontend App (see `frontend/README.md`)
