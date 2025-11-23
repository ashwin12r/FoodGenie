# MealCraft-AI Production Deployment Guide

## Project Structure (Production Ready)

```
ML/
├── mealcraft_ai.py              # Core ML system (979 lines)
├── mealcraft_cli.py             # Command-line interface (121 lines)
├── mealcraft_api.py             # FastAPI REST server (150 lines)
├── local_grocery_scraper.py     # Chennai grocery scraper - HTTP (548 lines)
├── selenium_grocery_scraper.py  # Chennai grocery scraper - Selenium (400 lines)
├── indian_food.csv              # Original dataset (800+ dishes)
├── indian_food_cleaned.csv      # Production dataset (used by system)
├── requirements.txt             # Python dependencies
├── README.md                    # User documentation
├── DEPLOYMENT.md                # This file
├── .venv/                       # Virtual environment
└── archive/                     # Old files, tests, debug scripts
```

---

## System Requirements

### Minimum
- Python 3.8+
- 2 GB RAM
- 500 MB disk space
- Windows/Linux/macOS

### Recommended
- Python 3.10+
- 4 GB RAM
- 1 GB disk space
- Chrome browser (for Selenium - optional)

---

## Installation Steps

### 1. Environment Setup

```bash
# Navigate to project
cd "c:\prime project\ML"

# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.venv\Scripts\activate.bat

# Activate (Linux/Mac)
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Verify installation
python -c "import pandas, sklearn, fastapi; print('✓ All packages installed')"
```

### 3. Verify Data Files

```bash
# Check dataset exists
ls indian_food_cleaned.csv

# Should show: indian_food_cleaned.csv (800+ dishes)
```

---

## Running the System

### Option 1: Command-Line Interface (Recommended for Users)

```bash
python mealcraft_cli.py
```

**Features:**
- Interactive menu
- Easy meal plan generation
- Export options (JSON/CSV)
- User-friendly output

### Option 2: REST API Server (Recommended for Integration)

```bash
python mealcraft_api.py
```

**Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/

**Production deployment:**
```bash
uvicorn mealcraft_api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Option 3: Python Import (Recommended for Developers)

```python
from mealcraft_ai import MealCraftAI

planner = MealCraftAI('indian_food_cleaned.csv')
plan = planner.generate_meal_plan(days=7, budget=1500)
planner.display_meal_plan(plan)
```

---

## Configuration

### Core Settings (mealcraft_ai.py)

```python
# Location for grocery pricing
location = "Chennai"  # Currently only Chennai supported

# Real-time pricing (optional)
use_realtime_prices = False  # True = Selenium scraping, False = fallback DB

# Fallback database
fallback_prices = {
    'rice': 60,
    'toor dal': 110,
    'tomato': 50,
    # ... 200+ items
}
```

### Scraper Settings

**local_grocery_scraper.py** (HTTP requests - faster):
- Grace Daily: Direct connection (no proxy)
- KPN Fresh: Direct connection
- Cache: 1 hour
- Timeout: 10 seconds

**selenium_grocery_scraper.py** (JavaScript rendering - comprehensive):
- Chrome headless mode
- 3-second wait for React/Next.js
- Supports: Grace Daily, KPN Fresh
- Cache: 1 hour

---

## Production Deployment

### Docker Deployment (Recommended)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mealcraft_ai.py mealcraft_api.py indian_food_cleaned.csv ./
COPY local_grocery_scraper.py selenium_grocery_scraper.py ./

CMD ["uvicorn", "mealcraft_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t mealcraft-ai .
docker run -p 8000:8000 mealcraft-ai
```

### Cloud Deployment

**AWS/GCP/Azure:**
```bash
# Using uvicorn with multiple workers
uvicorn mealcraft_api:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info
```

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn mealcraft_api:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

---

## Performance Optimization

### 1. Dataset Loading
```python
# Pre-load dataset at startup
planner = MealCraftAI('indian_food_cleaned.csv')
# Takes ~1 second, then cached in memory
```

### 2. Price Caching
```python
# Enable 1-hour cache (automatic)
# Cache file: chennai_grocery_cache.json
# Reduces scraping from 2-5 min to <1 ms
```

### 3. API Response Time
- First request: 2-5 seconds (dataset loading)
- Subsequent: <1 second (in-memory)
- With real-time scraping: +2-5 minutes (first hour only)

---

## Monitoring & Logging

### Enable Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mealcraft.log'),
        logging.StreamHandler()
    ]
)
```

### API Monitoring

```bash
# Health check endpoint
curl http://localhost:8000/

# Expected response:
{"status": "healthy", "version": "1.0"}
```

---

## Database Integration (Future)

Currently uses CSV files. For production at scale:

```python
# Option 1: SQLite
import sqlite3
conn = sqlite3.connect('mealcraft.db')

# Option 2: PostgreSQL
import psycopg2
conn = psycopg2.connect("dbname=mealcraft user=admin")

# Option 3: MongoDB
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
```

---

## Security Considerations

### 1. API Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/generate")
async def generate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "YOUR_API_KEY":
        raise HTTPException(status_code=401)
    # ... generate meal plan
```

### 2. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/generate")
@limiter.limit("10/minute")
async def generate():
    # ... generate meal plan
```

### 3. Input Validation

```python
from pydantic import BaseModel, validator

class MealPlanRequest(BaseModel):
    days: int
    budget: float
    
    @validator('days')
    def validate_days(cls, v):
        if v < 1 or v > 30:
            raise ValueError('Days must be between 1 and 30')
        return v
```

---

## Backup & Recovery

### 1. Data Backup

```bash
# Backup dataset
cp indian_food_cleaned.csv indian_food_cleaned.backup.csv

# Backup cache
cp chennai_grocery_cache.json chennai_grocery_cache.backup.json
```

### 2. Configuration Backup

```bash
# Create config file
cat > config.json << EOF
{
  "location": "Chennai",
  "use_realtime_prices": false,
  "cache_duration_hours": 1,
  "default_budget": 1500
}
EOF
```

---

## Troubleshooting

### Issue: Module not found
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Dataset not loading
```bash
# Verify file exists
ls -lh indian_food_cleaned.csv

# Check file format
head -5 indian_food_cleaned.csv
```

### Issue: Selenium errors
```bash
# Use fallback database instead
use_realtime_prices = False

# Or install ChromeDriver
# Windows: choco install chromedriver
# Mac: brew install chromedriver
# Linux: apt-get install chromium-chromedriver
```

### Issue: API not responding
```bash
# Check if port is in use
netstat -ano | findstr :8000

# Use different port
uvicorn mealcraft_api:app --port 8001
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Check API health endpoint
- Monitor error logs
- Review cache hit rate

**Weekly:**
- Update grocery prices (if using fallback)
- Clean old cache files
- Review API usage stats

**Monthly:**
- Update dataset (add new dishes)
- Update Python dependencies
- Review and optimize queries

### Update Commands

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Check for outdated packages
pip list --outdated

# Update specific package
pip install pandas --upgrade
```

---

## Support & Documentation

### Files
- `README.md` - User documentation
- `DEPLOYMENT.md` - This file
- API Docs - http://localhost:8000/docs

### Code Comments
All core files are well-commented with:
- Function docstrings
- Parameter descriptions
- Return value documentation
- Usage examples

---

## Production Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`requirements.txt`)
- [ ] Dataset file present (`indian_food_cleaned.csv`)
- [ ] System tested (CLI or API)
- [ ] Fallback database configured
- [ ] Logging enabled
- [ ] Health checks passing
- [ ] Performance acceptable (<5s response)
- [ ] Documentation reviewed

---

## Version History

### v1.0 (Production - November 2025)
- ✅ Core ML system complete
- ✅ CLI interface ready
- ✅ REST API functional
- ✅ Chennai grocery pricing (HTTP + Selenium)
- ✅ Fallback database (200+ items)
- ✅ 800+ dish dataset
- ✅ Complete documentation

---

**System Status:** Production Ready ✓  
**Last Updated:** November 2025  
**Maintainer:** MealCraft-AI Team
