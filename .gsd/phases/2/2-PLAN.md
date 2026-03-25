---
phase: 2
plan: 2
wave: 1
---

# Plan 2.2: Implement Mandatory Agent Tools

## Objective
Create the three required tools for the CrewAI Agent: Tavily Search Tool, CSV Pandas Dataset Tool, and Calculator Tool.

## Context
- .gsd/SPEC.md
- .gsd/REQUIREMENTS.md
- backend/agent_core.py

## Tasks

<task type="auto">
  <name>Create CSV Dataset and Setup Data Folder</name>
  <files>
    - data/destinations.csv
    - backend/requirements.txt
  </files>
  <action>
    - Add `pandas` to `backend/requirements.txt`.
    - Create a sample `data/destinations.csv` with columns: `City, Attractions, AverageCost, BestSeason`.
    - Populate it with at least 5 cities (e.g., Paris, Tokyo, New York, Bali, Rome) and realistic data.
  </action>
  <verify>Get-Content data/destinations.csv | Select-Object -First 1 | Select-String "City,Attractions"</verify>
  <done>CSV dataset exists with correct headers and sample data.</done>
</task>

<task type="auto">
  <name>Implement Custom Tools</name>
  <files>
    - backend/tools.py
    - backend/requirements.txt
  </files>
  <action>
    - Remove `langchain-community`, and replace it with `requests` if not already present in requirements (though Tavily has its own client). Ensure `tavily-python` and `numexpr` are in `backend/requirements.txt`.
    - Create `backend/tools.py`.
    - Import `tool` from `crewai.tools` instead of LangChain's decorator.
    - Implement a `TavilySearchTool` wrapper using the `tavily-python` client directly and decorating a python function with `@tool("Search web")`.
    - Implement a custom `CalculatorTool` using `@tool("Calculate")` that takes a mathematical expression as a string and evaluates it safely using `numexpr` or basic math.
    - Implement a `CSVDatasetTool` using `@tool("Search CSV")` that loads `data/destinations.csv` with Pandas and searches by city name, returning a formatted string.
  </action>
  <verify>Get-Content backend/tools.py | Select-String "from crewai.tools import tool"</verify>
  <done>Three distinct plain Python tools (Tavily, Calculator, CSV) are defined using CrewAI's native `@tool` decorator, without LangChain.</done>
</task>

## Success Criteria
- [ ] `data/destinations.csv` exists and is formatted correctly.
- [ ] `backend/tools.py` successfully defines the three mandatory tools.
