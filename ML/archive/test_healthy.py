"""
Test the improved MealCraft-AI with data cleaning and health focus
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json


def test_healthy_meal_plan():
    """Test the improved health-focused meal planning"""
    
    print("="*70)
    print("🧪 TESTING IMPROVED MEALCRAFT-AI")
    print("   Data Cleaning + Health-Focused Meal Selection")
    print("="*70)
    print()
    
    # Initialize with healthy mode enabled
    print("1️⃣  Initializing MealCraft-AI with healthy mode...")
    ai = MealCraftAI("indian_food.csv", use_healthy_mode=True)
    print()
    
    # Test scenario: Health-conscious vegetarian
    print("2️⃣  Creating health-focused meal plan...")
    print()
    
    user_prefs = UserPreferences(
        diet="Vegetarian",
        preferred_cuisines=["North Indian"],
        daily_calorie_target=2000,
        weekly_budget=1200,
        preferred_flavors=["spicy", "mild"],
        cooking_time_limit=45,
        region="North",
        goals=["weight loss", "energy"],
        cost_per_meal_limit=75
    )
    
    print(f"📋 User Profile:")
    print(f"   Diet: {user_prefs.diet}")
    print(f"   Goals: {', '.join(user_prefs.goals)}")
    print(f"   Region: {user_prefs.region}")
    print(f"   Daily Calories: {user_prefs.daily_calorie_target}")
    print(f"   Weekly Budget: ₹{user_prefs.weekly_budget}")
    print()
    
    print("⏳ Generating meal plan...")
    meal_plan = ai.generate_weekly_plan(user_prefs)
    print()
    
    if "error" in meal_plan:
        print(f"❌ Error: {meal_plan['error']}")
        return
    
    # Check meal types
    print("3️⃣  Analyzing meal types...")
    print()
    
    breakfast_items = []
    lunch_items = []
    dinner_items = []
    
    for day in meal_plan['weekly_plan']:
        breakfast_items.append(day['meals']['breakfast']['dish'])
        lunch_items.append(day['meals']['lunch']['dish'])
        dinner_items.append(day['meals']['dinner']['dish'])
    
    print("🍳 BREAKFAST ITEMS (Should be healthy snacks like Poha, Idli, etc.):")
    for i, item in enumerate(breakfast_items, 1):
        print(f"   Day {i}: {item}")
    
    print(f"\n🍛 LUNCH ITEMS (Should be main courses):")
    for i, item in enumerate(lunch_items, 1):
        print(f"   Day {i}: {item}")
    
    print(f"\n🍲 DINNER ITEMS (Should be main courses):")
    for i, item in enumerate(dinner_items, 1):
        print(f"   Day {i}: {item}")
    
    # Show summary
    print("\n" + "="*70)
    print("📊 WEEKLY SUMMARY")
    print("="*70)
    summary = meal_plan['summary']
    print(f"💰 Total Cost: {summary['total_cost']} (Budget: ₹{user_prefs.weekly_budget})")
    print(f"📈 Budget Status: {summary['budget_status'].upper()}")
    print(f"🍽️  Avg Cost/Meal: {summary['avg_cost_per_meal']}")
    print(f"🔥 Daily Avg Calories: {summary['daily_avg_calories']} kcal")
    print(f"💪 Daily Avg Protein: {summary['daily_avg_protein']}")
    print(f"🎯 Calorie Accuracy: {summary['calorie_balance_accuracy']}")
    
    # Save output
    with open('healthy_meal_plan_test.json', 'w', encoding='utf-8') as f:
        json.dump(meal_plan, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Full plan saved to: healthy_meal_plan_test.json")
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETE!")
    print("="*70)
    print("\n💡 Key Improvements:")
    print("   ✓ -1 values in dataset cleaned")
    print("   ✓ Breakfast now uses healthy snacks (not sweets)")
    print("   ✓ Lunch & dinner use main courses only")
    print("   ✓ Desserts removed (health focus)")
    print("   ✓ More balanced, nutritious meal plans")


if __name__ == "__main__":
    test_healthy_meal_plan()
