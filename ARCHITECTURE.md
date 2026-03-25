# ROUTEWISE FULL STACK ARCHITECTURE & INTEGRATION

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ROUTEWISE SYSTEM                             │
└─────────────────────────────────────────────────────────────────────┘

                              PORT 3000
                                 │
                    ┌────────────────────────┐
                    │   REACT FRONTEND       │
                    │   (localhost:3000)     │
                    │                        │
                    │  • Input Form          │
                    │  • Axios HTTP Client   │
                    │  • Result Display      │
                    │  • Error Handling      │
                    └────────────────────────┘
                              │
                              │
                    ← CORS Enabled →  (All Origins)
                              │
         ┌────────────────────────────────────────┐
         │  HTTP POST                              │
         │  /plan-trip                             │
         │  JSON: {destination, budget, days}     │
         └────────────────────────────────────────┘
                              │
                              ↓
                        PORT 8000
              ┌──────────────────────────────┐
              │    FASTAPI BACKEND           │
              │    (0.0.0.0:8000)            │
              │                              │
              │  • CORS Middleware           │
              │  • Route: POST /plan-trip     │
              │  • Pydantic Models           │
              │  • Error Handling            │
              └──────────────────────────────┘
                              │
                              ↓
              ┌──────────────────────────────┐
              │    CREWAI AGENT WORKFLOW     │
              │                              │
              │  1. Create Task              │
              │  2. Initialize Crew          │
              │  3. Execute Agent            │
              │     └─ ReAct Logic           │
              └──────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ↓                    ↓                    ↓
  ┌────────────┐      ┌────────────┐      ┌────────────┐
  │ Tool 1:    │      │ Tool 2:    │      │ Tool 3:    │
  │ Search CSV │      │ Search Web │      │Calculate   │
  │            │      │            │      │            │
  │ pandas     │      │ Tavily API │      │ numexpr    │
  │ CSV File   │      │ Real-time  │      │ Math       │
  │ locations  │      │ Travel     │      │ Budget     │
  │ & costs    │      │ Data       │      │ Breakdown  │
  └────────────┘      └────────────┘      └────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ↓
              ┌──────────────────────────────┐
              │  GENERATED ITINERARY         │
              │  {status, itinerary, logs}   │
              └──────────────────────────────┘
                              │
                              ↓
         ┌────────────────────────────────────────┐
         │  HTTP 200 Response                      │
         │  JSON: {itinerary, reasoning_logs}     │
         └────────────────────────────────────────┘
                              │
                              ↓
                    ┌────────────────────────┐
                    │   FRONTEND DISPLAY     │
                    │                        │
                    │  • Clear Loading       │
                    │  • Show Itinerary      │
                    │  • Show Logs           │
                    │  • Handle Errors       │
                    └────────────────────────┘
```

---

## Component Integration Summary

### Frontend Layer (React)
**Location:** `frontend/App.js`
- React hooks for state management (useState)
- Input validation
- Axios for HTTP requests
- Error handling with try-catch
- UI rendering with conditional display

**State Variables:**
```javascript
destination  - Destination input
budget      - Budget input (number)
days        - Days input (number)
itinerary   - API response itinerary
reasoning_logs - API response logs
loading     - Request in progress
error       - Error messages
```

**API Call:**
```javascript
axios.post('http://127.0.0.1:8000/plan-trip', {
  destination: string,
  budget: number,
  days: number
})
```

---

### Backend Layer (FastAPI)
**Location:** `backend/main.py`

**Key Components:**
1. **CORS Middleware:**
   - Allows all origins (*)
   - Allows all methods (GET, POST, etc.)
   - Allows all headers

2. **Pydantic Models:**
   - TripRequest: destination (str), budget (float), days (int)
   - TripResponse: status (str), itinerary (str), reasoning_logs (Optional[str])

3. **Endpoints:**
   - GET / → Health check
   - POST /plan-trip → Main workflow

4. **Error Handling:**
   - Try-except block
   - Returns error response on failure

---

### Agent Layer (CrewAI)
**Location:** `backend/agent_core.py`

**Agent Configuration:**
- Role: "Expert Travel Planner"
- Goal: Create optimized travel itineraries
- Backstory: Experienced world traveler
- Tools: [search_web, calculate_expression, search_csv]
- LLM: OpenAI (via OpenRouter) - gpt-4o-mini
- Verbose: True (logs visible)

**Agent Capabilities:**
- Reasoning through multiple data sources
- Tool selection and execution
- Structured output generation

---

### Tools Layer
**Location:** `backend/tools.py`

**Tool 1: search_csv**
- Input: city name (string)
- Action: Query destinations.csv
- Output: City data (attractions, cost, best season)
- Framework: pandas

**Tool 2: search_web**
- Input: search query (string)
- Action: Query Tavily API for real-time info
- Output: Web search results
- Framework: Tavily API

**Tool 3: calculate_expression**
- Input: math expression (string)
- Action: Evaluate budget calculations
- Output: Numeric result
- Framework: numexpr (safe evaluation)

---

### Data Layer
**Location:** `data/destinations.csv`

**Structure:**
```
City,Attractions,AverageCost,BestSeason
Goa,"Basilica of Bom Jesus, Fort Aguada, Anjuna Beach",5000,November-February
```

**Fields:**
- City: Destination name (searchable)
- Attractions: Key places (included in itinerary)
- AverageCost: Baseline cost per day
- BestSeason: Travel recommendation

---

## Request-Response Flow

### REQUEST FLOW:

1. **Frontend validation** (App.js)
   - Check destination non-empty
   - Check budget > 0
   - Check days > 0

2. **axios.post() call**
   ```
   POST http://127.0.0.1:8000/plan-trip
   Content-Type: application/json
   {
     "destination": "Goa",
     "budget": 15000,
     "days": 3
   }
   ```

3. **CORS preflight** (if needed)
   - Browser sends OPTIONS request
   - Server responds with CORS headers
   - Browser allows actual POST

4. **FastAPI receives**
   - Pydantic validates JSON
   - Routes to /plan-trip endpoint
   - Creates TripRequest object

### PROCESSING FLOW:

1. **Task Creation** (main.py)
   - Format: Task with ReAct instructions
   - Include: destination, budget, days details

2. **Crew Initialization** (main.py)
   - Agent: travel_planner_agent
   - Task: travel_task
   - Verbose: True

3. **Agent Execution** (agent_core.py)
   - Load LLM (OpenAI via OpenRouter)
   - Process task description
   - Plan tool sequence

4. **Tool Execution Sequence:**
   ```
   Step 1: Search CSV tool
           Query: "Goa"
           Return: {City: Goa, Attractions: [...], Cost: 5000, Season: Nov-Feb}
   
   Step 2: Search web tool
           Query: "Goa travel weather events 2026"
           Return: Real-time travel info (curated by Tavily)
   
   Step 3: Calculate tool
           Query: "15000 / 3"  (or more complex budget breakdown)
           Return: 5000/day, 15000 total
   ```

5. **Itinerary Generation**
   - Combine tool outputs
   - Structure as day-wise plan
   - Format with costs, attractions, recommendations
   - Return as string

### RESPONSE FLOW:

1. **Backend returns**
   ```json
   {
     "status": "success",
     "itinerary": "Day 1-3: [Generated plan]",
     "reasoning_logs": "Reasoning logs are printed to the console."
   }
   ```

2. **Frontend receives**
   - axios intercepts response
   - Maps to state: itinerary, reasoning_logs

3. **Frontend displays**
   - Clear loading state
   - Show itinerary card
   - Show reasoning logs section
   - Update UI

---

## Integration Points Checklist

```
✓ Frontend → Backend (HTTP POST)
✓ CORS Enabled (Browser → Server)
✓ Request Format (JSON match)
✓ Response Format (JSON match)
✓ Agent Tools (All 3 integrated)
✓ Error Handling (Try-catch + Alerts)
✓ State Management (React hooks)
✓ API Contract (Matching models)
✓ Data Persistence (CSV + search)
✓ Real-time Data (Tavily API)
✓ Calculations (Budget math)
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React (js) | User interface |
| **HTTP Client** | axios | API communication |
| **Backend** | FastAPI | REST API server |
| **Server** | uvicorn | ASGI server |
| **Agent** | CrewAI | Agentic workflow |
| **LLM** | OpenAI (OpenRouter) | Language model |
| **Web Search** | Tavily API | Real-time data |
| **Data** | pandas | CSV processing |
| **Calculation** | numexpr | Safe math eval |
| **Config** | python-dotenv | API keys (.env) |

---

## Environment Variables Required

**File:** `backend/.env`

```
OPENROUTER_API_KEY=<your_key>    # LLM access
TAVILY_API_KEY=<your_key>         # Web search access
```

---

## File Structure

```
Routewise/
├── backend/
│   ├── main.py                 # FastAPI + CORS + Endpoints
│   ├── agent_core.py           # CrewAI Agent setup
│   ├── tools.py                # Tool implementations
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # API keys
├── frontend/
│   └── App.js                  # React component main
├── data/
│   └── destinations.csv        # Travel data
├── INTEGRATION_GUIDE.md        # Setup instructions
├── INTEGRATION_CHECKLIST.md    # Verification checklist
└── QUICK_TEST_GUIDE.md         # Testing steps
```

---

## Success Metrics

### Backend
- ✓ Starts without errors
- ✓ Health endpoint responds
- ✓ /plan-trip accepts POST
- ✓ CrewAI executes
- ✓ Tools execute
- ✓ Returns valid JSON

### Frontend
- ✓ Loads on localhost:3000
- ✓ Form validates input
- ✓ Sends axios request
- ✓ Receives response
- ✓ Displays itinerary
- ✓ Shows error alerts

### Integration
- ✓ No CORS errors
- ✓ Request format matches
- ✓ Response format matches
- ✓ Full flow works end-to-end
- ✓ Data displayed correctly
- ✓ Errors handled gracefully

---

## Next Steps After Integration

1. Add error boundary to React (error fallback UI)
2. Add loading spinners instead of text
3. Add timeout handling for long requests
4. Implement response caching
5. Add user feedback/ratings
6. Integrate real frontend framework (if needed)
7. Add unit tests for tools
8. Add API documentation (Swagger)
9. Add logging and monitoring
10. Deploy to production (cloud)

---

**Current Status: ✅ FULLY INTEGRATED & READY FOR TESTING**
