---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: Define CrewAI Tasks and Execute Agent Workflow

## Objective
Connect the customized tools to the CrewAI Agent, define the exact tasks for the travel agent to execute, and integrate this into the FastAPI `/plan-trip` endpoint to enable the full ReAct workflow.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md
- backend/main.py
- backend/agent_core.py
- backend/tools.py

## Tasks

<task type="auto">
  <name>Construct CrewAI Workflow in Endpoint</name>
  <files>
    - backend/main.py
    - backend/agent_core.py
    - backend/tools.py
  </files>
  <action>
    - Update `backend/main.py` and `backend/agent_core.py` to import the tools from `tools.py`.
    - Modify `agent_core.py` or the `main.py` endpoint so the `travel_planner_agent` includes the tools array: `[search_web, calculate_expression, search_csv]`.
    - Inside the `/plan-trip` endpoint in `main.py`, create a CrewAI `Task`. The task description MUST explicitly enforce the ReAct reasoning format (Thought -> Action -> Observation -> Final Answer).
    - Instruct the agent to execute this specific sequence:
      1. Use `Search CSV` to retrieve city insights and base costs for {destination}.
      2. Use `Search web` to fetch real-time travel information, weather, or events for {destination}.
      3. Use `Calculate` to breakdown the {budget} across {days} days and estimate daily costs vs expected costs.
    - Require the final output to be well-structured including:
      - Day-wise itinerary (Day 1, Day 2, etc.)
      - Estimated daily and total cost
      - Attractions to visit
      - Best time recommendations
    - Create a `Crew` with the `travel_planner_agent` and the constructed task. Set `verbose=True` to ensure logs are clearly visible in the console.
    - Call `crew.kickoff()` to execute the flow.
    - Return the final result in the `itinerary` field of `TripResponse`.
    - For `reasoning_logs`, return a placeholder string "Reasoning logs are printed to the console."
  </action>
  <verify>Get-Content backend/main.py | Select-String "crew.kickoff()"</verify>
  <done>The FastAPI endpoint triggers the CrewAI workflow utilizing all three tools and returns the generated itinerary.</done>
</task>

## Success Criteria
- [ ] Agent is equipped with the 3 custom tools.
- [ ] `/plan-trip` endpoint executes the `Crew` kickoff.
- [ ] The generated response is returned as the API response.
