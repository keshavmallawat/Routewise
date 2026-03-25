# QUICK TEST GUIDE - Routewise Full Stack

## Prerequisites
- Python 3.9+ installed
- Node.js 14+ installed  
- API keys added to backend/.env

---

## STEP 1: Start Backend Server

```powershell
cd D:\Routewise\backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Started server process [XXXX]
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## STEP 2: Verify Backend Health

```powershell
curl http://127.0.0.1:8000/
```

**Expected Response:**
```json
{"status":"healthy","message":"Routewise API is running"}
```

---

## STEP 3: View API Documentation

Visit in browser:
```
http://127.0.0.1:8000/docs
```

You should see:
- POST /plan-trip endpoint
- Request schema with destination, budget, days
- Response schema with itinerary, reasoning_logs

---

## STEP 4: Test Backend with cURL

```powershell
$json = @{
    destination = "Goa"
    budget = 15000
    days = 3
} | ConvertTo-Json

curl -X POST http://127.0.0.1:8000/plan-trip `
  -H "Content-Type: application/json" `
  -d $json
```

**Expected Response:**
```json
{
  "status": "success",
  "itinerary": "Day 1-3: [Generated itinerary with Goa details...]",
  "reasoning_logs": "Reasoning logs are printed to the console."
}
```

---

## STEP 5: Install Frontend Dependencies

```powershell
cd D:\Routewise\frontend
npm install
```

---

## STEP 6: Start Frontend Server

```powershell
cd D:\Routewise\frontend
npm start
```

**Expected Output:**
```
Compiled successfully!
You can now view routewise in the browser at http://localhost:3000
```

Browser should open automatically.

---

## STEP 7: Test Full Stack in UI

### Input Values:
- **Destination:** Goa
- **Budget:** 15000
- **Days:** 3

### Steps:
1. Open http://localhost:3000 (should already be open)
2. Fill in Destination: "Goa"
3. Fill in Budget: "15000"
4. Fill in Days: "3"
5. Click "Plan Trip" button
6. Wait for response (should take 10-30 seconds)

### Expected Behavior:
- Button changes to "Planning Trip..." (disabled)
- Loading message shows: "Generating your personalized itinerary..."
- After response: Button returns to normal
- Itinerary card appears with travel plan
- Reasoning logs card appears below

### Expected Itinerary Content:
- Day 1, Day 2, Day 3 plans
- Cost estimates (₹15000 / 3 days = ₹5000/day)
- Goa attractions: Basilica of Bom Jesus, Fort Aguada, Anjuna Beach
- Best time: November-February

---

## STEP 8: Error Testing (Optional)

### Test 1: Empty Destination
- Leave destination blank
- Click "Plan Trip"
- **Expected:** Error message: "Please enter a destination"

### Test 2: Invalid Budget
- Enter Budget: "0"
- Click "Plan Trip"  
- **Expected:** Error message: "Please enter a valid budget"

### Test 3: Stop Backend, Send Request
- Stop backend server (Ctrl+C)
- Click "Plan Trip" with valid input
- **Expected:** Error alert: "Failed to plan trip. Please try again."

---

## DEBUGGING CHECKLIST

### Backend Not Running?
```powershell
# Check if port 8000 is in use
netstat -ano | Select-String "8000"

# Kill process on port 8000 (if needed)
Stop-Process -Id XXXX -Force

# Restart backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend Not Connecting?
1. Check backend is running on 127.0.0.1:8000
2. Open browser console (F12)
3. Look for any CORS or connection errors
4. Check axios endpoint URL matches: http://127.0.0.1:8000/plan-trip

### API Key Errors?
1. Check backend/.env has valid keys
2. Restart backend after updating .env
3. Check backend logs for API errors

### Frontend Still Shows "Planning..."?
1. Backend might be slow (first request can take 30+ seconds)
2. Check backend console for errors
3. Check browser console (F12) for axios errors

---

## VERIFICATION COMMANDS

### Verify CORS Enabled:
All endpoints should respond to preflight OPTIONS requests:
```powershell
curl -X OPTIONS http://127.0.0.1:8000/plan-trip `
  -H "Access-Control-Request-Method: POST" `
  -v
```

Should see headers like:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: *
```

### Verify Tools Are Loaded:
Check backend logs for tool initialization messages.

### Verify React Imports:
```powershell
Select-String -Path .\frontend\App.js "import React|import axios"
```

Should find both imports.

---

## EXPECTED API FLOW

1. **Frontend sends:** 
```json
POST /plan-trip
{
  "destination": "Goa",
  "budget": 15000,
  "days": 3
}
```

2. **Backend processes:**
   - Creates CrewAI Task
   - Initializes Crew with agent
   - Runs crew.kickoff()
   - Agent executes:
     - Search CSV → Finds Goa data
     - Search web → Fetches travel info
     - Calculate → Breaks down budget
   - Generates itinerary
   - Returns response

3. **Frontend displays:**
   - Itinerary in formatted card
   - Reasoning logs section
   - Map response to UI

---

## LOGS TO MONITOR

### Backend Console (should show):
```
Tool use: 'Search CSV' with args: "Goa"
Tool use: 'Search web' with args: "..."  
Tool use: 'Calculate' with args: "15000/3"
Final response: [Generated itinerary]
```

### Frontend Console (should show):
```
POST http://127.0.0.1:8000/plan-trip 200 OK
Response data: {status: 'success', itinerary: '...'}
```

### Errors to Watch For:
- CORS errors → Check middleware in main.py
- Connection refused → Backend not running
- 422 errors → Request JSON format incorrect
- API key errors → Invalid or missing keys in .env

---

## SUCCESS CRITERIA

✅ **Integration Complete When:**
- Backend starts without errors
- Frontend loads on localhost:3000
- Can input Destination, Budget, Days
- "Plan Trip" button works
- API request succeeds (no 5xx errors)
- Response displays itinerary
- No CORS errors in console
- All 3 tools execute in backend
- Itinerary includes formatted output

✅ **Test Passes When:**
- Input: Goa, 15000, 3
- Output: Multi-day itinerary with costs and attractions
- No errors in frontend or backend

---

## QUICK RESTART

**Terminal 1 (Backend):**
```powershell
cd D:\Routewise\backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 (Frontend):**
```powershell
cd D:\Routewise\frontend  
npm start
```

Both should run simultaneously. Open http://localhost:3000 when ready.

---

## PERFORMANCE NOTES

- Initial request: 20-40 seconds (LLM thinking + web search)
- Subsequent requests: Faster (if API credentials cached)
- Browser console shows network timing
- Backend console shows agent thinking process

---

**Ready to Test!** 🚀
