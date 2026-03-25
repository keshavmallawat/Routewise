from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from crewai import Task, Crew
from agent_core import travel_planner_agent
from tools import search_web, calculate_expression, search_csv

app = FastAPI(title="Routewise API", description="Backend for Routewise - AI Travel Planning Agent")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models for request
class TripRequest(BaseModel):
    destination: str
    budget: float
    days: int

class TripResponse(BaseModel):
    status: str
    itinerary: str
    reasoning_logs: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Routewise API is running"}

@app.post("/plan-trip", response_model=TripResponse)
def plan_trip(request: TripRequest):
    """
    Execute CrewAI workflow with ReAct reasoning to generate travel itineraries.
    The agent will:
    1. Search CSV for city insights and base costs
    2. Search web for real-time travel information
    3. Calculate budget breakdown across days
    """
    try:
        # Create the travel planning task with explicit ReAct workflow
        travel_task = Task(
            description=f"""
            Your goal is to create a production-grade, optimized travel itinerary for {request.destination} with a budget of ${request.budget} for {request.days} days.
            
            You MUST follow the ReAct reasoning pattern strictly for every step:
            Thought: [Your reasoning about what to do next]
            Action: [The tool you will use]
            Observation: [The result from the tool]
            ... (Repeat as needed)
            Final Answer: [Your complete, structured itinerary]
            
            STRICT TOOL SEQUENCE REQUIRED:
            1. Use 'Search CSV' first to retrieve city insights, attractions, and average costs from our local database.
            2. Use 'Search web' to fetch real-time weather, current events, and any travel advisories for {request.destination}.
            3. Use 'Calculate' to perform a detailed breakdown of the ${request.budget} budget across {request.days} days, ensuring it covers the costs gathered.
            
            The final itinerary must be well-structured and include:
            - Day-wise breakdown (Day 1, Day 2, etc.)
            - Attractions to visit (combining local data and real-time info)
            - Estimated daily and total cost breakdown
            - Best season/time recommendations
            
            Destination: {request.destination}
            Budget: ${request.budget}
            Days: {request.days}
            """,
            expected_output="A structured travel itinerary with daily plans, cost analysis, and local recommendations.",
            agent=travel_planner_agent
        )
        
        # Create the crew with the agent and task
        crew = Crew(
            agents=[travel_planner_agent],
            tasks=[travel_task],
            verbose=True
        )
        
        # Execute the workflow
        result = crew.kickoff()
        
        return TripResponse(
            status="success",
            itinerary=str(result),
            reasoning_logs="Reasoning logs are printed to the console."
        )
    
    except Exception as e:
        return TripResponse(
            status="error",
            itinerary="An error occurred while generating the itinerary.",
            reasoning_logs=f"Error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
