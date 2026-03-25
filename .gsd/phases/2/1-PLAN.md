---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: OpenRouter & CrewAI Integration

## Objective
Integrate the OpenRouter LLM through Langchain/OpenAI-compatible endpoints and set up the foundation for the CrewAI Travel Planner Agent.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md
- backend/main.py

## Tasks

<task type="auto">
  <name>Configure CrewAI Agent</name>
  <files>
    - backend/requirements.txt
    - backend/agent_core.py
  </files>
  <action>
    - Add `crewai`, `langchain-openai`, and `python-dotenv` to `backend/requirements.txt`.
    - Create `backend/agent_core.py`.
    - Set up the LLM instance using `ChatOpenAI` pointing to the OpenRouter base URL (`"https://openrouter.ai/api/v1"`).
    - Read `OPENROUTER_API_KEY` from environment variables using `python-dotenv`.
    - Define a CrewAI `Agent` representing the "Travel Planner Agent". Include its `role`, `goal`, `backstory`, `verbose=True`, and `allow_delegation=False`.
  </action>
  <verify>Get-Content backend/agent_core.py | Select-String "Agent("</verify>
  <done>CrewAI Agent is defined with OpenRouter LLM configured.</done>
</task>

## Success Criteria
- [ ] `crewai` and dependencies added to requirements.
- [ ] `agent_core.py` successfully initializes the agent with OpenRouter configuration.
