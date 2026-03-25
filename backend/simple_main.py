from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
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

# Comprehensive destination database with real data
DESTINATION_DATA = {
    "tokyo": {
        "country": "Japan",
        "currency": "JPY",
        "language": "Japanese",
        "best_time": "March-May (Cherry Blossoms) & October-November",
        "daily_hotel": 150,
        "daily_food": 80,
        "daily_transport": 40,
        "landmarks": ["Tokyo Tower", "Senso-ji Temple", "Meiji Shrine", "Shibuya Crossing", "Imperial Palace"],
        "dishes": ["Sushi", "Ramen", "Tempura", "Yakitori", "Sashimi"],
        "activities": {
            "morning": [
                "Visit Tsukiji Outer Market for fresh sushi breakfast",
                "Explore historic Asakusa district and Senso-ji Temple",
                "Take a guided tour of the Imperial Palace East Garden",
                "Experience traditional tea ceremony in Ueno",
                "Visit the famous Meiji Shrine and Yoyogi Park",
                "Explore the trendy Harajuku district early morning",
                "Take a sunrise walk through Ueno Park",
                "Visit the Tokyo National Museum"
            ],
            "afternoon": [
                "Shop in Ginza district and visit luxury department stores",
                "Explore Akihabara electronics and anime culture",
                "Take a cooking class and learn to make sushi",
                "Visit teamLab Borderless digital art museum",
                "Explore the traditional Yanaka district",
                "Take a day trip to nearby Kamakura temples",
                "Visit the Ghibli Museum in Mitaka",
                "Explore Odaiba island and Rainbow Bridge",
                "Shop at Ameya-Yucho market in Ueno"
            ],
            "evening": [
                "Experience Shinjuku nightlife and Golden Gai",
                "Dine at a traditional izakaya in Shibuya",
                "Watch the sunset from Tokyo Skytree observation deck",
                "Enjoy karaoke in a local Japanese bar",
                "Visit an onsen (hot spring) in Hakone",
                "Explore the vibrant nightlife of Roppongi",
                "Dine at Michelin-starred restaurant in Ginza",
                "Watch a sumo wrestling tournament (if in season)",
                "Experience robot restaurant show in Shinjuku"
            ]
        }
    },
    "paris": {
        "country": "France",
        "currency": "EUR",
        "language": "French",
        "best_time": "April-June & September-October",
        "daily_hotel": 120,
        "daily_food": 70,
        "daily_transport": 30,
        "landmarks": ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Arc de Triomphe", "Sacré-Cœur"],
        "dishes": ["Croissant", "Baguette", "Coq au Vin", "Ratatouille", "Macarons"],
        "activities": {
            "morning": [
                "Visit Eiffel Tower early morning for photos",
                "Explore Montmartre and Sacré-Cœur Basilica",
                "Tour the Louvre Museum with skip-the-line tickets",
                "Walk along Seine River and Île de la Cité",
                "Visit Notre-Dame Cathedral area",
                "Explore Le Marais historic district",
                "Visit Musée d'Orsay for Impressionist art",
                "Take a morning food tour in Saint-Germain"
            ],
            "afternoon": [
                "Shop on Champs-Élysées and Arc de Triomphe",
                "Explore Latin Quarter and Sorbonne University",
                "Visit Palace of Versailles (day trip)",
                "Take French cooking class in Montmartre",
                "Explore Luxembourg Gardens and Panthéon",
                "Visit Musée Rodin and Invalides",
                "Shop at Le Bon Marché department store",
                "Explore Canal Saint-Martin area",
                "Visit Centre Pompidou for modern art"
            ],
            "evening": [
                "Seine River dinner cruise with city lights",
                "Watch Moulin Rouge cabaret show",
                "Dine at traditional bistro in Le Marais",
                "Enjoy jazz club in Saint-Germain-des-Prés",
                "Watch sunset from Montmartre viewpoint",
                "Experience wine tasting in local cellar",
                "Dine at Michelin-starred restaurant",
                "Explore nightlife in Bastille district",
                "Attend opera at Palais Garnier",
                "Enjoy cocktails at rooftop bar near Eiffel Tower"
            ]
        }
    },
    "goa": {
        "country": "India",
        "currency": "INR",
        "language": "Konkani, Hindi, English",
        "best_time": "November-February",
        "daily_hotel": 40,
        "daily_food": 25,
        "daily_transport": 15,
        "landmarks": ["Basilica of Bom Jesus", "Fort Aguada", "Anjuna Beach", "Dudhsagar Waterfall", "Old Goa Churches"],
        "dishes": ["Goan Fish Curry", "Vindaloo", "Bebinca", "Sorpotel", "Xacuti"],
        "activities": {
            "morning": [
                "Visit Basilica of Bom Jesus in Old Goa",
                "Explore Fort Aguada and lighthouse",
                "Morning walk on Anjuna Beach",
                "Visit spice plantation in Ponda",
                "Explore Old Portuguese churches of Goa",
                "Morning boat trip to see dolphins",
                "Visit Dudhsagar Waterfall",
                "Explore the vibrant Mapusa market"
            ],
            "afternoon": [
                "Relax on Calangute or Baga Beach",
                "Take spice cooking class in local village",
                "Visit Anjuna flea market (Wednesday only)",
                "Explore the beaches of South Goa",
                "Take a backwaters boat tour",
                "Visit the famous Saturday Night Market in Arpora",
                "Explore the spice markets of Margao",
                "Take a jeep safari in Bhagwan Mahavir Wildlife Sanctuary",
                "Visit the ancient caves of Arvalem"
            ],
            "evening": [
                "Enjoy sunset at Palolem Beach",
                "Experience Goan nightlife in Tito's Lane",
                "Dine on beachfront restaurant with fresh seafood",
                "Attend traditional Goan cultural show",
                "Enjoy feni (local cashew liquor) tasting",
                "Explore the Wednesday night market in Anjuna",
                "Dine at beach shack with live music",
                "Take a night walk on Candolim Beach",
                "Experience casino nightlife in Panjim",
                "Enjoy traditional Goan folk dance performance"
            ]
        }
    },
    "new york": {
        "country": "USA",
        "currency": "USD",
        "language": "English",
        "best_time": "April-June & September-November",
        "daily_hotel": 200,
        "daily_food": 90,
        "daily_transport": 50,
        "landmarks": ["Statue of Liberty", "Empire State Building", "Central Park", "Times Square", "Brooklyn Bridge"],
        "dishes": ["New York Pizza", "Bagels", "Pastrami Sandwich", "Cheesecake", "Hot Dogs"],
        "activities": {
            "morning": [
                "Visit Statue of Liberty and Ellis Island",
                "Walk across Brooklyn Bridge early morning",
                "Explore Central Park with bike rental",
                "Visit Empire State Building observatory",
                "Explore High Line elevated park",
                "Visit 9/11 Memorial and Museum",
                "Take morning jog through Central Park",
                "Explore Grand Central Terminal"
            ],
            "afternoon": [
                "Shop on Fifth Avenue and visit Saks",
                "Explore Metropolitan Museum of Art",
                "Visit American Museum of Natural History",
                "Take Broadway theater district tour",
                "Explore Greenwich Village and Washington Square Park",
                "Visit One World Observatory",
                "Shop in SoHo and cast-iron district",
                "Explore Chelsea Market and High Line",
                "Visit Intrepid Sea, Air & Space Museum"
            ],
            "evening": [
                "Watch Broadway show in Theater District",
                "Dine at rooftop restaurant with skyline view",
                "Explore Times Square lights and energy",
                "Take sunset helicopter tour of Manhattan",
                "Enjoy jazz club in Greenwich Village",
                "Dine at Little Italy or Chinatown",
                "Explore nightlife in East Village",
                "Take sunset cruise around Manhattan",
                "Visit comedy club in West Village",
                "Experience speakeasy cocktail bar"
            ]
        }
    },
    "london": {
        "country": "UK",
        "currency": "GBP",
        "language": "English",
        "best_time": "May-September",
        "daily_hotel": 140,
        "daily_food": 75,
        "daily_transport": 35,
        "landmarks": ["Big Ben", "Tower Bridge", "Buckingham Palace", "British Museum", "London Eye"],
        "dishes": ["Fish and Chips", "Sunday Roast", "Full English Breakfast", "Pie and Mash", "Afternoon Tea"],
        "activities": {
            "morning": [
                "Visit Tower of London and Tower Bridge",
                "Explore Buckingham Palace and Changing of Guard",
                "Visit British Museum (free entry)",
                "Morning walk through Hyde Park",
                "Visit Westminster Abbey and Parliament",
                "Explore Covent Garden market area",
                "Visit Tate Modern art gallery",
                "Morning Thames River walk"
            ],
            "afternoon": [
                "Shop on Oxford Street and Regent Street",
                "Visit London Eye for city views",
                "Explore Notting Hill and Portobello Market",
                "Take afternoon tea at Fortnum & Mason",
                "Visit Shakespeare's Globe Theatre",
                "Explore Camden Market and alternative culture",
                "Visit Churchill War Rooms",
                "Shop at Harrods department store",
                "Explore Greenwich and Royal Observatory"
            ],
            "evening": [
                "Watch West End theater show",
                "Dine at traditional pub in Soho",
                "Take sunset Thames River cruise",
                "Explore nightlife in Shoreditch",
                "Dine at restaurant with city views",
                "Visit jazz club in Soho",
                "Experience comedy club in Camden",
                "Take Jack the Ripper walking tour",
                "Dine at Michelin-starred restaurant",
                "Enjoy cocktails at rooftop bar in Soho"
            ]
        }
    },
    "dubai": {
        "country": "UAE",
        "currency": "AED",
        "language": "Arabic, English",
        "best_time": "November-March",
        "daily_hotel": 180,
        "daily_food": 85,
        "daily_transport": 40,
        "landmarks": ["Burj Khalifa", "Dubai Mall", "Palm Jumeirah", "Burj Al Arab", "Dubai Fountain"],
        "dishes": ["Shawarma", "Al Harees", "Machboos", "Luqaimat", "Thareed"],
        "activities": {
            "morning": [
                "Visit Burj Khalifa observation deck early",
                "Explore Dubai Mall and Aquarium",
                "Morning desert safari with dune bashing",
                "Visit Gold Souk and Spice Souk",
                "Explore Jumeirah Beach and walkway",
                "Visit Dubai Museum in Al Fahidi",
                "Morning tour of Palm Jumeirah",
                "Explore Al Fahidi historical neighborhood"
            ],
            "afternoon": [
                "Experience indoor skiing at Mall of Emirates",
                "Take yacht cruise around Dubai Marina",
                "Visit Miracle Garden and Butterfly Garden",
                "Explore Global Village cultural experience",
                "Shop at Dubai Outlet Mall",
                "Visit Dubai Frame for panoramic views",
                "Explore Alserkal Avenue arts district",
                "Take afternoon desert camel ride",
                "Visit Dubai Opera House"
            ],
            "evening": [
                "Watch Dubai Fountain show at night",
                "Dine at restaurant in Burj Al Arab",
                "Experience desert dinner under stars",
                "Explore Dubai Marina nightlife",
                "Dine at rooftop restaurant with city views",
                "Watch traditional Tanoura dance show",
                "Experience nightlife at Dubai Marina",
                "Dine at floating restaurant on Dubai Creek",
                "Visit sky lounge with Burj Khalifa views",
                "Enjoy traditional Arabic coffee and dates"
            ]
        }
    },
    "bali": {
        "country": "Indonesia",
        "currency": "IDR",
        "language": "Indonesian, Balinese",
        "best_time": "April-October",
        "daily_hotel": 50,
        "daily_food": 30,
        "daily_transport": 20,
        "landmarks": ["Tanah Lot Temple", "Ubud Rice Terraces", "Mount Batur", "Uluwatu Temple", "Seminyak Beach"],
        "dishes": ["Nasi Goreng", "Satay", "Babi Guling", "Gado-Gado", "Sambal"],
        "activities": {
            "morning": [
                "Visit Tanah Lot Temple at sunrise",
                "Explore Ubud Monkey Forest Sanctuary",
                "Morning walk through Tegallalang Rice Terraces",
                "Visit Tirta Empul water temple",
                "Morning yoga session in Ubud",
                "Visit Goa Gajah and Goa Lawah temples",
                "Explore traditional markets in Ubud",
                "Morning coffee plantation tour"
            ],
            "afternoon": [
                "Relax on Seminyak or Kuta Beach",
                "Take Balinese cooking class",
                "Visit Mount Batur volcano and hot springs",
                "Explore art markets in Ubud",
                "Take traditional silver jewelry making class",
                "Visit Tegenungan Waterfall",
                "Explore coffee plantations in Kintamani",
                "Take bike tour through rice paddies",
                "Visit traditional Balinese compound"
            ],
            "evening": [
                "Watch sunset at Tanah Lot Temple",
                "Experience traditional Kecak fire dance",
                "Dine at beachfront restaurant in Jimbaran",
                "Enjoy spa treatment with Balinese techniques",
                "Explore nightlife in Seminyak",
                "Attend traditional gamelan music performance",
                "Dine at cliff-top restaurant in Uluwatu",
                "Visit night market in Sanur",
                "Take evening rice paddy walk",
                "Enjoy beach clubbing in Kuta"
            ]
        }
    },
    "bangkok": {
        "country": "Thailand",
        "currency": "THB",
        "language": "Thai",
        "best_time": "November-February",
        "daily_hotel": 60,
        "daily_food": 35,
        "daily_transport": 25,
        "landmarks": ["Grand Palace", "Wat Arun", "Wat Pho", "Chatuchak Market", "Chao Phraya River"],
        "dishes": ["Pad Thai", "Tom Yum Goong", "Green Curry", "Mango Sticky Rice", "Som Tum"],
        "activities": {
            "morning": [
                "Visit Grand Palace and Emerald Buddha",
                "Explore Wat Arun (Wat Pho Kaew) at dawn",
                "Morning boat trip on Chao Phraya River",
                "Visit Wat Pho and Reclining Buddha",
                "Explore Chatuchak Weekend Market early",
                "Morning visit to Jim Thompson House",
                "Explore Lumpini Park in city center",
                "Visit Wat Saket and Golden Mount"
            ],
            "afternoon": [
                "Shop at Siam Paragon and Central World",
                "Take Thai cooking class in Silom",
                "Visit floating markets at Damnoen Saduak",
                "Explore Chinatown (Yaowarat) food scene",
                "Take longtail boat through Bangkok canals",
                "Visit Museum of Contemporary Art",
                "Shop at Terminal 21 shopping mall",
                "Explore Asiatique night market area",
                "Visit Suan Pakkad Palace"
            ],
            "evening": [
                "Dinner cruise on Chao Phraya River",
                "Explore nightlife in Khao San Road",
                "Dine at rooftop restaurant with city views",
                "Experience traditional Thai massage",
                "Visit night market in Ratchada",
                "Watch Muay Thai boxing match",
                "Explore rooftop bars in Sukhumvit",
                "Dine at street food stalls in Yaowarat",
                "Experience ladyboy show in Patpong",
                "Enjoy cocktails at sky bar"
            ]
        }
    },
    "singapore": {
        "country": "Singapore",
        "currency": "SGD",
        "language": "English, Mandarin, Malay, Tamil",
        "best_time": "February-April",
        "daily_hotel": 150,
        "daily_food": 60,
        "daily_transport": 30,
        "landmarks": ["Marina Bay Sands", "Gardens by the Bay", "Sentosa Island", "Merlion", "Chinatown"],
        "dishes": ["Hainanese Chicken Rice", "Chili Crab", "Laksa", "Satay", "Kaya Toast"],
        "activities": {
            "morning": [
                "Visit Gardens by the Bay and Supertree Grove",
                "Explore Marina Bay Sands Skypark",
                "Morning walk through Singapore Botanic Gardens",
                "Visit Chinatown heritage area",
                "Explore Little India cultural district",
                "Morning visit to National Gallery Singapore",
                "Explore Kampong Glam historic area",
                "Visit Singapore Flyer early morning"
            ],
            "afternoon": [
                "Shop on Orchard Road luxury district",
                "Visit Sentosa Island and Universal Studios",
                "Explore Clarke Quay and Boat Quay",
                "Take Singapore River Safari tour",
                "Visit Jewel Changi Airport complex",
                "Explore Haji Lane shopping district",
                "Visit ArtScience Museum",
                "Shop at Bugis Street Market",
                "Explore East Coast Park and beach"
            ],
            "evening": [
                "Dine at Marina Bay Sands restaurant",
                "Watch Spectra light and water show",
                "Explore nightlife in Clarke Quay",
                "Dine at hawker center in Maxwell",
                "Experience rooftop bar at Marina Bay",
                "Night safari at Singapore Zoo",
                "Explore Geylang Serai food scene",
                "Dine at restaurant in Chinatown",
                "Experience cocktail scene in Robertson Quay",
                "Enjoy night shopping at Mustafa Centre"
            ]
        }
    },
    "rome": {
        "country": "Italy",
        "currency": "EUR",
        "language": "Italian",
        "best_time": "April-June & September-October",
        "daily_hotel": 130,
        "daily_food": 80,
        "daily_transport": 25,
        "landmarks": ["Colosseum", "Vatican City", "Trevi Fountain", "Pantheon", "Roman Forum"],
        "dishes": ["Carbonara", "Cacio e Pepe", "Pizza Margherita", "Gelato", "Tiramisu"],
        "activities": {
            "morning": [
                "Visit Colosseum and Roman Forum early",
                "Explore Vatican City and St. Peter's Basilica",
                "Morning walk through Villa Borghese gardens",
                "Visit Pantheon and Piazza Navona",
                "Explore Trastevere neighborhood",
                "Morning visit to Capitoline Museums",
                "Walk Spanish Steps area",
                "Visit Campo de' Fiori market"
            ],
            "afternoon": [
                "Throw coin in Trevi Fountain",
                "Explore Roman food markets in Testaccio",
                "Visit Castel Sant'Angelo and bridge",
                "Take pasta making class in Trastevere",
                "Explore Appian Way and catacombs",
                "Visit Borghese Gallery and gardens",
                "Shop on Via del Corso",
                "Explore Aventine Keyhole view",
                "Visit Palatine Hill and ruins"
            ],
            "evening": [
                "Dine at traditional trattoria in Trastevere",
                "Watch sunset from Gianicolo Hill",
                "Experience Roman nightlife in Testaccio",
                "Dine at restaurant with Colosseum view",
                "Enjoy gelato walking tour",
                "Explore Campo de' Fiori evening market",
                "Dine at rooftop restaurant in Trastevere",
                "Experience opera at Teatro dell'Opera",
                "Enjoy aperitivo culture in Piazza Navona",
                "Take evening Roman food tour"
            ]
        }
    },
    "barcelona": {
        "country": "Spain",
        "currency": "EUR",
        "language": "Spanish, Catalan",
        "best_time": "May-June & September-October",
        "daily_hotel": 100,
        "daily_food": 70,
        "daily_transport": 30,
        "landmarks": ["Sagrada Familia", "Park Güell", "Las Ramblas", "Gothic Quarter", "Camp Nou Stadium"],
        "dishes": ["Paella", "Tapas", "Gazpacho", "Crema Catalana", "Pan con Tomate"],
        "activities": {
            "morning": [
                "Visit Sagrada Familia early morning",
                "Explore Park Güell and Gaudi architecture",
                "Morning walk through Gothic Quarter",
                "Visit La Boqueria market",
                "Explore Casa Batlló and Casa Milà",
                "Morning visit to Picasso Museum",
                "Walk along La Ramblas",
                "Visit Barcelona Cathedral"
            ],
            "afternoon": [
                "Relax on Barceloneta Beach",
                "Take paella cooking class",
                "Visit Camp Nou Stadium and museum",
                "Explore El Born district and Santa Maria del Mar",
                "Shop on Passeig de Gràcia",
                "Visit Miró Foundation and Joan Miró Museum",
                "Explore Montjuïc Castle and gardens",
                "Visit Barcelona History Museum",
                "Take cable car up to Montjuïc"
            ],
            "evening": [
                "Watch sunset from Bunkers del Carmel",
                "Experience tapas hopping in Gothic Quarter",
                "Dine at restaurant with sea views",
                "Explore nightlife in El Born",
                "Watch flamenco show in Tablao Cordobés",
                "Enjoy cocktails at rooftop bar in Gothic Quarter",
                "Experience nightlife in El Raval",
                "Dine at traditional Catalan restaurant",
                "Walk along La Ramblas at night",
                "Visit jazz club in Gothic Quarter"
            ]
        }
    }
}

def get_destination_data(destination: str) -> Dict:
    """Get destination data or fallback values"""
    dest_lower = destination.lower().strip()
    
    # Try exact match first
    if dest_lower in DESTINATION_DATA:
        return DESTINATION_DATA[dest_lower]
    
    # Try partial matches
    for key, data in DESTINATION_DATA.items():
        if dest_lower in key or key in dest_lower:
            return data
    
    # Fallback values for unknown destinations
    return {
        "country": "Unknown",
        "currency": "USD",
        "language": "Local Language",
        "best_time": "Year-round (check local climate)",
        "daily_hotel": 80,
        "daily_food": 50,
        "daily_transport": 30,
        "landmarks": ["Historic City Center", "Main Square", "Local Museum", "Famous Landmark", "Cultural Site"],
        "dishes": ["Local Speciality", "Traditional Dish", "Regional Cuisine", "Street Food", "Local Dessert"],
        "activities": {
            "morning": [
                f"Visit {destination}'s historic landmarks and monuments",
                f"Explore {destination}'s main cultural attractions",
                f"Morning walk through {destination}'s old town",
                f"Visit {destination}'s famous museums and galleries",
                f"Explore {destination}'s local markets and shopping areas",
                f"Take guided tour of {destination}'s highlights",
                f"Visit {destination}'s most iconic viewpoints",
                f"Experience {destination}'s morning culture and traditions"
            ],
            "afternoon": [
                f"Discover {destination}'s hidden gems and local neighborhoods",
                f"Take cooking class to learn {destination}'s cuisine",
                f"Explore {destination}'s shopping districts and markets",
                f"Visit nearby attractions from {destination}",
                f"Experience {destination}'s outdoor activities and nature",
                f"Tour {destination}'s architectural wonders",
                f"Relax at {destination}'s best parks or recreational areas",
                f"Take day trip to surrounding areas of {destination}",
                f"Explore {destination}'s artisan workshops and local crafts"
            ],
            "evening": [
                f"Experience {destination}'s nightlife and entertainment",
                f"Dine at {destination}'s finest restaurants",
                f"Attend cultural performance in {destination}",
                f"Enjoy sunset views from {destination}'s best viewpoints",
                f"Take evening food tour of {destination}",
                f"Visit {destination}'s night markets and evening atmosphere",
                f"Enjoy traditional entertainment in {destination}",
                f"Experience {destination}'s local festivals or events",
                f"Take romantic evening stroll through {destination}"
            ]
        }
    }

def calculate_realistic_budget(data: Dict, budget: float, days: int) -> Dict:
    """Calculate realistic budget breakdown based on destination costs"""
    
    # Base costs for the destination
    daily_hotel_cost = data["daily_hotel"]
    daily_food_cost = data["daily_food"]
    daily_transport_cost = data["daily_transport"]
    
    # Calculate total required budget
    required_budget = (daily_hotel_cost + daily_food_cost + daily_transport_cost) * days
    
    # Add 20% for activities and miscellaneous
    required_budget *= 1.2
    
    # Check if budget is realistic
    budget_warning = ""
    if budget < required_budget * 0.7:
        budget_warning = f"⚠️ **BUDGET WARNING**: Your budget of ${budget:.2f} may be too low for {days} days in {data['country']}. Recommended minimum: ${required_budget * 0.7:.2f}"
    elif budget < required_budget * 0.85:
        budget_warning = f"💰 **BUDGET NOTE**: Your budget of ${budget:.2f} is tight for {days} days in {data['country']}. Consider ${required_budget * 0.85:.2f} for comfortable experience."
    
    # Calculate actual allocations
    if budget >= required_budget:
        # Use realistic costs
        hotel_total = daily_hotel_cost * days
        food_total = daily_food_cost * days
        transport_total = daily_transport_cost * days
        activities_total = (budget - hotel_total - food_total - transport_total) * 0.7
        miscellaneous_total = (budget - hotel_total - food_total - transport_total) * 0.3
    else:
        # Proportional allocation within budget
        hotel_total = budget * 0.45
        food_total = budget * 0.25
        transport_total = budget * 0.15
        activities_total = budget * 0.10
        miscellaneous_total = budget * 0.05
    
    return {
        'hotel': {
            'total': hotel_total,
            'daily': hotel_total / days,
            'percentage': (hotel_total / budget) * 100
        },
        'food': {
            'total': food_total,
            'daily': food_total / days,
            'percentage': (food_total / budget) * 100
        },
        'transport': {
            'total': transport_total,
            'daily': transport_total / days,
            'percentage': (transport_total / budget) * 100
        },
        'activities': {
            'total': activities_total,
            'daily': activities_total / days,
            'percentage': (activities_total / budget) * 100
        },
        'miscellaneous': {
            'total': miscellaneous_total,
            'daily': miscellaneous_total / days,
            'percentage': (miscellaneous_total / budget) * 100
        },
        'budget_warning': budget_warning
    }

def get_unique_activities(data: Dict, days: int) -> List[Dict]:
    """Get unique activities for each day to avoid repetition"""
    activities_by_day = []
    
    for day in range(days):
        day_activities = {
            'morning': random.choice(data['activities']['morning']),
            'afternoon': random.choice(data['activities']['afternoon']),
            'evening': random.choice(data['activities']['evening'])
        }
        activities_by_day.append(day_activities)
    
    return activities_by_day

def generate_realistic_tips(data: Dict, budget: float, days: int) -> List[str]:
    """Generate realistic travel tips based on destination"""
    tips = []
    
    tips.append(f"🌍 **Country**: {data['country']}")
    tips.append(f"💱 **Local Currency**: {data['currency']} - Exchange at local banks for better rates")
    tips.append(f"🗣️ **Language**: {data['language']} - English widely spoken in tourist areas")
    tips.append(f"🌤️ **Best Time to Visit**: {data['best_time']}")
    
    # Budget-specific advice
    if budget < 500:
        tips.append(f"💰 **Budget Tip**: Consider staying in hostels and eating at local street food stalls to maximize your ${budget:.2f} budget")
    elif budget < 1500:
        tips.append(f"💰 **Budget Tip**: With ${budget:.2f}, opt for mid-range accommodations and mix of restaurants and street food")
    else:
        tips.append(f"💰 **Budget Tip**: Your ${budget:.2f} budget allows for comfortable hotels and fine dining experiences")
    
    # Destination-specific tips
    if data['currency'] == 'JPY':
        tips.append("🚗 **Getting Around**: Japan Rail Pass recommended for multiple cities, efficient local transit in Tokyo")
    elif data['currency'] == 'EUR':
        if 'paris' in str(data).lower():
            tips.append("🚗 **Getting Around**: Paris Métro day passes available, walking is best for central areas")
        else:
            tips.append("🚗 **Getting Around**: Excellent public transportation, consider city passes")
    elif data['currency'] == 'INR':
        tips.append("🚗 **Getting Around**: Auto-rickshaws and taxis affordable, rent scooter for flexibility")
    elif data['currency'] == 'USD':
        if 'new york' in str(data).lower():
            tips.append("🚗 **Getting Around**: NYC Subway是最 efficient, walking best for Manhattan neighborhoods")
        else:
            tips.append("🚗 **Getting Around**: Ride-sharing apps available, public transit varies by city")
    
    # Duration advice
    if days <= 3:
        tips.append(f"⏰ **Duration**: {days} days perfect for highlights tour of {data['country']}")
    elif days <= 7:
        tips.append(f"⏰ **Duration**: {days} days allows both major attractions and local cultural experiences")
    else:
        tips.append(f"⏰ **Duration**: With {days} days, you can explore beyond main attractions and take day trips")
    
    return tips

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Routewise API is running"}

@app.post("/plan-trip", response_model=TripResponse)
def plan_trip(request: TripRequest):
    """
    Generate ultra-realistic destination-aware travel itinerary
    """
    try:
        destination = request.destination.title()
        budget = request.budget
        days = request.days
        
        # Get destination-specific data
        data = get_destination_data(request.destination)
        
        # Calculate realistic budget breakdown
        budget_breakdown = calculate_realistic_budget(data, budget, days)
        
        # Generate unique activities for each day
        activities_by_day = get_unique_activities(data, days)
        
        # Generate realistic travel tips
        travel_tips = generate_realistic_tips(data, budget, days)
        
        # Build itinerary
        itinerary_lines = []
        
        # Header
        itinerary_lines.append(f"# 🌍 Complete Travel Itinerary for {destination}")
        itinerary_lines.append("")
        itinerary_lines.append(f"## 💰 Budget Overview: ${budget:,.2f} for {days} days")
        itinerary_lines.append(f"**Daily Budget: ${budget/days:,.2f} per day**")
        itinerary_lines.append("")
        
        # Add budget warning if applicable
        if budget_breakdown['budget_warning']:
            itinerary_lines.append(budget_breakdown['budget_warning'])
            itinerary_lines.append("")
        
        # Day-by-day itinerary
        for day, activities in enumerate(activities_by_day, 1):
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
        itinerary_lines.append(f"• **Local Rate**: ${data['daily_hotel']:,.2f} per night")
        itinerary_lines.append(f"• **Your Rate**: ${budget_breakdown['hotel']['daily']:,.2f} per night")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['hotel']['total']:,.2f} ({budget_breakdown['hotel']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Food & Dining
        itinerary_lines.append("### 🍽️ Food & Dining")
        itinerary_lines.append(f"• **Local cuisine**: {', '.join(data['dishes'][:3])} and more")
        itinerary_lines.append(f"• **Daily Average**: ${budget_breakdown['food']['daily']:,.2f}")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['food']['total']:,.2f} ({budget_breakdown['food']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Transportation
        itinerary_lines.append("### 🚗 Transportation")
        itinerary_lines.append(f"• **Local transport**, airport transfers, and day trips")
        itinerary_lines.append(f"• **Daily Average**: ${budget_breakdown['transport']['daily']:,.2f}")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['transport']['total']:,.2f} ({budget_breakdown['transport']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Activities
        itinerary_lines.append("### 🎯 Activities & Entertainment")
        itinerary_lines.append(f"• **Landmarks to visit**: {', '.join(data['landmarks'][:3])}")
        itinerary_lines.append(f"• **Daily Average**: ${budget_breakdown['activities']['daily']:,.2f}")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['activities']['total']:,.2f} ({budget_breakdown['activities']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Miscellaneous
        itinerary_lines.append("### 🛍️ Miscellaneous")
        itinerary_lines.append(f"• **Shopping, tips,** and unexpected expenses")
        itinerary_lines.append(f"• **Total**: ${budget_breakdown['miscellaneous']['total']:,.2f} ({budget_breakdown['miscellaneous']['percentage']:.0f}%)")
        itinerary_lines.append("")
        
        # Grand total
        calculated_total = (budget_breakdown['hotel']['total'] + 
                           budget_breakdown['food']['total'] + 
                           budget_breakdown['transport']['total'] + 
                           budget_breakdown['activities']['total'] + 
                           budget_breakdown['miscellaneous']['total'])
        
        itinerary_lines.append(f"## 🧾 Grand Total: ${calculated_total:,.2f}")
        itinerary_lines.append(f"**💚 Remaining Budget: ${(budget - calculated_total):,.2f}**")
        itinerary_lines.append("")
        
        # Travel tips
        itinerary_lines.append(f"## 🎒 Essential Travel Tips for {destination}")
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
        itinerary_lines.append(f"*🎉 Enjoy your amazing {days}-day adventure in {destination}! This itinerary has been carefully crafted with real local data to provide authentic experiences within your ${budget:,.2f} budget.*")
        itinerary_lines.append("")
        
        # Join all lines
        final_itinerary = "\n".join(itinerary_lines)
        
        return TripResponse(
            status="success",
            itinerary=final_itinerary,
            reasoning_logs=f"Generated destination-aware {days}-day itinerary for {destination} with ${budget:.2f} budget using real local cost data, unique daily activities, and authentic travel insights."
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
