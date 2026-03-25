import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool

# Import raw tool functions from tools.py
from tools import search_web as _search_web, calculate_expression as _calc, search_csv as _search_csv

load_dotenv()

# Wrap as LangChain Tool objects — required by crewai 0.22.5
search_web_tool = Tool.from_function(
    func=_search_web,
    name="Search web",
    description="Search the internet for real-time travel info, weather, events. Input: search query string."
)

calculate_tool = Tool.from_function(
    func=_calc,
    name="Calculate",
    description="Evaluate a math expression for budgeting. Input: expression string like '2000 / 5'."
)

search_csv_tool = Tool.from_function(
    func=_search_csv,
    name="Search CSV",
    description="Look up city data (attractions, costs, best season) from local database. Input: city name."
)

# Initialize OpenRouter LLM (OpenAI-compatible)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY", "dummy_key"),
    model="openai/gpt-4o-mini",
    temperature=0.7
)

travel_planner_agent = Agent(
    role="Expert Travel Planner",
    goal="Create the most personalized and optimized travel itineraries based on destination, budget, and time.",
    backstory=(
        "You are an experienced travel agent who has lived all over the world. "
        "You excel at balancing costs with incredible experiences and creating structured, actionable itineraries. "
        "You think step-by-step to gather information and output clear, day-by-day advice."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_web_tool, calculate_tool, search_csv_tool]
)

