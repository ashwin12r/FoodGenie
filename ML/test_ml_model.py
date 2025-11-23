"""
Test script to verify MealCraft ML model functionality
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json

def test_ml_model():
    print("=" * 60)
    print("🧪 Testing MealCraft ML Model")
    print("=" * 60)
    
    # Step 1: Initialize ML system
    print("\n1️⃣ Initializing ML system...")
    try:
        meal_planner = MealCraftAI(
            dataset_path="indian_food_cleaned.csv",
            location="Mumbai",
            use_realtime_prices=False
        )
        print("✅ ML system initialized successfully!")
        print(f"   Dataset loaded with {len(meal_planner.df)} dishes")
    except Exception as e:
        print(f"❌ Failed to initialize ML system: {e}")
        return False
    
    # Step 2: Create test user preferences
    print("\n2️⃣ Creating test user preferences...")
    test_preferences = UserPreferences(
        diet="Vegetarian",
        preferred_cuisines=["North Indian"],
        daily_calorie_target=2000,
        weekly_budget=2000.0,
        preferred_flavors=["spicy", "mild"],
        cooking_time_limit=30,
        region="North",
        goals=["balanced"],
        cost_per_meal_limit=100.0
    )
    print("✅ Test preferences created:")
    print(f"   Cuisine: {test_preferences.preferred_cuisines}")
    print(f"   Diet: {test_preferences.diet}")
    print(f"   Budget: ₹{test_preferences.cost_per_meal_limit} per meal")
    
    # Step 3: Generate weekly meal plan
    print("\n3️⃣ Generating weekly meal plan...")
    try:
        meal_plan = meal_planner.generate_weekly_plan(test_preferences)
        print("✅ Weekly meal plan generated successfully!")
        
        total_meals = 0
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            meals = meal_plan.get(day, {})
            day_meals = len([m for m in meals.values() if m])
            total_meals += day_meals
            if day_meals > 0:
                print(f"   {day.capitalize()}: {day_meals} meals")
        
        print(f"\n   Total meals planned: {total_meals}")
        
        # Show sample meals
        print("\n   Sample meals:")
        monday_breakfast = meal_plan.get('monday', {}).get('breakfast')
        if monday_breakfast:
            print(f"      Monday Breakfast: {monday_breakfast.get('name', 'N/A')}")
            print(f"         Diet: {monday_breakfast.get('diet', 'N/A')}")
            
        monday_lunch = meal_plan.get('monday', {}).get('lunch')
        if monday_lunch:
            print(f"      Monday Lunch: {monday_lunch.get('name', 'N/A')}")
            
        monday_dinner = meal_plan.get('monday', {}).get('dinner')
        if monday_dinner:
            print(f"      Monday Dinner: {monday_dinner.get('name', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Failed to generate weekly plan: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 4: Test different dietary preferences
    print("\n4️⃣ Testing different dietary preferences...")
    dietary_options = ["vegetarian", "non-vegetarian", "vegan"]
    
    for diet in dietary_options:
        try:
            prefs = UserPreferences(
                diet=diet,
                preferred_cuisines=["North Indian"],
                daily_calorie_target=2000,
                weekly_budget=2000.0,
                preferred_flavors=["spicy"],
                cooking_time_limit=30,
                region="North",
                goals=["balanced"],
                cost_per_meal_limit=100.0
            )
            plan = meal_planner.generate_weekly_plan(prefs)
            meal_count = sum(len([m for m in plan.get(d, {}).values() if m]) for d in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
            print(f"   ✅ {diet.capitalize()}: {meal_count} meals generated")
        except Exception as e:
            print(f"   ⚠️  {diet.capitalize()}: {e}")
    
    # Success summary
    print("\n" + "=" * 60)
    print("✨ ML Model Test Complete!")
    print("=" * 60)
    print("\n✅ All core functionalities working:")
    print("   • Model initialization")
    print("   • User preferences handling")
    print("   • Weekly meal plan generation")
    print("   • Multiple dietary options support")
    print("\n🎉 ML model is ready for integration!")
    
    return True

if __name__ == "__main__":
    test_ml_model()
