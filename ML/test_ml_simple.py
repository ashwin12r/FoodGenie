"""
Simple ML test - check what's being generated
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json

# Initialize
print("Initializing ML system...")
meal_planner = MealCraftAI(
    dataset_path="indian_food_cleaned.csv",
    location="Mumbai",
    use_realtime_prices=False
)

# Create preferences
prefs = UserPreferences(
    diet="vegetarian",
    preferred_cuisines=["North Indian"],
    daily_calorie_target=2000,
    weekly_budget=2000.0,
    preferred_flavors=["spicy", "mild"],
    cooking_time_limit=30,
    region="North",
    goals=["balanced"],
    cost_per_meal_limit=100.0
)

# Generate plan
print("\nGenerating meal plan...")
meal_plan = meal_planner.generate_weekly_plan(prefs)

# Show structure
print("\nMeal plan structure:")
print(f"Type: {type(meal_plan)}")
print(f"Keys: {list(meal_plan.keys())}")

# Show what's in the plan
print("\nDetailed plan:")
print(json.dumps(meal_plan, indent=2, default=str))
