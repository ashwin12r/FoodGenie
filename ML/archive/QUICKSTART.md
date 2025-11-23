# 🚀 MealCraft-AI Quick Start Guide

## Installation (2 minutes)

### Step 1: Install Dependencies

Open PowerShell and run:

```powershell
cd "c:\prime project\ML"
pip install -r requirements.txt
```

### Step 2: Verify Installation

```powershell
python -c "import pandas, numpy, flask; print('✅ All dependencies installed!')"
```

---

## Usage Options

### Option 1: Interactive CLI (Easiest - Recommended for First Time)

```powershell
python mealcraft_cli.py
```

Follow the prompts:
1. Choose your diet (e.g., Vegetarian)
2. Select region (e.g., North)
3. Enter daily calories (e.g., 2000)
4. Set weekly budget (e.g., 1200)
5. ... and more

**Output:** Your meal plan will be saved to `my_meal_plan.json`

---

### Option 2: Python Script (Programmers)

Create a file `my_meal_plan.py`:

```python
from mealcraft_ai import MealCraftAI, UserPreferences
import json

# Initialize
ai = MealCraftAI("indian_food.csv")

# Your preferences
prefs = UserPreferences(
    diet="Vegetarian",
    preferred_cuisines=["North Indian"],
    daily_calorie_target=2000,
    weekly_budget=1200,
    preferred_flavors=["spicy", "mild"],
    cooking_time_limit=45,
    region="North",
    goals=["weight loss"],
    cost_per_meal_limit=75
)

# Generate
meal_plan = ai.generate_weekly_plan(prefs)

# Save
with open('output.json', 'w') as f:
    json.dump(meal_plan, f, indent=2)

print("✅ Meal plan created!")
```

Run it:
```powershell
python my_meal_plan.py
```

---

### Option 3: REST API (Web/Mobile Apps)

#### Start the server:

```powershell
python mealcraft_api.py
```

Server runs at: `http://localhost:5000`

#### Make a request:

**Using cURL:**
```powershell
curl -X POST http://localhost:5000/api/generate-meal-plan -H "Content-Type: application/json" -d '{\"diet\":\"Vegetarian\",\"daily_calorie_target\":2000,\"weekly_budget\":1200,\"cooking_time_limit\":45,\"region\":\"North\",\"preferred_flavors\":[\"spicy\"],\"goals\":[\"weight loss\"],\"cost_per_meal_limit\":75}'
```

**Using Python:**
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
print(meal_plan)
```

---

### Option 4: Jupyter Notebook (Data Scientists)

```powershell
jupyter notebook mealcraft_demo.ipynb
```

Run all cells to see:
- 3 complete example scenarios
- Visualizations (calorie/protein charts)
- Cost analysis
- Shopping lists
- Batch cooking suggestions

---

## Understanding Your Output

Your meal plan JSON looks like this:

```json
{
  "weekly_plan": [
    {
      "day": "Monday",
      "meals": {
        "breakfast": {
          "dish": "Poha",
          "time": "30 min",
          "calories": "350 kcal",
          "protein": "8.5g",
          "cost": "₹45"
        },
        "lunch": { ... },
        "dinner": { ... }
      }
    },
    ...
  ],
  "summary": {
    "total_cost": "₹1150",
    "budget_status": "optimal"
  },
  "shopping_list": { ... },
  "batch_cooking_suggestions": [ ... ]
}
```

---

## Quick Examples

### 1. Budget Student Plan (₹800/week)

```python
UserPreferences(
    diet="Vegetarian",
    daily_calorie_target=1800,
    weekly_budget=800,
    cooking_time_limit=30,
    region="North",
    goals=["energy"],
    cost_per_meal_limit=50
)
```

### 2. Gym Enthusiast Plan (High Protein)

```python
UserPreferences(
    diet="High-Protein",
    daily_calorie_target=2500,
    weekly_budget=1500,
    cooking_time_limit=60,
    region="All",
    goals=["muscle gain"],
    cost_per_meal_limit=90
)
```

### 3. Vegan South Indian

```python
UserPreferences(
    diet="Vegan",
    daily_calorie_target=1800,
    weekly_budget=1000,
    cooking_time_limit=40,
    region="South",
    goals=["immunity"],
    cost_per_meal_limit=60
)
```

---

## Testing the System

Run comprehensive tests:

```powershell
python test_mealcraft.py
```

This validates:
- ✅ All diet types
- ✅ Budget constraints
- ✅ Calorie accuracy
- ✅ Ingredient optimization

---

## Common Issues

### "ModuleNotFoundError: No module named 'pandas'"

**Fix:**
```powershell
pip install pandas numpy flask flask-cors matplotlib jupyter
```

### "FileNotFoundError: indian_food.csv"

**Fix:**
Make sure you're in the correct directory:
```powershell
cd "c:\prime project\ML"
```

### "Budget exceeded"

**Fix:**
- Increase `weekly_budget`
- Lower `cost_per_meal_limit`
- Choose simpler diet (Vegetarian is cheapest)

---

## Next Steps

1. ✅ Run the CLI: `python mealcraft_cli.py`
2. ✅ Review your meal plan
3. ✅ Try different preferences
4. ✅ Explore the Jupyter notebook
5. ✅ Integrate the API into your app

---

## Need Help?

- 📖 Read the full README.md
- 🧪 Run tests: `python test_mealcraft.py`
- 📓 Check demo notebook: `mealcraft_demo.ipynb`
- 🔍 Review example files in the examples folder

---

**Happy Meal Planning! 🍽️✨**
