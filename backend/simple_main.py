from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="Routewise API", description="Backend for Routewise - AI Travel Planning Agent using Google Gemini")

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


def create_gemini_prompt(destination: str, budget: float, days: int) -> str:
    """Create a detailed prompt for Gemini to generate a realistic itinerary."""
    return f"""You are an expert travel planner with deep knowledge of destinations worldwide.

Create a detailed {days}-day travel itinerary for {destination} with a total budget of ${budget:,.2f} USD.

REQUIREMENTS:
1. Use ONLY real, actual landmark names, attractions, and points of interest in {destination}
2. Include real local dishes and cuisine specific to {destination} (not generic food)
3. Provide realistic cost estimates in USD based on actual local prices in {destination}
4. Each day must have DIFFERENT morning, afternoon, and evening activities - never repeat the same activity
5. Include specific restaurants, cafés, or food markets with real names where possible
6. Budget breakdown should reflect real costs for {destination} (research typical prices)
7. Include practical travel tips specific to {destination} (currency, language, transport, customs)
8. Mention the best time to visit and current weather considerations
9. Include local transportation methods specific to {destination}
10. Add a "Budget Reality Check" section warning if ${budget:,.2f} is too low for {days} days in {destination}

FORMAT:
# 🌍 {days}-Day Travel Itinerary for {destination}

## 💰 Budget Overview: ${budget:,.2f} for {days} days

### Budget Reality Check
[Analyze if this budget is realistic for {destination}. If too low, explain what's realistic and what corners need to be cut.]

## 📅 Day-by-Day Itinerary

### Day 1
**🌅 Morning**
[Specific real activity with actual landmark/location name - estimated cost]

**🌞 Afternoon** 
[Different activity - different landmark - estimated cost]

**🌆 Evening**
[Different activity - real restaurant/venue name - estimated cost]

[Repeat for all {days} days - each day completely different]

## 💳 Detailed Budget Breakdown
[Breakdown reflecting real local costs: accommodation per night, meals, transport, activities, etc.]

## 🎒 Essential Travel Tips for {destination}
- 💱 Currency: [actual currency]
- 🗣️ Language: [primary language and tips]
- 🚗 Transport: [specific modes used in {destination}]
- 🌤️ Best time to visit: [actual seasons]
- ⚡ Voltage/Plugs: [if relevant]
- 📱 Emergency numbers: [local equivalents]

## ⚠️ Important Notes
[Safety tips, cultural norms, visa requirements if applicable]

Make this feel authentic and research-backed. Use emojis for visual appeal."""


def generate_itinerary_with_gemini(destination: str, budget: float, days: int) -> str:
    """Generate itinerary using Google Gemini API."""
    if not GEMINI_API_KEY:
        return """# ⚠️ Gemini API Key Not Configured

Please set GEMINI_API_KEY in your .env file to use AI-powered itinerary generation.

Get your free API key at: https://aistudio.google.com/app/apikey

Without the API key, the system cannot generate detailed itineraries."""

    try:
        # Initialize Gemini model (using free tier: gemini-1.5-flash)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create detailed prompt
        prompt = create_gemini_prompt(destination, budget, days)
        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=8000,
            )
        )
        
        if response and response.text:
            return response.text
        else:
            return "Error: Gemini returned empty response. Please try again."
            
    except Exception as e:
        return f"""# ⚠️ Error Generating Itinerary

An error occurred while calling the Gemini API:
{str(e)}

Please check:
1. Your GEMINI_API_KEY is valid and set in .env
2. You have internet connectivity
3. The Gemini API is accessible from your location

You can get a free API key at: https://aistudio.google.com/app/apikey"""


@app.get("/")
def read_root():
    return {
        "status": "healthy", 
        "message": "Routewise API is running with Gemini integration",
        "gemini_configured": bool(GEMINI_API_KEY)
    }


@app.post("/plan-trip", response_model=TripResponse)
def plan_trip(request: TripRequest):
    """
    Generate AI-powered travel itinerary using Google Gemini API.
    """
    try:
        destination = request.destination.title()
        budget = request.budget
        days = request.days
        
        # Generate itinerary using Gemini
        itinerary = generate_itinerary_with_gemini(destination, budget, days)
        
        # Determine status based on whether we got a valid itinerary
        if itinerary.startswith("# ⚠️") or itinerary.startswith("Error"):
            status = "error"
        else:
            status = "success"
        
        return TripResponse(
            status=status,
            itinerary=itinerary,
            reasoning_logs=f"Generated {days}-day itinerary for {destination} using Google Gemini (gemini-1.5-flash) with ${budget:.2f} budget."
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
