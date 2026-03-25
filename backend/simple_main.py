from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

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
    Simple mock travel planning endpoint (CrewAI integration temporarily disabled)
    """
    try:
        # Generate a simple mock itinerary
        mock_itinerary = f"""
# Travel Itinerary for {request.destination}

## Budget: ${request.budget} for {request.days} days

## Day 1: Arrival and Exploration
- Morning: Arrive at {request.destination}
- Afternoon: Check into hotel and explore local area
- Evening: Dinner at a local restaurant
- Estimated Cost: ${request.budget * 0.2:.2f}

## Day 2: Main Attractions
- Morning: Visit famous landmarks
- Afternoon: Cultural activities and museums
- Evening: Local entertainment
- Estimated Cost: ${request.budget * 0.3:.2f}

## Day 3: Local Experiences
- Morning: Shopping and local markets
- Afternoon: Outdoor activities or relaxation
- Evening: Farewell dinner
- Estimated Cost: ${request.budget * 0.25:.2f}

## Additional Days
- Each additional day: ${request.budget * 0.25:.2f}

## Total Estimated Cost: ${request.budget:.2f}

## Notes
- Prices are estimates and may vary
- Book accommodations and activities in advance
- Consider travel insurance for longer trips
        """
        
        return TripResponse(
            status="success",
            itinerary=mock_itinerary.strip(),
            reasoning_logs="Mock itinerary generated (CrewAI agent temporarily disabled due to compatibility issues)"
        )
    
    except Exception as e:
        return TripResponse(
            status="error",
            itinerary="An error occurred while generating the itinerary.",
            reasoning_logs=f"Error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_main:app", host="0.0.0.0", port=8001, reload=True)
