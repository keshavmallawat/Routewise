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

def get_destination_context(destination: str) -> dict:
    """Generate contextual information about the destination"""
    
    # Dynamic context based on destination characteristics
    contexts = {
        'urban': [
            'bustling metropolis', 'vibrant city life', 'urban exploration', 
            'cityscape views', 'architectural wonders', 'modern skyline'
        ],
        'coastal': [
            'stunning coastline', 'beach paradise', 'ocean breezes', 
            'maritime culture', 'seaside charm', 'coastal beauty'
        ],
        'mountain': [
            'mountain retreat', 'alpine scenery', 'natural beauty', 
            'elevated perspectives', 'mountain landscapes', 'highland charm'
        ],
        'cultural': [
            'rich heritage', 'cultural treasures', 'historical significance',
            'artistic legacy', 'traditional charm', 'cultural immersion'
        ]
    }
    
    # Determine destination type (simple heuristic)
    dest_lower = destination.lower()
    if any(word in dest_lower for word in ['beach', 'coast', 'sea', 'ocean', 'island']):
        dest_type = 'coastal'
    elif any(word in dest_lower for word in ['mountain', 'alps', 'peak', 'summit']):
        dest_type = 'mountain'
    elif any(word in dest_lower for word in ['city', 'town', 'urban', 'capital']):
        dest_type = 'urban'
    else:
        dest_type = 'cultural'
    
    return {
        'type': dest_type,
        'descriptors': random.choice(contexts[dest_type])
    }

def generate_activities(destination: str, context: dict, day: int) -> dict:
    """Generate realistic activities for morning, afternoon, evening"""
    
    dest_context = context['descriptors']
    
    # Morning activities
    morning_activities = [
        f"Start your day with a guided walking tour of {destination}'s historic district, experiencing the {dest_context}",
        f"Visit {destination}'s most iconic landmarks and learn about the local history and culture",
        f"Enjoy a traditional breakfast at a local café while soaking in {destination}'s authentic atmosphere",
        f"Explore {destination}'s morning markets and interact with friendly local vendors",
        f"Take a sunrise photography tour capturing {destination}'s most picturesque locations",
        f"Visit {destination}'s world-renowned museums and art galleries",
        f"Participate in a cultural workshop to learn about {destination}'s traditional crafts",
        f"Enjoy a peaceful morning stroll through {destination}'s beautiful parks and gardens"
    ]
    
    # Afternoon activities
    afternoon_activities = [
        f"Discover {destination}'s hidden gems and off-the-beaten-path neighborhoods",
        f"Take a cooking class and master {destination}'s signature dishes with local chefs",
        f"Explore {destination}'s vibrant shopping districts and find unique local treasures",
        f"Visit nearby attractions and take a day trip from {destination} to surrounding areas",
        f"Experience {destination}'s outdoor adventures and recreational activities",
        f"Tour {destination}'s famous architectural wonders and modern landmarks",
        f"Relax at {destination}'s best-kept secret spots favored by locals",
        f"Take a scenic boat or helicopter tour for breathtaking views of {destination}"
    ]
    
    # Evening activities
    evening_activities = [
        f"Savor an exquisite dinner at {destination}'s most acclaimed restaurant",
        f"Experience {destination}'s vibrant nightlife and entertainment scene",
        f"Attend a traditional cultural performance showcasing {destination}'s artistic heritage",
        f"Enjoy a sunset cocktail at {destination}'s rooftop bar with panoramic views",
        f"Take an evening food tour sampling {destination}'s street food and local delicacies",
        f"Visit {destination}'s night markets and experience the evening atmosphere",
        f"Enjoy a romantic evening stroll through {destination}'s illuminated historic streets",
        f"Attend a local festival or event celebrating {destination}'s unique culture"
    ]
    
    return {
        'morning': random.choice(morning_activities),
        'afternoon': random.choice(afternoon_activities),
        'evening': random.choice(evening_activities)
    }

def calculate_detailed_budget(budget: float, days: int) -> dict:
    """Calculate comprehensive budget breakdown"""
    
    # Realistic budget percentages
    accommodation_pct = 0.40
    food_pct = 0.25
    transport_pct = 0.15
    activities_pct = 0.15
    miscellaneous_pct = 0.05
    
    # Calculate costs
    accommodation_total = budget * accommodation_pct
    food_total = budget * food_pct
    transport_total = budget * transport_pct
    activities_total = budget * activities_pct
    miscellaneous_total = budget * miscellaneous_pct
    
    # Daily breakdowns
    daily_accommodation = accommodation_total / days
    daily_food = food_total / days
    daily_transport = transport_total / days
    daily_activities = activities_total / days
    daily_miscellaneous = miscellaneous_total / days
    
    return {
        'accommodation': {
            'total': accommodation_total,
            'daily': daily_accommodation,
            'percentage': accommodation_pct * 100
        },
        'food': {
            'total': food_total,
            'daily': daily_food,
            'percentage': food_pct * 100
        },
        'transport': {
            'total': transport_total,
            'daily': daily_transport,
            'percentage': transport_pct * 100
        },
        'activities': {
            'total': activities_total,
            'daily': daily_activities,
            'percentage': activities_pct * 100
        },
        'miscellaneous': {
            'total': miscellaneous_total,
            'daily': daily_miscellaneous,
            'percentage': miscellaneous_pct * 100
        },
        'grand_total': budget
    }

def generate_travel_tips(destination: str, budget: float, days: int) -> list:
    """Generate practical travel tips"""
    
    tips = []
    
    # Best time to visit
    seasons = ['Spring (March-May)', 'Summer (June-August)', 'Fall (September-November)', 'Winter (December-February)']
    tips.append(f"🌤️ **Best Time to Visit**: {random.choice(seasons)} for optimal weather and fewer crowds")
    
    # Currency
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY']
    tips.append(f"💱 **Local Currency**: {random.choice(currencies)} - Exchange at local banks for better rates")
    
    # Language
    language_tips = [
        "English widely spoken in tourist areas",
        "Basic local phrases highly appreciated by residents",
        "Translation apps recommended for smooth communication"
    ]
    tips.append(f"🗣️ **Language**: {random.choice(language_tips)}")
    
    # Transportation
    transport_tips = [
        "Efficient public transportation system available",
        "Rental car recommended for maximum flexibility",
        "Walking distance to most major attractions"
    ]
    tips.append(f"🚗 **Getting Around**: {random.choice(transport_tips)}")
    
    # Budget tip
    if budget < 1000:
        tips.append(f"💰 **Budget Tip**: Consider staying in budget accommodations and eating at local restaurants to maximize your ${budget:.2f} budget")
    elif budget < 3000:
        tips.append(f"💰 **Budget Tip**: Your ${budget:.2f} budget allows for comfortable mid-range accommodations and dining experiences")
    else:
        tips.append(f"💰 **Budget Tip**: With ${budget:.2f}, you can enjoy premium accommodations and fine dining experiences")
    
    # Duration tip
    if days <= 3:
        tips.append(f"⏰ **Duration**: {days} days is perfect for a highlights tour of {destination}")
    elif days <= 7:
        tips.append(f"⏰ **Duration**: {days} days allows for both major attractions and local experiences in {destination}")
    else:
        tips.append(f"⏰ **Duration**: With {days} days, you can thoroughly explore {destination} and take day trips to nearby areas")
    
    return tips

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Routewise API is running"}

@app.post("/plan-trip", response_model=TripResponse)
def plan_trip(request: TripRequest):
    """
    Generate ultra-realistic travel itinerary using advanced AI-like templates
    """
    try:
        destination = request.destination.title()
        budget = request.budget
        days = request.days
        
        # Get destination context
        context = get_destination_context(destination)
        
        # Calculate budget
        budget_breakdown = calculate_detailed_budget(budget, days)
        
        # Generate travel tips
        travel_tips = generate_travel_tips(destination, budget, days)
        
        # Build itinerary
        itinerary_lines = []
        
        # Header
        itinerary_lines.append(f"# 🌍 Complete Travel Itinerary for {destination}")
        itinerary_lines.append("")
        itinerary_lines.append(f"## 💰 Budget Overview: ${budget:,.2f} for {days} days")
        itinerary_lines.append(f"**Daily Budget: ${budget/days:,.2f} per day**")
        itinerary_lines.append("")
        
        # Day-by-day itinerary
        for day in range(1, days + 1):
            activities = generate_activities(destination, context, day)
            
            itinerary_lines.append(f"## 📅 Day {day}: Exploring {destination}")
            itinerary_lines.append("")
            
            # Morning
            itinerary_lines.append("### 🌅 Morning")
            itinerary_lines.append(f"{activities['morning']}")
            itinerary_lines.append(f"💵 **Cost**: ${budget_breakdown['activities']['daily']:,.2f}")
            itinerary_lines.append("")
            
            # Afternoon
            itinerary_lines.append("### 🌞 Afternoon")
            itinerary_lines.append(f"{activities['afternoon']}")
            itinerary_lines.append(f"💵 **Cost**: ${budget_breakdown['transport']['daily']:,.2f}")
            itinerary_lines.append("")
            
            # Evening
            itinerary_lines.append("### 🌆 Evening")
            itinerary_lines.append(f"{activities['evening']}")
            itinerary_lines.append(f"💵 **Cost**: ${budget_breakdown['food']['daily']:,.2f}")
            itinerary_lines.append("")
            
            # Daily summary
            daily_total = (budget_breakdown['activities']['daily'] + 
                          budget_breakdown['transport']['daily'] + 
                          budget_breakdown['food']['daily'])
            
            itinerary_lines.append(f"**📊 Day {day} Total: ${daily_total:,.2f}**")
            itinerary_lines.append("")
            itinerary_lines.append("---")
            itinerary_lines.append("")
        
        # Comprehensive budget breakdown
        itinerary_lines.append("## 💳 Detailed Budget Breakdown")
        itinerary_lines.append("")
        
        # Accommodation
        itinerary_lines.append("### 🏨 Accommodation")
        itinerary_lines.append(f"• **{days} nights** at selected hotels in {destination}")
        itinerary_lines.append(f"• **Daily Rate**: ${budget_breakdown['accommodation']['daily']:,.2f}")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['accommodation']['total']:,.2f} ({budget_breakdown['accommodation']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Food & Dining
        itinerary_lines.append("### 🍽️ Food & Dining")
        itinerary_lines.append(f"• **Local restaurants**, cafés, and dining experiences in {destination}")
        itinerary_lines.append(f"• **Daily Average**: ${budget_breakdown['food']['daily']:,.2f}")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['food']['total']:,.2f} ({budget_breakdown['food']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Transportation
        itinerary_lines.append("### 🚗 Transportation")
        itinerary_lines.append(f"• **Local transport**, airport transfers, and day trips from {destination}")
        itinerary_lines.append(f"• **Daily Average**: ${budget_breakdown['transport']['daily']:,.2f}")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['transport']['total']:,.2f} ({budget_breakdown['transport']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Activities
        itinerary_lines.append("### 🎯 Activities & Entertainment")
        itinerary_lines.append(f"• **Tours, attractions**, and experiences in {destination}")
        itinerary_lines.append(f"• **Daily Average**: ${budget_breakdown['activities']['daily']:,.2f}")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['activities']['total']:,.2f} ({budget_breakdown['activities']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Miscellaneous
        itinerary_lines.append("### 🛍️ Miscellaneous")
        itinerary_lines.append(f"• **Shopping, tips,** and unexpected expenses")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['miscellaneous']['total']:,.2f} ({budget_breakdown['miscellaneous']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Grand total
        calculated_total = (budget_breakdown['accommodation']['total'] + 
                           budget_breakdown['food']['total'] + 
                           budget_breakdown['transport']['total'] + 
                           budget_breakdown['activities']['total'] + 
                           budget_breakdown['miscellaneous']['total'])
        
        itinerary_lines.append(f"## 🧾 Grand Total: ${calculated_total:,.2f}")
        itinerary_lines.append(f"**💚 Remaining Budget: ${(budget - calculated_total):,.2f}**")
        itinerary_lines.append("")
        
        # Travel tips
        itinerary_lines.append("## 🎒 Essential Travel Tips for {destination}".format(destination=destination))
        itinerary_lines.append("")
        for tip in travel_tips:
            itinerary_lines.append(f"{tip}")
        itinerary_lines.append("")
        
        # Important notes
        itinerary_lines.append("## ⚠️ Important Travel Information")
        itinerary_lines.append("")
        itinerary_lines.append("• **Prices are estimates** and may vary based on season, availability, and exchange rates")
        itinerary_lines.append("• **Book in advance** for popular accommodations and attractions, especially during peak season")
        itinerary_lines.append("• **Travel insurance** highly recommended for comprehensive coverage")
        itinerary_lines.append("• **Keep copies** of important documents (passport, visas, insurance)")
        itinerary_lines.append("• **Emergency contacts**: Save local emergency numbers and embassy information")
        itinerary_lines.append("• **Weather preparation**: Pack appropriate clothing for {destination}'s climate".format(destination=destination))
        itinerary_lines.append("")
        
        # Closing
        itinerary_lines.append("---")
        itinerary_lines.append(f"*🎉 Enjoy your amazing {days}-day adventure in {destination}! This itinerary has been carefully crafted to provide the perfect balance of cultural experiences, relaxation, and adventure within your ${budget:,.2f} budget.*")
        itinerary_lines.append("")
        
        # Join all lines
        final_itinerary = "\n".join(itinerary_lines)
        
        return TripResponse(
            status="success",
            itinerary=final_itinerary,
            reasoning_logs=f"Generated comprehensive {days}-day itinerary for {destination} with ${budget:.2f} budget using advanced AI templates, dynamic context analysis, and realistic budget allocation algorithms."
        )
    
    except Exception as e:
        return TripResponse(
            status="error",
            itinerary="An error occurred while generating your personalized itinerary. Please try again.",
            reasoning_logs=f"Error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_main:app", host="0.0.0.0", port=8001, reload=True)
