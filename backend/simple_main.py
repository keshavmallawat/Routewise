from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from crewai import Crew, Task
from agent_core import travel_planner_agent

# Load environment variables
load_dotenv()

app = FastAPI(title="Routewise API", description="Backend for Routewise - AI Travel Planning Agent using CrewAI")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    destination: str
    budget: float
    days: int


class TripResponse(BaseModel):
    status: str
    itinerary: str
    reasoning_logs: Optional[str] = None


def create_itinerary_task(destination: str, budget: float, days: int) -> Task:
    """Create a CrewAI task for itinerary generation"""
    return Task(
        description=f"""Create a detailed {days}-day travel itinerary for {destination} with a total budget of ${budget:,.2f} USD.

Requirements:
1. Use ONLY real, actual landmark names, attractions, and points of interest in {destination}
2. Include real local dishes and cuisine specific to {destination}
3. Provide realistic cost estimates in USD based on actual local prices
4. Each day must have DIFFERENT morning, afternoon, and evening activities
5. Include specific restaurants, cafés, or food markets with real names where possible
6. Budget breakdown should reflect real costs for {destination}
7. Include practical travel tips specific to {destination} (currency, language, transport, customs)
8. Mention the best time to visit and current weather considerations
9. Include local transportation methods specific to {destination}
10. Add a "Budget Reality Check" section if ${budget:,.2f} is too low

Format as a complete travel itinerary with markdown formatting. Use emojis for visual appeal.""",
        expected_output="A comprehensive day-by-day travel itinerary with budget breakdown and practical tips.",
        agent=travel_planner_agent
    )


@app.get("/")
def read_root():
    return {
        "status": "healthy", 
        "message": "Routewise API is running with CrewAI integration",
        "model": os.environ.get("MODEL_NAME", "google/gemini-2.0-flash-exp:free")
    }


@app.post("/plan-trip", response_model=TripResponse)
def plan_trip(request: TripRequest):
    """
    Generate AI-powered travel itinerary using CrewAI.
    """
    try:
        destination = request.destination.title()
        budget = request.budget
        days = request.days
        
        # Create CrewAI task
        itinerary_task = create_itinerary_task(destination, budget, days)
        
        # Execute task with CrewAI
        crew = Crew(
            agents=[travel_planner_agent],
            tasks=[itinerary_task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        if result and str(result).strip():
            return TripResponse(
                status="success",
                itinerary=str(result),
                reasoning_logs=f"Generated {days}-day itinerary for {destination} using CrewAI with {os.environ.get('MODEL_NAME', 'google/gemini-2.0-flash-exp:free')} model and ${budget:.2f} budget."
            )
        else:
            return TripResponse(
                status="error",
                itinerary="No itinerary was generated. Please try again.",
                reasoning_logs="CrewAI returned empty result"
            )
    
    except Exception as e:
        return TripResponse(
            status="error",
            itinerary="An unexpected error occurred while generating your itinerary. Please try again.",
            reasoning_logs=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("simple_main:app", host="0.0.0.0", port=port, reload=True)
