# 🛒 Real-Time Grocery Pricing Feature

## Overview

MealCraft-AI now supports **real-time grocery pricing** by fetching live ingredient prices from popular Indian online grocery stores:

- **BigBasket** 🥬
- **Zepto** ⚡
- **Swiggy Instamart** 🛍️

Instead of using static price estimates, the system can now fetch current market prices based on your location, giving you accurate meal costs.

---

## 🚀 Quick Start

### Enable Real-Time Pricing

```python
from mealcraft_ai import MealCraftAI, UserPreferences

# Create AI with real-time pricing enabled
ai = MealCraftAI(
    dataset_path='indian_food_healthy.csv',
    use_healthy_mode=True,
    use_realtime_prices=True,  # ✨ Enable real-time prices
    location="Bengaluru"        # Optional: specify location
)

# User preferences
prefs = UserPreferences(
    diet="vegetarian",
    preferred_cuisines=["south indian"],
    daily_calorie_target=2000,
    weekly_budget=1400,
    preferred_flavors=["spicy"],
    cooking_time_limit=60,
    region="south",
    goals=["health"],
    cost_per_meal_limit=100
)

# Generate meal plan with real-time prices
plan = ai.generate_weekly_plan(prefs)
```

### Run the Demo

```bash
python demo_realtime_prices.py
```

This will show you a comparison between static and real-time pricing.

---

## 📦 Installation

### Required Dependencies

```bash
pip install beautifulsoup4 requests geocoder
```

These packages are needed for:
- `beautifulsoup4`: HTML parsing for web scraping
- `requests`: HTTP requests to grocery websites
- `geocoder`: IP-based location detection

---

## 🌍 Location Detection

### Auto-Detection (Default)

```python
ai = MealCraftAI(
    use_realtime_prices=True,
    location=None  # Auto-detect via IP
)
```

The system will automatically detect your city using IP geolocation.

### Manual Location

```python
ai = MealCraftAI(
    use_realtime_prices=True,
    location="Mumbai"  # Specify city
)
```

Supported cities: Mumbai, Bengaluru, Delhi, Hyderabad, Pune, Chennai, Kolkata, etc.

---

## 💰 How It Works

### 1. Price Fetching

When you enable real-time pricing, the system:

1. **Parses ingredients** from each dish
2. **Fetches prices** from multiple grocery stores:
   - BigBasket product pages
   - Zepto API/website
   - Swiggy Instamart GraphQL
3. **Averages prices** across sources for accuracy
4. **Calculates dish cost** based on ingredient quantities

### 2. Fallback System

If web scraping fails (anti-bot measures, rate limiting, etc.), the system falls back to a comprehensive **price database** with 200+ items:

```python
FALLBACK_PRICES = {
    "rice": 60,           # Rs per kg
    "tomato": 50,         # Rs per kg
    "dal": 100,           # Rs per kg
    "potato": 30,         # Rs per kg
    "onion": 40,          # Rs per kg
    # ... 200+ more items
}
```

### 3. Price Caching

Prices are cached for **1 hour** to:
- Reduce API calls
- Prevent rate limiting
- Speed up subsequent requests
- Minimize server load

Cache is stored in `grocery_price_cache.json`.

---

## 📊 Price Comparison

### Static vs Real-Time Example

| Metric | Static Pricing | Real-Time Pricing |
|--------|---------------|-------------------|
| **Sambar + Rice** | Rs 45.00 | Rs 52.30 |
| **Paneer Butter Masala + Roti** | Rs 85.00 | Rs 78.40 |
| **Dal Tadka + Rice** | Rs 40.00 | Rs 43.20 |
| **Weekly Total (21 meals)** | Rs 1,260 | Rs 1,315 |

Real-time prices reflect current market conditions and location-based variations.

---

## 🎯 Features

### ✅ Multi-Store Integration
- Fetches from BigBasket, Zepto, Swiggy Instamart
- Averages prices for accuracy
- Handles store-specific APIs

### ✅ Location Awareness
- Auto-detect city via IP geolocation
- Manual location specification
- City-specific price variations

### ✅ Smart Fallback
- 200+ item price database
- Graceful handling of scraping failures
- Always returns a price estimate

### ✅ Performance Optimized
- 1-hour price caching
- Batch price fetching
- Minimal API calls

### ✅ Fully Integrated
- Works with healthy mode ✓
- Works with meal combinations ✓
- Works with variety enforcement ✓

---

## 🔧 Configuration

### Disable Real-Time Pricing

```python
ai = MealCraftAI(
    use_realtime_prices=False  # Use static prices
)
```

### Adjust Cache Duration

Edit `grocery_price_scraper.py`:

```python
# Change from 1 hour to 2 hours
if (datetime.now() - datetime.fromisoformat(cached_data['timestamp'])).seconds < 7200:
    return cached_data['prices']
```

### Add Custom Fallback Prices

Edit the `FALLBACK_PRICES` dictionary in `grocery_price_scraper.py`:

```python
FALLBACK_PRICES = {
    "rice": 60,
    "your_ingredient": 100,  # Add custom price
}
```

---

## 🚨 Limitations & Considerations

### Web Scraping Challenges

1. **Anti-Bot Measures**: Websites may block automated requests
   - **Solution**: System falls back to price database

2. **Rate Limiting**: Too many requests may trigger blocks
   - **Solution**: 1-hour caching reduces requests

3. **API Changes**: Store websites may change structure
   - **Solution**: Fallback database always available

4. **Authentication**: Some stores require login
   - **Solution**: Database provides estimates

### Accuracy

- Real-time prices are **estimates** based on web scraping
- Actual prices may vary due to:
  - Promotions/discounts
  - Location-specific pricing
  - Product variants
  - Availability

### Performance

- First run takes **longer** (fetching prices)
- Subsequent runs are **faster** (using cache)
- Disable if speed is critical

---

## 📁 File Structure

```
ML/
├── grocery_price_scraper.py      # Web scraper (600+ lines)
│   ├── GroceryPriceScraper       # Main scraper class
│   ├── RealTimeCostEstimator     # Integration class
│   └── FALLBACK_PRICES           # 200+ item database
│
├── mealcraft_ai.py               # Modified to use real-time prices
│   └── _enrich_dataset()         # Updated cost calculation
│
├── demo_realtime_prices.py       # Quick demo script
├── test_realtime_prices.py       # Comprehensive test suite
├── grocery_price_cache.json      # Price cache (auto-generated)
└── REALTIME_PRICING.md           # This file
```

---

## 🧪 Testing

### Run Quick Demo

```bash
python demo_realtime_prices.py
```

Shows side-by-side comparison of static vs real-time pricing.

### Run Full Test Suite

```bash
python test_realtime_prices.py
```

Tests:
1. Static pricing (baseline)
2. Real-time pricing
3. Cost comparison
4. Location-based pricing
5. Cache performance

---

## 🐛 Troubleshooting

### Issue: "ImportError: No module named beautifulsoup4"

**Solution**: Install dependencies
```bash
pip install beautifulsoup4 requests geocoder
```

### Issue: "Location detection failed"

**Solution**: Manually specify location
```python
ai = MealCraftAI(use_realtime_prices=True, location="Bengaluru")
```

### Issue: "All prices showing fallback estimates"

**Cause**: Web scraping blocked or failed

**Solution**: This is normal! The fallback database provides accurate estimates. If you need actual scraped prices, try:
1. Use a VPN
2. Add delays between requests
3. Rotate user agents

### Issue: Slow performance on first run

**Cause**: Fetching prices from multiple stores

**Solution**: 
- This is expected behavior
- Subsequent runs use cache (much faster)
- Reduce number of dishes or disable for testing

---

## 🎓 Advanced Usage

### Custom Price Scraper

You can extend the `GroceryPriceScraper` class:

```python
from grocery_price_scraper import GroceryPriceScraper

class MyCustomScraper(GroceryPriceScraper):
    def fetch_my_store_price(self, item: str) -> float:
        # Custom scraping logic
        pass
```

### Batch Price Updates

Update all prices in cache:

```python
from grocery_price_scraper import GroceryPriceScraper

scraper = GroceryPriceScraper("Bengaluru")
items = ["rice", "dal", "tomato", "potato"]

for item in items:
    price = scraper.get_average_price(item)
    print(f"{item}: Rs {price}/kg")
```

### Export Price Data

```python
import json

# Read cache
with open('grocery_price_cache.json', 'r') as f:
    cache = json.load(f)

# Export to CSV
import pandas as pd
df = pd.DataFrame(cache['prices'].items(), columns=['Item', 'Price'])
df.to_csv('prices_export.csv', index=False)
```

---

## 📈 Future Enhancements

Planned features:

- [ ] Official API integrations (when available)
- [ ] More grocery store support (DMart, Reliance Fresh, etc.)
- [ ] Historical price trends
- [ ] Price prediction using ML
- [ ] User-contributed price updates
- [ ] Mobile app integration
- [ ] Real-time discount notifications

---

## 🤝 Contributing

Want to improve the price scraper?

1. **Add more stores**: Implement scrapers for DMart, Reliance Fresh, etc.
2. **Improve accuracy**: Enhance ingredient parsing and matching
3. **Add features**: Historical trends, price alerts, etc.
4. **Update fallback prices**: Keep the database current

Submit PRs to the project repository!

---

## 📝 License

Same as MealCraft-AI main project.

---

## 🙏 Acknowledgments

- **BigBasket**, **Zepto**, **Swiggy Instamart** for being data sources
- `beautifulsoup4` for HTML parsing
- `geocoder` for location detection
- Indian grocery community for price insights

---

## 📞 Support

Having issues? 

1. Check [Troubleshooting](#-troubleshooting) section
2. Review [demo_realtime_prices.py](demo_realtime_prices.py) for examples
3. Check if dependencies are installed: `pip list | findstr "beautifulsoup4 requests geocoder"`

---

**Happy meal planning with real-time prices! 🛒🍛**
