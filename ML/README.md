# MealCraft-AI 🍽️# 🍽️ MealCraft-AI: Intelligent Indian Meal Planning System



**AI-Powered Meal Planning System with Real-Time Chennai Grocery Pricing****Version:** 1.0.0  

**Author:** AI-Powered Meal Planning  

Generate personalized, healthy, budget-friendly meal plans using machine learning and live grocery prices from Chennai stores.**License:** MIT



------



## 🌟 Features## 📖 Overview



- ✅ **AI-Powered Meal Planning**: ML-driven dish selection and combinations**MealCraft-AI** is a deterministic machine learning-powered meal planning system specifically designed for Indian cuisine. It generates personalized 7-day meal plans optimized for:

- ✅ **Health-Focused**: Nutritional analysis (calories, protein, carbs, fat, fiber)

- ✅ **Budget-Aware**: Real-time Chennai grocery pricing + fallback database- ✅ Dietary preferences (Vegetarian, Non-Veg, Vegan, Jain, Keto, Gluten-Free, etc.)

- ✅ **100% Variety**: No repeated dishes in meal plans- ✅ Budget constraints

- ✅ **Smart Combinations**: Breakfast/Lunch/Dinner optimization- ✅ Nutritional goals (weight loss, muscle gain, energy, immunity)

- ✅ **Export Ready**: JSON/CSV meal plans with grocery lists- ✅ Regional cuisine preferences

- ✅ **REST API**: FastAPI server for integration- ✅ Cooking time limitations

- ✅ Ingredient reuse & cost efficiency

---

---

## 📦 Installation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+### Installation

- Virtual environment (recommended)

- Chrome browser (for Selenium scraping - optional)```bash

# Clone or download the project

### Quick Setupcd "c:\prime project\ML"



```bash# Install dependencies

# Navigate to projectpip install -r requirements.txt

cd "c:\prime project\ML"```



# Create virtual environment### Basic Usage

python -m venv .venv

#### 1. Command-Line Interface (Recommended for beginners)

# Activate virtual environment

.\.venv\Scripts\Activate.ps1```bash

python mealcraft_cli.py

# Install dependencies```

pip install -r requirements.txt

```Follow the interactive prompts to generate your meal plan.



---#### 2. Python Script



## 🚀 Quick Start```python

from mealcraft_ai import MealCraftAI, UserPreferences

### 1. Command Line Interface

# Initialize AI

```bashai = MealCraftAI("indian_food.csv")

python mealcraft_cli.py

```# Define preferences

user_prefs = UserPreferences(

### 2. Python API    diet="Vegetarian",

    preferred_cuisines=["North Indian"],

```python    daily_calorie_target=2000,

from mealcraft_ai import MealCraftAI    weekly_budget=1200,

    preferred_flavors=["spicy", "mild"],

meal_planner = MealCraftAI(    cooking_time_limit=45,

    data_path='indian_food_cleaned.csv',    region="North",

    location='Chennai'    goals=["weight loss", "energy"],

)    cost_per_meal_limit=75

)

meal_plan = meal_planner.generate_meal_plan(

    days=7,# Generate meal plan

    budget=1500,meal_plan = ai.generate_weekly_plan(user_prefs)

    diet='vegetarian',

    cuisine='south indian'# Display results

)import json

print(json.dumps(meal_plan, indent=2))

meal_planner.display_meal_plan(meal_plan)```

```

#### 3. REST API Server

### 3. REST API Server

```bash

```bash# Start API server

python mealcraft_api.pypython mealcraft_api.py

```

# Server runs on http://localhost:5000

API Documentation: http://localhost:8000/docs```



---API Endpoints:

- `POST /api/generate-meal-plan` - Generate meal plan

## 📁 Project Structure- `GET /api/available-options` - Get diet/region options

- `GET /api/dishes` - Search dishes

```- `POST /api/nutrition-estimate` - Estimate nutrition

ML/- `GET /health` - Health check

├── mealcraft_ai.py              # Main ML system

├── mealcraft_cli.py             # CLI interface---

├── mealcraft_api.py             # REST API

├── local_grocery_scraper.py     # Chennai scraper (HTTP)## 🎯 Input Parameters

├── selenium_grocery_scraper.py  # Chennai scraper (Selenium)

├── indian_food_cleaned.csv      # 800+ dishes dataset### Required Fields

├── requirements.txt             # Dependencies

└── README.md                    # This file| Parameter | Type | Description | Example |

```|-----------|------|-------------|---------|

| `diet` | string | Dietary preference | "Vegetarian" |

---| `daily_calorie_target` | int | Target daily calories | 2000 |

| `weekly_budget` | float | Weekly food budget (INR) | 1200 |

## 🎯 Sample Output| `cooking_time_limit` | int | Max cooking time (minutes) | 45 |

| `cost_per_meal_limit` | float | Max cost per meal (INR) | 75 |

```

╔═══════════════════════════════════════════════════════╗### Optional Fields

║         MEALCRAFT-AI: 7-DAY MEAL PLAN                 ║

╠═══════════════════════════════════════════════════════╣| Parameter | Type | Description | Example |

║ Budget: Rs 1500 | Spent: Rs 565.68                   ║|-----------|------|-------------|---------|

║ Diet: vegetarian | Cuisine: south indian             ║| `preferred_cuisines` | list | Cuisine preferences | ["North Indian", "South Indian"] |

╚═══════════════════════════════════════════════════════╝| `preferred_flavors` | list | Flavor preferences | ["spicy", "mild"] |

| `region` | string | Regional preference | "North" |

DAY 1| `goals` | list | Health goals | ["weight loss", "energy"] |

🌅 BREAKFAST: Idli (Rs 32.30 | 150 kcal)

🌞 LUNCH: Sambar (Rs 60.80 | 180 kcal)### Supported Options

🌙 DINNER: Curd Rice (Rs 56.50 | 200 kcal)

**Diet Types:**

Total: 21 meals | Rs 565.68 | 2268 kcal/day avg- Vegetarian

Status: Rs 934.32 UNDER BUDGET ✓- Non-Vegetarian

```- Vegan

- Jain

---- Gluten-Free

- Keto

## 🏪 Chennai Grocery Pricing- High-Protein

- Low-Carb

### Supported Stores

- Grace Daily (gracedaily.com)**Regions:**

- KPN Fresh (kpnfresh.com)- North

- South

### Fallback Database- East

200+ Chennai grocery items with realistic prices:- West

- Rice: Rs 60/kg- North East

- Toor Dal: Rs 110/kg- Central

- Tomato: Rs 50/kg- All

- Onion: Rs 40/kg

**Flavors:**

---- spicy

- mild

## 📊 Dataset- sweet

- sour

**File:** `indian_food_cleaned.csv`- bitter



- 800+ Indian dishes**Goals:**

- Nutritional data (calories, protein, carbs, fat, fiber)- weight loss

- Cooking time & difficulty- muscle gain

- Ingredient lists- energy

- Multiple cuisines (South Indian, North Indian, Bengali, etc.)- immunity

- maintenance

---

---

## 🔧 Configuration

## 📊 Output Format

### Enable Real-Time Scraping (Optional)

### JSON Structure

```python

planner = MealCraftAI(```json

    data_path='indian_food_cleaned.csv',{

    use_realtime_prices=True  # Enable Selenium  "weekly_plan": [

)    {

```      "day": "Monday",

      "meals": {

**Note:** Uses fallback database by default (instant, reliable).        "breakfast": {

          "dish": "Poha",

---          "time": "30 min",

          "calories": "350 kcal",

## 📝 API Reference          "protein": "8.5g",

          "carbs": "55.2g",

### REST API Endpoints          "fat": "8.1g",

          "cost": "₹45.50",

| Method | Endpoint | Description |          "reason": "budget-friendly, quick to prepare"

|--------|----------|-------------|        },

| GET | `/` | Health check |        "lunch": { ... },

| POST | `/generate` | Generate meal plan |        "dinner": { ... }

| GET | `/nutrition` | Nutrition analysis |      }

| GET | `/groceries` | Grocery list |    },

    ...

### Python API  ],

  "summary": {

```python    "total_cost": "₹1150.25",

MealCraftAI(data_path, location='Chennai', use_realtime_prices=False)    "avg_cost_per_meal": "₹54.77",

generate_meal_plan(days, budget, diet, cuisine, max_calories, min_protein)    "weekly_budget": "₹1200",

display_meal_plan(meal_plan)    "budget_status": "optimal",

export_meal_plan(meal_plan, filename)    "calorie_balance_accuracy": "94.5%",

```    "daily_avg_calories": 1980,

    "daily_avg_protein": "65.2g",

---    "ingredient_overlap_score": "38.5%"

  },

## 🛠️ Troubleshooting  "shopping_list": {

    "potato": 8,

### Import errors    "tomato": 12,

```bash    "onion": 10,

pip install -r requirements.txt --upgrade    ...

```  },

  "batch_cooking_suggestions": [

### Selenium issues    "Batch prep dal - used on days Monday, Wednesday, Friday",

Use fallback database: `use_realtime_prices=False` (default)    ...

  ],

### Empty meal plans  "nutrition_summary": { ... }

Increase budget: `budget=2000` or relax filters: `diet=None`}

```

---

---

## 📈 Performance

## 🧠 How It Works

- Dataset Loading: ~1 second

- Meal Plan Generation: 2-5 seconds  ### Step-by-Step Algorithm

- Real-Time Scraping: 2-5 minutes (first run, cached for 1 hour)

- Fallback Database: Instant (<1 ms)1. **Filter Dataset**

   - Match dietary restrictions (strict)

---   - Apply regional preferences (soft)

   - Filter by cooking time constraints

## 📞 Support

2. **Enrich Data**

1. Check troubleshooting section   - Estimate nutritional values from ingredients

2. Review API documentation at `/docs`   - Calculate cost based on ingredient complexity

3. Test with fallback database first   - Add time complexity factors



---3. **Score Meals**

   - Cost optimization (30% weight)

**Version:** 1.0 Production Ready     - Time efficiency (20% weight)

**Last Updated:** November 2025     - Nutritional match (25% weight)

**Location:** Chennai, India   - Flavor preferences (10% weight)

   - Protein bonuses for specific goals
   - Ingredient reuse bonuses

4. **Build Weekly Plan**
   - Select highest-scoring meals
   - Avoid repetitions
   - Maximize ingredient overlap
   - Balance daily nutrition

5. **Validate & Rebalance**
   - Check budget constraints
   - Verify calorie targets (±15% tolerance)
   - Adjust if necessary

6. **Generate Outputs**
   - Shopping list
   - Batch cooking suggestions
   - Nutrition reports

---

## 📁 Project Structure

```
ML/
├── indian_food.csv              # Dataset (256 Indian dishes)
├── mealcraft_ai.py              # Core AI system
├── mealcraft_cli.py             # Interactive CLI
├── mealcraft_api.py             # REST API server
├── mealcraft_demo.ipynb         # Jupyter demo notebook
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── examples/
    ├── example_vegetarian.json
    ├── example_nonveg.json
    └── example_vegan.json
```

---

## 🔬 Technical Details

### Nutrition Estimation

The system uses a comprehensive ingredient-to-nutrition mapping database covering:
- 50+ common Indian ingredients
- Macronutrient profiles (protein, carbs, fat)
- Calorie estimations
- Portion size adjustments by course type

### Cost Estimation

Cost calculation factors:
- Ingredient base costs (market rates)
- Cooking complexity premium
- Preparation time overhead
- Ingredient count scaling

### Scoring Algorithm

Composite scoring formula:
```
score = (cost_score × 0.30) + 
        (time_score × 0.20) + 
        (nutrition_score × 0.25) + 
        (flavor_score × 0.10) + 
        protein_bonus + 
        ingredient_reuse_bonus
```

---

## 💡 Example Use Cases

### 1. Budget-Conscious Student

```python
prefs = UserPreferences(
    diet="Vegetarian",
    daily_calorie_target=1800,
    weekly_budget=800,
    cooking_time_limit=30,
    region="North",
    goals=["energy"],
    cost_per_meal_limit=50
)
```

**Output:** Simple, quick, affordable vegetarian meals under ₹800/week.

### 2. Fitness Enthusiast

```python
prefs = UserPreferences(
    diet="High-Protein",
    daily_calorie_target=2500,
    weekly_budget=1500,
    cooking_time_limit=60,
    region="All",
    goals=["muscle gain", "high-protein"],
    cost_per_meal_limit=90
)
```

**Output:** Protein-rich meals (>15g protein/meal) optimized for muscle gain.

### 3. Vegan South Indian

```python
prefs = UserPreferences(
    diet="Vegan",
    daily_calorie_target=1800,
    weekly_budget=1000,
    cooking_time_limit=40,
    region="South",
    goals=["immunity"],
    cost_per_meal_limit=60
)
```

**Output:** Plant-based South Indian meals without dairy/eggs.

---

## 🧪 Testing

Run the demonstration notebook:

```bash
jupyter notebook mealcraft_demo.ipynb
```

Or use the CLI for interactive testing:

```bash
python mealcraft_cli.py
```

---

## 📈 Performance Metrics

- **Dataset Coverage:** 256 authentic Indian dishes
- **Diet Support:** 8 dietary patterns
- **Regional Coverage:** 6 Indian regions
- **Average Generation Time:** 2-5 seconds
- **Budget Accuracy:** ±5% of target
- **Calorie Accuracy:** ±15% of target
- **Ingredient Reuse:** 30-40% overlap

---

## 🤝 API Integration

### Example cURL Request

```bash
curl -X POST http://localhost:5000/api/generate-meal-plan \
  -H "Content-Type: application/json" \
  -d '{
    "diet": "Vegetarian",
    "daily_calorie_target": 2000,
    "weekly_budget": 1200,
    "cooking_time_limit": 45,
    "region": "North",
    "preferred_flavors": ["spicy"],
    "goals": ["weight loss"],
    "cost_per_meal_limit": 75
  }'
```

### Example Python Request

```python
import requests

response = requests.post(
    'http://localhost:5000/api/generate-meal-plan',
    json={
        "diet": "Vegetarian",
        "daily_calorie_target": 2000,
        "weekly_budget": 1200,
        "cooking_time_limit": 45,
        "region": "North",
        "preferred_flavors": ["spicy"],
        "goals": ["weight loss"],
        "cost_per_meal_limit": 75
    }
)

meal_plan = response.json()
```

---

## 🛠️ Customization

### Adding New Ingredients

Edit `NutritionEstimator.INGREDIENT_NUTRITION` in `mealcraft_ai.py`:

```python
INGREDIENT_NUTRITION = {
    "new_ingredient": {
        "calories": 100, 
        "protein": 5, 
        "carbs": 15, 
        "fat": 2
    },
    ...
}
```

### Adjusting Cost Factors

Modify `CostEstimator.INGREDIENT_COSTS`:

```python
INGREDIENT_COSTS = {
    "ingredient": 10,  # INR per typical serving
    ...
}
```

### Changing Scoring Weights

Adjust weights in `MealScorer.score_meal()`:

```python
final_score = (
    cost_score * 0.30 +      # Adjust these weights
    time_score * 0.20 +
    nutrition_score * 0.25 +
    flavor_score * 0.10 +
    protein_bonus +
    reuse_bonus
)
```

---

## 🐛 Troubleshooting

### Issue: "No dishes match your dietary preferences"

**Solution:** Relax constraints or choose "All" for region.

### Issue: Budget exceeded

**Solution:** Increase `weekly_budget` or lower `cost_per_meal_limit`.

### Issue: Low ingredient overlap

**Solution:** System prioritizes nutrition over overlap. This is normal.

---

## 📚 Additional Resources

- **Dataset Source:** Custom curated Indian food database
- **Nutrition Data:** Based on USDA and IFCT databases
- **Cost Data:** Average Indian market prices (2024-2025)

---

## 🎉 Features Roadmap

- [ ] Multi-week planning
- [ ] Leftover management
- [ ] Seasonal ingredient optimization
- [ ] Restaurant alternative suggestions
- [ ] Grocery delivery integration
- [ ] Mobile app development

---

## 📧 Support

For questions or issues:
- Open an issue in the repository
- Review the demo notebook for examples
- Check the API documentation

---

## ⚖️ License

MIT License - Feel free to use, modify, and distribute.

---

**MealCraft-AI** - Making Indian meal planning intelligent, affordable, and delicious! 🍛✨
