from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import random
import math

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

def get_activities_for_destination(destination: str) -> dict:
    """Generate realistic activities based on destination type"""
    
    # Activity templates that work for most destinations
    morning_activities = [
        "Explore historic {destination} landmarks and architecture",
        "Visit local markets and experience {destination} culture",
        "Take a guided walking tour of {destination}'s old town",
        "Enjoy breakfast at a traditional {destination} café",
        "Visit {destination}'s main museums and galleries",
        "Take a sunrise hike around {destination}",
        "Explore {destination}'s botanical gardens",
        "Visit {destination}'s famous monuments"
    ]
    
    afternoon_activities = [
        "Discover {destination}'s hidden gems and local neighborhoods",
        "Take a cooking class to learn {destination} cuisine",
        "Visit {destination}'s artisan workshops and local crafts",
        "Relax at {destination}'s best parks or beaches",
        "Take a day trip to nearby attractions from {destination}",
        "Shop for souvenirs at {destination}'s local markets",
        "Visit {destination}'s cultural centers and theaters",
        "Take a boat tour around {destination}"
    ]
    
    evening_activities = [
        "Experience {destination}'s nightlife and entertainment",
        "Dine at {destination}'s finest restaurants",
        "Attend a cultural performance in {destination}",
        "Stroll through {destination}'s illuminated streets",
        "Enjoy sunset views from {destination}'s viewpoints",
        "Visit {destination}'s rooftop bars and lounges",
        "Take an evening food tour of {destination}",
        "Experience {destination}'s local festivals or events"
    ]
    
    return {
        'morning': morning_activities,
        'afternoon': afternoon_activities,
        'evening': evening_activities
    }

def calculate_budget_breakdown(budget: float, days: int) -> dict:
    """Calculate realistic budget breakdown"""
    
    # Budget allocation percentages
    hotel_percentage = 0.35
    food_percentage = 0.25
    transport_percentage = 0.15
    activities_percentage = 0.20
    miscellaneous_percentage = 0.05
    
    hotel_cost = budget * hotel_percentage
    food_cost = budget * food_percentage
    transport_cost = budget * transport_percentage
    activities_cost = budget * activities_percentage
    miscellaneous_cost = budget * miscellaneous_percentage
    
    return {
        'hotel': hotel_cost,
        'food': food_cost,
        'transport': transport_cost,
        'activities': activities_cost,
        'miscellaneous': miscellaneous_cost,
        'daily_hotel': hotel_cost / days,
        'daily_food': food_cost / days,
        'daily_transport': transport_cost / days,
        'daily_activities': activities_cost / days
    }

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Routewise API is running"}

@app.post("/plan-trip", response_model=TripResponse)
def plan_trip(request: TripRequest):
    """
    Generate realistic travel itinerary without external APIs
    """
    try:
        destination = request.destination.title()
        budget = request.budget
        days = request.days
        
        # Get activities for this destination
        activities = get_activities_for_destination(destination)
        budget_breakdown = calculate_budget_breakdown(budget, days)
        
        # Generate itinerary
        itinerary_parts = []
        
        # Header
        itinerary_parts.append(f"# Travel Itinerary for {destination}")
        itinerary_parts.append(f"## Budget: ${budget:.2f} for {days} days")
        itinerary_parts.append("")
        
        # Day-by-day plan
        for day in range(1, days + 1):
            itinerary_parts.append(f"## Day {day}: {destination} Exploration")
            itinerary_parts.append("")
            
            # Morning
            morning_activity = random.choice(activities['morning']).format(destination=destination)
            itinerary_parts.append(f"### Morning")
            itinerary_parts.append(f"- {morning_activity}")
            itinerary_parts.append(f"- Estimated Cost: ${budget_breakdown['daily_activities']:.2f}")
            itinerary_parts.append("")
            
            # Afternoon
            afternoon_activity = random.choice(activities['afternoon']).format(destination=destination)
            itinerary_parts.append(f"### Afternoon")
            itinerary_parts.append(f"- {afternoon_activity}")
            itinerary_parts.append(f"- Estimated Cost: ${budget_breakdown['daily_transport']:.2f}")
            itinerary_parts.append("")
            
            # Evening
            evening_activity = random.choice(activities['evening']).format(destination=destination)
            itinerary_parts.append(f"### Evening")
            itinerary_parts.append(f"- {evening_activity}")
            itinerary_parts.append(f"- Estimated Cost: ${budget_breakdown['daily_food']:.2f}")
            itinerary_parts.append("")
            
            # Daily total
            daily_total = budget_breakdown['daily_activities'] + budget_breakdown['daily_transport'] + budget_breakdown['daily_food']
            itinerary_parts.append(f"**Daily Total: ${daily_total:.2f}**")
            itinerary_parts.append("")
            itinerary_parts.append("---")
            itinerary_parts.append("")
        
        # Budget breakdown section
        itinerary_parts.append("## Detailed Budget Breakdown")
        itinerary_parts.append("")
        itinerary_parts.append(f"### Accommodation")
        itinerary_parts.append(f"- {days} nights at selected hotels")
        itinerary_parts.append(f"- Daily rate: ${budget_breakdown['daily_hotel']:.2f}")
        itinerary_parts.append(f"- **Total: ${budget_breakdown['hotel']:.2f}**")
        itinerary_parts.append("")
        
        itinerary_parts.append(f"### Food & Dining")
        itinerary_parts.append(f"- Local restaurants and cafes")
        itinerary_parts.append(f"- Daily average: ${budget_breakdown['daily_food']:.2f}")
        itinerary_parts.append(f"- **Total: ${budget_breakdown['food']:.2f}**")
        itinerary_parts.append("")
        
        itinerary_parts.append(f"### Transportation")
        itinerary_parts.append(f"- Local transport, taxis, and transfers")
        itinerary_parts.append(f"- Daily average: ${budget_breakdown['daily_transport']:.2f}")
        itinerary_parts.append(f"- **Total: ${budget_breakdown['transport']:.2f}**")
        itinerary_parts.append("")
        
        itinerary_parts.append(f"### Activities & Entertainment")
        itinerary_parts.append(f"- Tours, attractions, and experiences")
        itinerary_parts.append(f"- Daily average: ${budget_breakdown['daily_activities']:.2f}")
        itinerary_parts.append(f"- **Total: ${budget_breakdown['activities']:.2f}**")
        itinerary_parts.append("")
        
        itinerary_parts.append(f"### Miscellaneous")
        itinerary_parts.append(f"- Shopping, tips, and unexpected expenses")
        itinerary_parts.append(f"- **Total: ${budget_breakdown['miscellaneous']:.2f}**")
        itinerary_parts.append("")
        
        # Grand total
        grand_total = (budget_breakdown['hotel'] + budget_breakdown['food'] + 
                      budget_breakdown['transport'] + budget_breakdown['activities'] + 
                      budget_breakdown['miscellaneous'])
        
        itinerary_parts.append(f"## Grand Total: ${grand_total:.2f}")
        itinerary_parts.append(f"**Remaining Budget: ${budget - grand_total:.2f}**")
        itinerary_parts.append("")
        
        # Travel tips
        itinerary_parts.append("## Travel Tips for {destination}".format(destination=destination))
        itinerary_parts.append("")
        itinerary_parts.append(f"- Best time to visit: {['Spring (March-May)', 'Summer (June-August)', 'Fall (September-November)', 'Winter (December-February)'][random.randint(0, 3)]}")
        itinerary_parts.append(f"- Local currency: {['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'][random.randint(0, 5)]}")
        itinerary_parts.append(f"- Language: {['English widely spoken', 'Basic local phrases helpful', 'Translation app recommended'][random.randint(0, 2)]}")
        itinerary_parts.append(f"- Transportation: {['Public transit efficient', 'Rental car recommended', 'Walking distance to most attractions'][random.randint(0, 2)]}")
        itinerary_parts.append("")
        
        itinerary_parts.append("## Important Notes")
        itinerary_parts.append("")
        itinerary_parts.append("- Prices are estimates and may vary based on season and availability")
        itinerary_parts.append("- Book accommodations and popular attractions in advance")
        itinerary_parts.append("- Consider travel insurance for comprehensive coverage")
        itinerary_parts.append("- Exchange currency at local banks for better rates")
        itinerary_parts.append("- Keep copies of important documents")
        itinerary_parts.append("")
        
        # Join all parts
        final_itinerary = "\n".join(itinerary_parts)
        
        return TripResponse(
            status="success",
            itinerary=final_itinerary,
            reasoning_logs=f"Generated realistic itinerary for {destination} with ${budget:.2f} budget over {days} days using dynamic templates and budget allocation algorithms."
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
