---
phase: 4
plan: 2
wave: 1
---

# Plan 4.2: Backend Integration & Itinerary Rendering

## Objective
Connect the React frontend to the FastAPI backend and render the structured travel itinerary returned by the AI agent.

## Context
- backend/main.py
- .gsd/REQUIREMENTS.md

## Tasks

<task type="auto">
  <name>Integrate API and Render Result</name>
  <files>
    - frontend/src/App.jsx
  </files>
  <action>
    - Implement an `handleSubmit` function using `axios` to POST the user inputs to `http://localhost:8000/plan-trip`.
    - Handle the response by storing the `itinerary` and `status` in state.
    - Create a dedicated "Itinerary" section in the UI that parses the Markdown or text response and displays it cleanly.
    - Ensure errors are handled gracefully with a user-friendly message.
  </action>
  <verify>Get-Content frontend/src/App.jsx | Select-String "axios.post"</verify>
  <done>Frontend is connected to the backend and displays the agent's itinerary.</done>
</task>

## Success Criteria
- [ ] API call successfully triggers the backend agent.
- [ ] Final itinerary is displayed on the screen.
- [ ] End-to-home flow works.
