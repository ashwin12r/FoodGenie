"""
Simple test for meal combinations - outputs to JSON file
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json

print("="*70)
print("TESTING MEAL COMBINATIONS FEATURE")
print("="*70)

print("\nInitializing MealCraft-AI...")
ai = MealCraftAI(use_meal_combinations=True)

print("\nCreating user preferences...")
user_prefs = UserPreferences(
    diet="Vegetarian",
    daily_calorie_target=2000,
    weekly_budget=1500,
    cooking_time_limit=60,
    region="South",
    goals=["weight loss", "energy"],
    cost_per_meal_limit=80,
    preferred_flavors=["spicy"],
    preferred_cuisines=["South Indian"]
)

print("Generating meal plan...")
meal_plan = ai.generate_weekly_plan(user_prefs)

# Save to file
output_file = "meal_plan_combinations.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(meal_plan, f, indent=2, ensure_ascii=False)

print(f"\n SUCCESS! Meal plan saved to: {output_file}")

# Print summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

# Count combinations
total_meals = 0
meals_with_combos = 0

for day in meal_plan['weekly_plan']:
    for meal_type in ['breakfast', 'lunch', 'dinner']:
        total_meals += 1
        meal = day['meals'][meal_type]
        
        # Check if meal has + sign (combination)
        if '+' in meal['dish']:
            meals_with_combos += 1
            print(f"\n{day['day']} {meal_type.title()}: {meal['dish']}")
            if 'accompaniments' in meal:
                print(f"  Components: {len(meal['accompaniments']) + 1} items")

print(f"\n\nTotal Meals: {total_meals}")
print(f"Meals with Combinations: {meals_with_combos}")
print(f"Single-Dish Meals: {total_meals - meals_with_combos}")
print(f"Combination Rate: {(meals_with_combos/total_meals)*100:.1f}%")

print("\n" + "="*70)
print("EXAMPLES OF COMPLETE MEALS:")
print("="*70)

# Show first 3 combinations
count = 0
for day in meal_plan['weekly_plan']:
    for meal_type in ['breakfast', 'lunch', 'dinner']:
        meal = day['meals'][meal_type]
        if '+' in meal['dish'] and count < 5:
            count += 1
            print(f"\n{count}. {day['day']} - {meal_type.upper()}")
            print(f"   Meal: {meal['dish']}")
            print(f"   Time: {meal['time']}")
            print(f"   Cost: {meal['cost']}")
            print(f"   Calories: {meal['calories']}")
            if 'accompaniments' in meal:
                print(f"   Breakdown:")
                main = meal['dish'].split('+')[0].strip()
                print(f"      - {main} (main dish)")
                for acc in meal['accompaniments']:
                    print(f"      - {acc['name']} ({acc['quantity']})")

print("\n" + "="*70)
print("TEST COMPLETE!")
print("="*70)
print(f"\nCheck {output_file} for full details")
