# SPEC.md — Project Specification

> **Status**: `FINALIZED`

## Vision
A production-grade full stack Agentic AI application named "Routewise – AI Travel Planning Agent" that generates optimized travel itineraries based on destination, budget, and duration, utilizing a React frontend, FastAPI backend, and a CrewAI-based intelligent agent.

## Goals
1. Provide a modern, clean React.js frontend for users to input travel details (destination, budget, days) and view structured itineraries.
2. Implement a FastAPI backend with a POST `/plan-trip` endpoint to handle inputs and coordinate with the agent layer.
3. Integrate a CrewAI-based Travel Planner Agent with specific roles, goals, and backstories, powered by an OpenRouter LLM.
4. Utilize mandatory tools including Tavily Search (real-time data), a Pandas CSV Dataset Tool (local destination data), and a Calculator Tool (cost estimation).
5. Ensure the agent uses the ReAct reasoning pattern (Thought → Action → Observation → Final Answer) and logs reasoning visibly.

## Non-Goals (Out of Scope)
- Database integration for persistent storage (no database required).
- User authentication and authorization.
- Real booking of flights or hotels.

## Users
Travelers looking for quick, AI-optimized itineraries and cost estimations based on their constraints, as well as university students/evaluators reviewing the lab project for full-stack integration and agentic reasoning capabilities.

## Constraints
- Must use React.js and FastAPI.
- Must use CrewAI and OpenRouter API keys via `.env`.
- Must include specific mandatory tools (Tavily, CSV Pandas, Calculator).
- Clean modular folder structure required.

## Success Criteria
- [ ] User can input destination, budget, and days in the frontend.
- [ ] Backend successfully receives request and triggers the CrewAI agent.
- [ ] Agent successfully utilizes at least two tools to gather info and calculate costs.
- [ ] Agent successfully outputs a structured itinerary using ReAct pattern.
- [ ] Frontend displays the final itinerary clearly.
- [ ] Logs clearly demonstrate the agent's multi-step reasoning.
