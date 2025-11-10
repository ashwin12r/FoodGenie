# 🚀 MealCraft Quick Start Guide

## ✅ What We've Built

Your MealCraft application now has:

1. ✅ **Full Backend API** (`ML/backend_server.py`)
2. ✅ **Database Integration** (Neon PostgreSQL via `ML/database.py`)
3. ✅ **ML Meal Planner** (Connected to frontend)
4. ✅ **Grocery Price Scraping** (Grace Daily & KPN Fresh)
5. ✅ **Frontend Integration** (API client + integration scripts)

---

## 📁 New Files Created

### Backend Files (in `ML/` folder):
- `backend_server.py` - Main FastAPI server (470 lines)
- `database.py` - PostgreSQL database manager (400+ lines)
- `.env.example` - Configuration template

### Frontend Files (in `pages/` folder):
- `api-client.js` - JavaScript API wrapper
- `onboarding-integration.js` - **Onboarding → database connector**
- `meal-planner-integration.js` - Meal planner connector
- `smart-shopping-integration.js` - Shopping connector

### Documentation:
- `INTEGRATION_SETUP.md` - Complete setup instructions
- `ML/requirements.txt` - Updated with database dependencies

---

## 🎯 Quick Start (5 Steps)

### Step 1: Get Neon Database

1. Go to https://console.neon.tech/
2. Sign up (it's free!)
3. Create project named "mealcraft"
4. Copy your connection string

### Step 2: Configure Backend

```powershell
cd "c:\prime project\prime\ML"

# Create .env file
copy .env.example .env

# Edit .env and add your Neon connection string
notepad .env
```

**Add this line to `.env`:**
```
DATABASE_URL=postgresql://your-neon-connection-string-here
```

### Step 3: Install Dependencies

```powershell
# Install new Python packages
pip install psycopg2-binary python-dotenv
```

Or install everything:
```powershell
pip install -r requirements.txt
```

### Step 4: Initialize Database

```powershell
# Create all database tables
python database.py
```

**Expected output:**
```
✅ Database connection pool created successfully
✅ Database schema initialized successfully
✅ Database setup complete!
```

### Step 5: Start Everything

**Terminal 1 - Backend Server:**
```powershell
cd "c:\prime project\prime\ML"
python backend_server.py
```

**Terminal 2 - Frontend:**
```powershell
cd "c:\prime project\prime"
Start-Process index.html
```

---

## 🧪 Test the Integration

### Test 1: API Health Check

Open browser and visit:
```
http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "ml_model": "ready",
    "grocery_scraper": "ready"
  }
}
```

### Test 2: API Documentation

Visit the interactive API docs:
```
http://localhost:8000/docs
```

### Test 3: Generate Meal Plan

1. Open `pages/mealplanner.html` in browser
2. Open browser console (F12)
3. Run:
```javascript
await mealCraftAPI.generateMealPlan('test@example.com', {
    email: 'test@example.com',
    diet: 'Vegetarian',
    daily_calorie_target: 2000,
    weekly_budget: 1200,
    cooking_time_limit: 45,
    cost_per_meal_limit: 75
});
```

### Test 4: Get Grocery Prices

On `pages/smartshopping.html`, open console and run:
```javascript
await mealCraftAPI.getGroceryPrices();
```

---

## 🔗 How It Works

### Flow Diagram:

```
User fills form on Frontend
        ↓
JavaScript (api-client.js)
        ↓
POST http://localhost:8000/api/meal-plan/generate
        ↓
Backend Server (backend_server.py)
        ↓
ML System (mealcraft_ai.py)
        ↓
PostgreSQL Database
        ↓
Response back to Frontend
        ↓
Display meal plan to user
```

---

## 📊 Database Tables Created

1. **users** - User profiles
2. **user_preferences** - Dietary preferences
3. **meal_plans** - Generated meal plans
4. **shopping_lists** - Shopping lists from plans
5. **grocery_prices** - Scraped prices from stores

---

## 🛠️ Available API Endpoints

### User Management
- `POST /api/users/create` - Create user
- `GET /api/users/{email}` - Get user

### Preferences
- `POST /api/preferences/save` - Save preferences
- `GET /api/preferences/{email}` - Get preferences

### Meal Plans
- `POST /api/meal-plan/generate` - Generate AI meal plan ⭐
- `GET /api/meal-plan/{id}` - Get specific plan
- `GET /api/meal-plan/user/{email}` - Get user's plans

### Grocery Prices
- `GET /api/grocery/prices` - Get all prices ⭐
- `POST /api/grocery/scrape` - Scrape stores
- `GET /api/grocery/compare?item_name=tomato` - Compare prices

### Options
- `GET /api/options` - Get available diets, cuisines, etc.

---

## 🎨 Frontend Integration (Already Done!)

### Meal Planner Page (`mealplanner.html`):
- ✅ Added `api-client.js` script
- ✅ Added `meal-planner-integration.js` script
- ✅ Auto-loads meal plans on page load
- ✅ Generate button connects to AI backend

### Smart Shopping Page (`smartshopping.html`):
- ✅ Added `api-client.js` script
- ✅ Added `smart-shopping-integration.js` script
- ✅ Auto-loads grocery prices
- ✅ Price comparison functionality

**No HTML changes needed!** Only added `<script>` tags at the end.

---

## ⚠️ Troubleshooting

### Problem: "Connection refused"
**Solution:** Make sure backend server is running:
```powershell
cd "c:\prime project\prime\ML"
python backend_server.py
```

### Problem: "Database connection failed"
**Solution:** 
1. Check `.env` file has correct Neon connection string
2. Verify Neon project is not paused (check console.neon.tech)

### Problem: "ModuleNotFoundError"
**Solution:**
```powershell
pip install -r requirements.txt
```

### Problem: CORS errors
**Solution:** Already configured! Backend allows all origins in development.

---

## 📱 What Works Now

### ✅ Meal Planner:
- Generate AI-powered meal plans
- Save plans to database
- View previous meal plans
- Shopping list generation

### ✅ Smart Shopping:
- View grocery prices from database
- Scrape prices from Grace Daily & KPN Fresh
- Compare prices across stores
- Shopping list from meal plan

### ⏳ Recipe Discovery:
- Not connected yet (as requested)

---

## 🎉 You're All Set!

Your MealCraft app is now:
- ✅ Connected to AI backend
- ✅ Storing data in PostgreSQL
- ✅ Scraping real grocery prices
- ✅ Ready for testing

### Next Steps:
1. Get Neon connection string
2. Configure `.env` file
3. Run `python database.py`
4. Start `python backend_server.py`
5. Test meal planner and smart shopping pages

---

## 💡 Pro Tips

- Keep backend server running while using frontend
- Use Chrome DevTools (F12) to see API calls
- Check backend terminal for logs
- Visit `/docs` endpoint for API testing
- Database is automatically created on first run

---

**Need Help?** 
- Check `INTEGRATION_SETUP.md` for detailed setup
- Visit http://localhost:8000/docs for API documentation
- Check browser console (F12) for errors

**Happy Meal Planning! 🍽️✨**
