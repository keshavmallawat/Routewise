---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Foundation & Backend Setup

## Objective
Set up the modular folder structure, standard configuration files, and initialize the FastAPI backend server with the `POST /plan-trip` endpoint.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md
- .gsd/REQUIREMENTS.md

## Tasks

<task type="auto">
  <name>Initialize Folder Structure and Config</name>
  <files>
    - .env.example
    - README.md
    - backend/
    - frontend/
    - tools/
    - data/
  </files>
  <action>
    - Create the base modular directories: `frontend`, `backend`, `tools`, `data`.
    - Create a `.env.example` file that includes placeholder keys for `OPENROUTER_API_KEY` and `TAVILY_API_KEY`.
    - Create a basic `README.md` introducing "Routewise – AI Travel Planning Agent" and its architecture.
    - Avoid creating actual `.env` with real credentials to prevent secrets leakage.
  </action>
  <verify>Get-ChildItem -Path . -Name -Include "frontend", "backend", "tools", "data", ".env.example" | Measure-Object | Select-Object -ExpandProperty Count</verify>
  <done>Folder structure is present and `.env.example` contains required placeholder keys.</done>
</task>

<task type="auto">
  <name>Setup FastAPI Backend Server</name>
  <files>
    - backend/main.py
    - backend/requirements.txt
  </files>
  <action>
    - Create `backend/requirements.txt` with `fastapi` and `uvicorn`.
    - Create `backend/main.py` initializing a FastAPI app.
    - Add a basic health check `GET /` endpoint.
    - Add a `POST /plan-trip` endpoint that accepts Pydantic models for `destination` (str), `budget` (str/float), and `days` (int).
    - The `/plan-trip` endpoint should currently return a mock structured itinerary response.
    - Avoid running the server in the action step, just write the code.
  </action>
  <verify>Get-Content backend/main.py | Select-String "/plan-trip"</verify>
  <done>FastAPI backend is implemented with the correct `POST /plan-trip` endpoint and Pydantic models.</done>
</task>

## Success Criteria
- [ ] Directory structure (`frontend/`, `backend/`, `tools/`, `data/`) exists.
- [ ] `.env.example` exists with required placeholders.
- [ ] `backend/main.py` exists with a working FastAPI application and `/plan-trip` endpoint.
