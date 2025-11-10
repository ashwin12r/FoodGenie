# MealCraft Integration Setup Guide

## 🎯 Overview

This guide explains how to connect your MealCraft frontend with the ML-powered backend.

---

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Neon PostgreSQL** account (free tier available)
3. **Node.js** (for frontend)
4. **Git** (optional)

---

## 🚀 Step-by-Step Setup

### 1. Set Up Neon PostgreSQL Database

1. **Create Account:**
   - Go to [https://console.neon.tech/](https://console.neon.tech/)
   - Sign up for free account

2. **Create Database:**
   - Click "New Project"
   - Name: `mealcraft`
   - Region: Choose closest to you
   - Click "Create Project"

3. **Get Connection String:**
   - In your project dashboard, click "Connection Details"
   - Copy the connection string
   - It looks like:
     ```
     postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/mealcraft?sslmode=require
     ```

### 2. Configure Backend

1. **Navigate to ML folder:**
   ```powershell
   cd "c:\prime project\prime\ML"
   ```

2. **Create `.env` file:**
   ```powershell
   copy .env.example .env
   ```

3. **Edit `.env` file:**
   - Open `.env` in notepad or VS Code
   - Replace `DATABASE_URL` with your Neon connection string:
     ```
     DATABASE_URL=postgresql://your-actual-connection-string-here
     ```

### 3. Install Python Dependencies

```powershell
cd "c:\prime project\prime\ML"

# Install all required packages
pip install -r requirements.txt
```

**Expected packages:**
- psycopg2-binary (PostgreSQL adapter)
- fastapi (API framework)
- uvicorn (ASGI server)
- pandas, numpy, scikit-learn (ML)
- beautifulsoup4, requests (web scraping)

### 4. Initialize Database

```powershell
# Run database initialization
python database.py
```

**Expected output:**
```
✅ Database connection pool created successfully
✅ Database schema initialized successfully
✅ Database setup complete!
```

### 5. Test ML System

```powershell
# Verify ML system works
python quickstart.py
```

**Expected output:**
```
✓ All dependencies installed
✓ Meal plan generated (7 days, ₹551.49)
✓ Export successful
✅ ALL TESTS PASSED - SYSTEM READY!
```

### 6. Start Backend Server

```powershell
# Start the API server
python backend_server.py
```

**Expected output:**
```
🚀 Starting MealCraft Backend Server...
📊 Database: Neon PostgreSQL
🤖 ML Model: MealCraft-AI
🛒 Scraper: Chennai Local Stores

🌐 Server will run on: http://localhost:8000
📖 API Docs: http://localhost:8000/docs

INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!** The server needs to run while using the frontend.

### 7. Test API Endpoints

Open browser and visit:
- **API Health:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs (Interactive Swagger UI)

### 8. Open Frontend

In a **NEW terminal** window:

```powershell
cd "c:\prime project\prime"

# Open the frontend
Start-Process index.html
```

Or use a local server:
```powershell
python -m http.server 3000
# Then visit: http://localhost:3000
```

---

## 🔗 How the Integration Works

### Architecture Flow:

```
Frontend (HTML/JS)
    ↓
API Client (api-client.js)
    ↓
Backend API (backend_server.py) - Port 8000
    ↓
ML System (mealcraft_ai.py)
    ↓
Neon PostgreSQL Database
```

### Key Connections:

1. **Onboarding Page** → Saves user preferences to database
2. **Meal Planner Page** → Generates AI meal plans via API
3. **Smart Shopping Page** → Fetches real-time grocery prices

---

## 📡 API Endpoints Available

### User Management
- `POST /api/users/create` - Create user
- `GET /api/users/{email}` - Get user info

### Preferences
- `POST /api/preferences/save` - Save preferences
- `GET /api/preferences/{email}` - Get preferences

### Meal Plans
- `POST /api/meal-plan/generate` - Generate AI meal plan
- `GET /api/meal-plan/{id}` - Get specific plan
- `GET /api/meal-plan/user/{email}` - Get user's plans

### Grocery Prices
- `GET /api/grocery/prices` - Get all prices
- `POST /api/grocery/scrape` - Trigger web scraping
- `GET /api/grocery/compare?item_name=tomato` - Compare prices

### Options
- `GET /api/options` - Get available diets, cuisines, etc.

---

## 🧪 Testing the Integration

### Test 1: Health Check
```javascript
// Open browser console on any page
fetch('http://localhost:8000/health')
    .then(r => r.json())
    .then(console.log);
```

### Test 2: Generate Meal Plan
```javascript
fetch('http://localhost:8000/api/meal-plan/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        email: 'test@example.com',
        preferences: {
            email: 'test@example.com',
            diet: 'Vegetarian',
            daily_calorie_target: 2000,
            weekly_budget: 1200,
            cooking_time_limit: 45,
            cost_per_meal_limit: 75
        }
    })
})
.then(r => r.json())
.then(console.log);
```

### Test 3: Get Grocery Prices
```javascript
fetch('http://localhost:8000/api/grocery/prices')
    .then(r => r.json())
    .then(console.log);
```

---

## ⚠️ Troubleshooting

### Issue: "Connection refused" or "CORS error"

**Solution:**
1. Make sure backend server is running: `python backend_server.py`
2. Check if port 8000 is accessible: http://localhost:8000/health
3. Try restarting the server

### Issue: "Database connection failed"

**Solution:**
1. Verify `.env` file has correct Neon connection string
2. Check if Neon project is active (not paused)
3. Test connection: `python database.py`

### Issue: "ML system unavailable"

**Solution:**
1. Check if `indian_food_cleaned.csv` exists in ML folder
2. Verify all dependencies installed: `pip install -r requirements.txt`
3. Test ML: `python quickstart.py`

### Issue: "Import errors"

**Solution:**
```powershell
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

---

## 🎯 Next Steps

1. ✅ **Complete onboarding** - Test user preference saving
2. ✅ **Generate meal plan** - Test AI meal generation
3. ✅ **View shopping list** - Test grocery price fetching
4. 🔄 **Iterate** - Customize as needed

---

## 📱 Production Deployment (Future)

For deploying to production:

1. **Backend:** Deploy to Heroku/AWS/DigitalOcean
2. **Frontend:** Deploy to Netlify/Vercel/GitHub Pages
3. **Database:** Already on Neon (production-ready)
4. **Update CORS:** Set specific frontend domain in `.env`

See `DEPLOYMENT.md` for detailed production guide.

---

## 🆘 Support

If you encounter issues:
1. Check console logs (browser & terminal)
2. Review API docs: http://localhost:8000/docs
3. Test endpoints individually
4. Verify database connection

---

**🎉 You're all set!** Your MealCraft app is now powered by AI and real-time data!
