"""
Quick test to see meal plan structure
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json

preferences = UserPreferences(
    diet="vegetarian",
    preferred_cuisines=["South Indian"],
    daily_calorie_target=2000,
    weekly_budget=1500,
    preferred_flavors=["spicy"],
    cooking_time_limit=45,
    region="South",
    goals=["balanced_nutrition"],
    cost_per_meal_limit=100
)

ai = MealCraftAI(
    dataset_path="indian_food.csv",
    use_healthy_mode=True,
    use_meal_combinations=True,
    use_realtime_prices=False
)

meal_plan = ai.generate_weekly_plan(preferences)

# Save to JSON to inspect structure
with open('meal_plan_structure.json', 'w', encoding='utf-8') as f:
    json.dump(meal_plan, f, indent=2, default=str)

print("✅ Saved meal plan structure to meal_plan_structure.json")
print(f"\nKeys: {list(meal_plan.keys())}")

if 'weekly_plan' in meal_plan:
    print(f"\nWeekly plan has {len(meal_plan['weekly_plan'])} days")
    if len(meal_plan['weekly_plan']) > 0:
        first_day = meal_plan['weekly_plan'][0]
        print(f"\nFirst day structure:")
        print(f"  Keys: {first_day.keys() if isinstance(first_day, dict) else 'Not a dict'}")
        if isinstance(first_day, dict) and 'meals' in first_day:
            print(f"  Number of meals: {len(first_day['meals'])}")
            if len(first_day['meals']) > 0:
                first_meal = first_day['meals'][0]
                print(f"  First meal type: {type(first_meal)}")
                if isinstance(first_meal, dict):
                    print(f"  First meal keys: {first_meal.keys()}")
