INTEGRATION GUIDE: Routewise Frontend-Backend Connection

================================================================================
STEP 1: BACKEND SETUP & VERIFICATION
================================================================================

1. Configure API Keys:
   - Open: backend/.env
   - Add your OpenRouter API Key: https://openrouter.ai
   - Add your Tavily API Key: https://tavily.com
   
   Example:
   OPENROUTER_API_KEY=sk-xxx...
   TAVILY_API_KEY=tvly-xxx...

2. Install Backend Dependencies:
   cd backend
   pip install -r requirements.txt

3. Start FastAPI Server:
   cd backend
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   
   Expected Output:
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete

4. Verify Backend Health:
   - Visit: http://127.0.0.1:8000/
   
   Expected Response:
   {
     "status": "healthy",
     "message": "Routewise API is running"
   }

5. View API Documentation:
   - Visit: http://127.0.0.1:8000/docs
   - You'll see interactive API documentation
   - Endpoints: /plan-trip (POST)

================================================================================
STEP 2: VERIFY CORS IS ENABLED
================================================================================

CORS Middleware has been added to main.py:
- Allows all origins (*)
- Allows all methods (GET, POST, etc.)
- Allows all headers

This enables frontend on localhost:3000 to communicate with backend on 0.0.0.0:8000

================================================================================
STEP 3: FRONTEND SETUP
================================================================================

1. Install Frontend Dependencies:
   cd frontend
   npm install axios
   
   (axios is imported in App.js for API calls)

2. Start React Development Server:
   cd frontend
   npm start
   
   Expected: App opens on http://localhost:3000

3. Frontend Configuration:
   - API endpoint: http://127.0.0.1:8000/plan-trip
   - Method: POST
   - Library: axios

================================================================================
STEP 4: TEST END-TO-END FLOW
================================================================================

TEST SCENARIO: Generate travel plan for Goa

1. Frontend Input:
   - Destination: Goa
   - Budget: 15000
   - Days: 3

2. Frontend Action:
   - Click "Plan Trip" button
   - Axios sends POST request to http://127.0.0.1:8000/plan-trip
   - Loading indicator shows "Planning Trip..."

3. Backend Processing:
   - Receives: { destination: "Goa", budget: 15000, days: 3 }
   - Creates CrewAI Task with ReAct workflow
   - Agent executes in sequence:
     a) Search CSV tool → Finds Goa destination data
     b) Search web tool → Fetches real-time info about Goa
     c) Calculate tool → Breaks down ₹15000 budget across 3 days
   - Generates comprehensive itinerary
   - Returns: { status: "success", itinerary: "...", reasoning_logs: "..." }

4. Frontend Display:
   - Displays generated itinerary in formatted card
   - Shows reasoning logs section below
   - Removes loading indicator

5. Verification Points:
   ✓ API call successful (no errors in console)
   ✓ Agent executed with all 3 tools
   ✓ Itinerary includes:
     - Day-wise plan (3 days)
     - Cost estimates (₹15000/3 days)
     - Attractions from CSV
     - Best time recommendations
   ✓ Response displayed in frontend

================================================================================
STEP 5: ERROR HANDLING VERIFICATION
================================================================================

Test Case 1: Backend Not Running
- Frontend: Shows error alert
- Console: Logs connection error

Test Case 2: Invalid Input
- Frontend: Shows validation message
- Backend: Not called

Test Case 3: Missing API Keys
- Backend: Returns error response
- Frontend: Displays error message from backend

================================================================================
INTEGRATION CHECKLIST
================================================================================

Backend:
 ✓ FastAPI server configured on port 8000
 ✓ CORS middleware enabled for all origins
 ✓ /plan-trip endpoint receives POST requests
 ✓ CrewAI Crew and Task properly configured
 ✓ Tools imported: search_csv, search_web, calculate_expression
 ✓ Error handling with try-except
 ✓ uvicorn startup configured
 ✓ .env file for API keys

Frontend:
 ✓ React App.js with useState hooks
 ✓ Input fields: destination, budget, days
 ✓ "Plan Trip" button
 ✓ axios POST request to correct endpoint
 ✓ JSON request format matches backend
 ✓ Response mapped to state: itinerary, reasoning_logs
 ✓ Loading state during API call
 ✓ Error handling with alerts
 ✓ Formatted display of itinerary and logs

Data:
 ✓ destinations.csv includes Goa
 ✓ CSV format matches tool expectations

================================================================================
TROUBLESHOOTING
================================================================================

Issue: "Backend not reachable" error
Solution:
1. Ensure Backend is running on port 8000
2. Check: http://127.0.0.1:8000/ is accessible
3. Verify no firewall blocking localhost:8000

Issue: "API key errors" 
Solution:
1. Check backend/.env has valid API keys
2. Restart backend server after updating .env
3. Verify keys grant necessary permissions

Issue: "Endpoint not found" error
Solution:
1. Verify backend/main.py has @app.post("/plan-trip")
2. Verify frontend URL matches: http://127.0.0.1:8000/plan-trip
3. Check request method is POST

Issue: CORS errors
Solution:
1. Verify CORSMiddleware is configured in main.py
2. Confirm allow_origins=["*"] is set
3. Restart backend server

Issue: Frontend shows "Planning..." indefinitely
Solution:
1. Check backend logs for errors
2. Verify API keys are valid
3. Check browser dev tools console for detailed errors

================================================================================
MONITORING AND DEBUGGING
================================================================================

Backend Logs:
- CrewAI verbose output shows:
  * Agent thinking process
  * Tool execution (Search CSV, Search web, Calculate)
  * Final itinerary generation

Frontend Logs (Browser Console):
- axios request details
- response data
- error messages

Testing with curl (alternative to frontend):
curl -X POST http://127.0.0.1:8000/plan-trip \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Goa",
    "budget": 15000,
    "days": 3
  }'

================================================================================
FULL STACK FLOW SUMMARY
================================================================================

User Input (Frontend)
        ↓
React State Updated
        ↓
axios.post() → http://127.0.0.1:8000/plan-trip
        ↓
FastAPI receives TripRequest
        ↓
CORS allows request
        ↓
CrewAI Agent Workflow:
  - Travel Planner Agent
  - Task with ReAct instructions
  - Tools: search_csv, search_web, calculate
        ↓
Agent Execution:
  1. Search CSV (Goa data)
  2. Search web (Real-time info)
  3. Calculate (Budget breakdown)
        ↓
Generates Itinerary
        ↓
Returns TripResponse
        ↓
Frontend receives response
        ↓
Updates state (itinerary, reasoning_logs)
        ↓
Displays formatted output
        ↓
User sees travel plan

================================================================================
STATUS: FULLY INTEGRATED AND READY FOR TESTING
================================================================================
