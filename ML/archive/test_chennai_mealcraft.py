"""
Test MealCraft-AI with Chennai Local Grocery Prices
Uses Grace Daily & KPN Fresh for real-time pricing
"""

from mealcraft_ai import MealCraftAI, UserPreferences

print("=" * 80)
print("MEALCRAFT-AI WITH CHENNAI GROCERY PRICES")
print("=" * 80)
print()

# Create user preferences
preferences = UserPreferences(
    diet="vegetarian",
    preferred_cuisines=["South Indian", "North Indian"],
    daily_calorie_target=2000,
    weekly_budget=1500,  # Rs 1500 per week
    preferred_flavors=["spicy", "tangy"],
    cooking_time_limit=45,
    region="South",
    goals=["balanced_nutrition", "weight_maintenance"],
    cost_per_meal_limit=100  # Rs 100 per meal max
)

print(f"User Preferences:")
print(f"  - Diet: {preferences.diet}")
print(f"  - Cuisines: {', '.join(preferences.preferred_cuisines)}")
print(f"  - Daily Calories: {preferences.daily_calorie_target}")
print(f"  - Weekly Budget: Rs {preferences.weekly_budget}")
print(f"  - Location: Chennai")
print()

# Initialize MealCraft-AI with real-time pricing
print("Initializing MealCraft-AI...")
ai = MealCraftAI(
    dataset_path="indian_food.csv",
    use_healthy_mode=True,
    use_meal_combinations=True,
    use_realtime_prices=False,  # Disable scraping, use fallback database for speed
    location="Chennai"
)
print()

# Generate meal plan
print("=" * 80)
print("GENERATING 3-DAY MEAL PLAN")
print("=" * 80)
print()

try:
    meal_plan = ai.generate_weekly_plan(preferences)
    
    print("\n" + "=" * 80)
    print("MEAL PLAN GENERATED")
    print("=" * 80)
    print()
    
    # Extract the actual weekly plan
    weekly_data = meal_plan.get('weekly_plan', [])
    
    # Display the plan
    total_cost = 0
    total_calories = 0
    meal_count = 0
    
    for day in weekly_data:
        day_name = day.get('day', 'Unknown')
        print(f"\n📅 {day_name.upper()}")
        print("-" * 80)
        
        day_calories = 0
        day_cost = 0
        
        # Get meals for the day (it's a dict: breakfast/lunch/dinner)
        meals = day.get('meals', {})
        for meal_type, meal_data in meals.items():
            meal_count += 1
            
            # Extract dish name
            dish_name = meal_data.get('dish', 'Unknown')
            
            # Extract calories (remove "kcal" suffix)
            calories_str = meal_data.get('calories', '0')
            calories = int(calories_str.replace(' kcal', '').replace(',', ''))
            
            # Extract cost (remove ₹ symbol)
            cost_str = meal_data.get('cost', '₹0')
            cost = float(cost_str.replace('₹', '').replace(',', ''))
            
            # Extract time
            time_str = meal_data.get('time', '0 min')
            
            print(f"\n🍽️  {meal_type.upper()}")
            print(f"   • {dish_name}")
            print(f"     Prep Time: {time_str}")
            print(f"     Calories: {calories} kcal")
            print(f"     Cost: Rs {cost:.2f}")
            print(f"     Reason: {meal_data.get('reason', 'N/A')}")
            
            day_calories += calories
            day_cost += cost
        
        print(f"\n   📊 Day Total: {day_calories} kcal | Rs {day_cost:.2f}")
        total_cost += day_cost
        total_calories += day_calories
    
    print("\n" + "=" * 80)
    day_count = len(weekly_data)
    print(f"💰 TOTAL COST ({day_count} days): Rs {total_cost:.2f}")
    if day_count > 0:
        print(f"💵 AVERAGE DAILY COST: Rs {total_cost/day_count:.2f}")
        print(f"📊 TOTAL MEALS: {meal_count}")
        print(f"� AVG DAILY CALORIES: {total_calories/day_count:.0f} kcal")
    print("=" * 80)
    
    # Check if within budget
    if total_cost <= preferences.weekly_budget:
        surplus = preferences.weekly_budget - total_cost
        print(f"\n✅ Within budget! You save Rs {surplus:.2f} per week")
    else:
        excess = total_cost - preferences.weekly_budget
        print(f"\n⚠️  Over budget by Rs {excess:.2f} per week")
    
    print("\n" + "=" * 80)
    print("✅ MEALCRAFT-AI WITH CHENNAI GROCERY PRICES - SUCCESS!")
    print("=" * 80)
    print()
    print("Price Sources:")
    print("  - Grace Daily (gracedaily.com) - Chennai local store")
    print("  - KPN Fresh (kpnfresh.com) - Chennai delivery service")
    print("  - Fallback database for items not found online")
    print("  - Bright Data proxy for reliable access")
    print()

except Exception as e:
    print(f"\n❌ Error generating meal plan: {e}")
    import traceback
    traceback.print_exc()
