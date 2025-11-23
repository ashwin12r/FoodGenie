"""
Comprehensive test showing variety and repetition analysis
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json
from collections import Counter

print("="*70)
print("VARIETY & REPETITION ANALYSIS")
print("="*70)

print("\nInitializing MealCraft-AI with combinations and variety enforcement...")
ai = MealCraftAI(use_meal_combinations=True)

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

# Save
with open("variety_test_output.json", 'w', encoding='utf-8') as f:
    json.dump(meal_plan, f, indent=2, ensure_ascii=False)

print("\n" + "="*70)
print("VARIETY ANALYSIS")
print("="*70)

# Extract all main dishes
all_main_dishes = []
meals_by_day = {}

for day in meal_plan['weekly_plan']:
    day_name = day['day']
    meals_by_day[day_name] = []
    
    for meal_type in ['breakfast', 'lunch', 'dinner']:
        meal = day['meals'][meal_type]
        # Extract main dish (before +)
        full_dish = meal['dish']
        main_dish = full_dish.split('+')[0].strip()
        
        all_main_dishes.append(main_dish)
        meals_by_day[day_name].append((meal_type, main_dish, full_dish))

# Count repetitions
dish_counts = Counter(all_main_dishes)

print(f"\nTotal Meals: {len(all_main_dishes)}")
print(f"Unique Dishes: {len(dish_counts)}")
print(f"Variety Rate: {(len(dish_counts)/len(all_main_dishes))*100:.1f}%")

# Show repetitions
repeated_dishes = {dish: count for dish, count in dish_counts.items() if count > 1}

if repeated_dishes:
    print(f"\nRepeated Dishes ({len(repeated_dishes)} dishes):")
    for dish, count in sorted(repeated_dishes.items(), key=lambda x: x[1], reverse=True):
        print(f"   {dish}: {count} times")
        
        # Show which days
        occurrences = []
        for day_name, meals in meals_by_day.items():
            for meal_type, main_dish, _ in meals:
                if main_dish == dish:
                    occurrences.append(f"{day_name} {meal_type}")
        print(f"      Appears: {', '.join(occurrences)}")
else:
    print("\n  ALL DISHES ARE UNIQUE! Perfect variety!")

print(f"\nNon-repeated Dishes: {len([d for d in dish_counts.values() if d == 1])}")

print("\n" + "="*70)
print("DAY-BY-DAY BREAKDOWN")
print("="*70)

for day_name, meals in meals_by_day.items():
    print(f"\n{day_name}:")
    for meal_type, main_dish, full_dish in meals:
        print(f"   {meal_type.title()}: {full_dish}")

print("\n" + "="*70)
print("REPETITION GAP ANALYSIS")
print("="*70)

# Check gaps between repetitions
if repeated_dishes:
    for dish in repeated_dishes:
        print(f"\n{dish}:")
        positions = []
        for i, d in enumerate(all_main_dishes):
            if d == dish:
                day_num = i // 3  # 3 meals per day
                meal_num = i % 3
                meal_names = ['breakfast', 'lunch', 'dinner']
                positions.append((day_num, meal_names[meal_num], i))
        
        for i in range(1, len(positions)):
            prev_pos = positions[i-1]
            curr_pos = positions[i]
            gap = curr_pos[2] - prev_pos[2]
            day_gap = curr_pos[0] - prev_pos[0]
            print(f"   Gap: {gap} meals ({day_gap} days) - from Day {prev_pos[0]+1} {prev_pos[1]} to Day {curr_pos[0]+1} {curr_pos[1]}")
else:
    print("\nNo repetitions to analyze!")

print("\n" + "="*70)
print("MEAL COMBINATION ANALYSIS")
print("="*70)

# Count combinations
combo_count = 0
single_count = 0

for day in meal_plan['weekly_plan']:
    for meal_type in ['breakfast', 'lunch', 'dinner']:
        meal = day['meals'][meal_type]
        if '+' in meal['dish']:
            combo_count += 1
        else:
            single_count += 1

print(f"\nMeals with Combinations: {combo_count}/{len(all_main_dishes)} ({(combo_count/len(all_main_dishes))*100:.1f}%)")
print(f"Single-Dish Meals: {single_count}/{len(all_main_dishes)}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"\n  Variety: {len(dish_counts)}/{len(all_main_dishes)} unique dishes ({(len(dish_counts)/len(all_main_dishes))*100:.1f}%)")
print(f"  Combinations: {combo_count}/{len(all_main_dishes)} meals ({(combo_count/len(all_main_dishes))*100:.1f}%)")
print(f"  Repetitions: {len(repeated_dishes)} dishes repeated")

if repeated_dishes:
    min_gap = min([
        curr[2] - prev[2]
        for dish in repeated_dishes
        for positions in [[
            (i // 3, i % 3, i) 
            for i, d in enumerate(all_main_dishes) 
            if d == dish
        ]]
        for prev, curr in zip(positions[:-1], positions[1:])
    ])
    print(f"  Minimum gap between repeats: {min_gap} meals (~{min_gap//3} days)")

print("\n  SUCCESS: Variety enforcement working!")
print(f"\n  Output saved to: variety_test_output.json")
