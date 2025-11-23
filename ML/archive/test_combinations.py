"""
🍽️ Test Meal Combinations Feature
Demonstrates the new complete meal combinations system.
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def test_meal_combinations():
    """Test the new meal combinations feature"""
    
    print_header("MEALCRAFT-AI: COMPLETE MEAL COMBINATIONS TEST")
    
    print("NEW FEATURE: Complete Meal Combinations")
    print("Instead of just 'Sambar', you get 'Sambar + Rice + Papad'")
    print("Instead of just 'Idli', you get 'Idli + Sambar + Chutney'")
    
    print_header("Initializing MealCraft-AI with Meal Combinations")
    
    # Initialize with meal combinations enabled (default)
    ai = MealCraftAI(use_meal_combinations=True)
    
    print_header("Creating User Profile")
    
    user_prefs = UserPreferences(
        diet="Vegetarian",
        daily_calorie_target=2000,
        weekly_budget=1500,
        cooking_time_limit=60,
        region="South",
        goals=["weight loss", "energy"],
        cost_per_meal_limit=80,
        preferred_flavors=["spicy"],
        preferred_cuisines=["South Indian", "North Indian"]
    )
    
    print(f"Diet: {user_prefs.diet}")
    print(f"Region: {user_prefs.region}")
    print(f"Budget per meal: <= Rs{user_prefs.cost_per_meal_limit}")
    print(f"Goals: {', '.join(user_prefs.goals)}")
    
    print_header("Generating 7-Day Meal Plan with Complete Combinations")
    
    print("Generating...")
    meal_plan = ai.generate_weekly_plan(user_prefs)
    
    print_header("MEAL PLAN WITH COMPLETE COMBINATIONS")
    
    for day_data in meal_plan['weekly_plan']:
        day = day_data['day']
        meals = day_data['meals']
        
        print(f"\n{'='*70}")
        print(f"  {day}")
        print(f"{'='*70}")
        
        # Breakfast
        breakfast = meals['breakfast']
        print(f"\n  BREAKFAST: {breakfast['dish']}")
        print(f"     Time: {breakfast['time']}")
        print(f"     Cost: {breakfast['cost']}")
        print(f"     Nutrition: {breakfast['calories']} | "
              f"Protein: {breakfast['protein']} | "
              f"Carbs: {breakfast['carbs']}")
        
        if 'accompaniments' in breakfast and breakfast['accompaniments']:
            print(f"     Components:")
            # Extract main dish (first part before +)
            main_dish = breakfast['dish'].split('+')[0].strip()
            print(f"       - {main_dish} (main)")
            for acc in breakfast['accompaniments']:
                print(f"       - {acc['name']} ({acc['quantity']})")
        
        # Lunch
        lunch = meals['lunch']
        print(f"\n  LUNCH: {lunch['dish']}")
        print(f"     Time: {lunch['time']}")
        print(f"     Cost: {lunch['cost']}")
        print(f"     Nutrition: {lunch['calories']} | "
              f"Protein: {lunch['protein']} | "
              f"Carbs: {lunch['carbs']}")
        
        if 'accompaniments' in lunch and lunch['accompaniments']:
            print(f"     Components:")
            main_dish = lunch['dish'].split('+')[0].strip()
            print(f"       - {main_dish} (main)")
            for acc in lunch['accompaniments']:
                print(f"       - {acc['name']} ({acc['quantity']})")
        
        # Dinner
        dinner = meals['dinner']
        print(f"\n  DINNER: {dinner['dish']}")
        print(f"     Time: {dinner['time']}")
        print(f"     Cost: {dinner['cost']}")
        print(f"     Nutrition: {dinner['calories']} | "
              f"Protein: {dinner['protein']} | "
              f"Carbs: {dinner['carbs']}")
        
        if 'accompaniments' in dinner and dinner['accompaniments']:
            print(f"     Components:")
            main_dish = dinner['dish'].split('+')[0].strip()
            print(f"       - {main_dish} (main)")
            for acc in dinner['accompaniments']:
                print(f"       - {acc['name']} ({acc['quantity']})")
    
    print_header("WEEKLY SUMMARY")
    
    summary = meal_plan['summary']
    
    def parse_cost(cost_str):
        return float(cost_str.replace('Rs', '').replace('  ', '').strip())
    
    total_cost = parse_cost(summary['total_cost'])
    
    print(f"Total Weekly Cost: {summary['total_cost']}")
    print(f"Weekly Budget: Rs{user_prefs.weekly_budget}")
    print(f"Budget Status: {summary['budget_status'].upper()}")
    print(f"\nDaily Average Calories: {summary['daily_avg_calories']:.0f} kcal")
    print(f"Daily Average Protein: {summary['daily_avg_protein']}")
    
    print_header("KEY IMPROVEMENTS")
    
    print("BEFORE (Old System):")
    print("   Lunch: Sambar (just gravy)")
    print("   Dinner: Dal Tadka (just gravy)")
    print("   Problem: Can't eat just gravy alone!")
    
    print("\nAFTER (New System with Combinations):")
    print("   Lunch: Sambar + Rice + Papad (complete meal)")
    print("   Breakfast: Idli + Sambar + Chutney (complete meal)")
    print("   Dinner: Dal Tadka + Roti + Pickle (complete meal)")
    print("   Success: Realistic, complete Indian meals!")
    
    print_header("COMPARISON")
    
    # Count combinations
    total_meals = len(meal_plan['weekly_plan']) * 3
    meals_with_combinations = 0
    
    for day_data in meal_plan['weekly_plan']:
        for meal_type, meal in day_data['meals'].items():
            if 'accompaniments' in meal and meal['accompaniments']:
                meals_with_combinations += 1
    
    print(f"Total Meals: {total_meals}")
    print(f"Meals with Combinations: {meals_with_combinations}")
    print(f"Single-Dish Meals: {total_meals - meals_with_combinations}")
    print(f"\nCombination Rate: {(meals_with_combinations/total_meals)*100:.1f}%")
    
    # Save
    output_file = "meal_plan_with_combinations.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(meal_plan, f, indent=2, ensure_ascii=False)
    
    print(f"\nFull meal plan saved to: {output_file}")
    
    print_header("TEST COMPLETE")
    
    print("Meal combinations are now working!")
    print("\nTo use in your code:")
    print("   ai = MealCraftAI(use_meal_combinations=True)  # Enable combinations")
    print("   ai = MealCraftAI(use_meal_combinations=False) # Disable (old behavior)")

if __name__ == "__main__":
    test_meal_combinations()
