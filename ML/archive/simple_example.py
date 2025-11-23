"""
Simple example showing real-time pricing vs static pricing
Run this to see the difference!
"""

from mealcraft_ai import MealCraftAI, UserPreferences

print("\n" + "="*70)
print("💰 PRICE COMPARISON: Static vs Real-Time")
print("="*70)

# User preferences
prefs = UserPreferences(
    diet="vegetarian",
    preferred_cuisines=["south indian"],
    daily_calorie_target=2000,
    weekly_budget=1400,
    preferred_flavors=["spicy"],
    cooking_time_limit=60,
    region="south",
    goals=["health"],
    cost_per_meal_limit=100
)

# Static pricing (default)
print("\n[1] With STATIC pricing (fast, estimates)...")
ai_static = MealCraftAI(
    dataset_path='indian_food_healthy.csv',
    use_realtime_prices=False
)
plan_static = ai_static.generate_weekly_plan(prefs)

# Extract cost from the structured plan
cost_static = 0
for day in plan_static['weekly_plan']:
    for meal_type, meal in day['meals'].items():
        # Parse cost string like "₹45.50"
        cost_str = meal['cost'].replace('₹', '').replace(',', '')
        cost_static += float(cost_str)

print(f"    ✅ Total weekly cost: Rs {cost_static:.2f}")
print(f"    📋 {len(plan_static['weekly_plan'])} days, {len(plan_static['weekly_plan']) * 3} meals")

# Real-time pricing (NEW!)
print("\n[2] With REAL-TIME pricing (actual grocery store prices)...")
ai_realtime = MealCraftAI(
    dataset_path='indian_food_healthy.csv',
    use_realtime_prices=True,
    location="Chennai"
)
plan_realtime = ai_realtime.generate_weekly_plan(prefs)

# Extract cost from the structured plan
cost_realtime = 0
for day in plan_realtime['weekly_plan']:
    for meal_type, meal in day['meals'].items():
        # Parse cost string like "₹45.50"
        cost_str = meal['cost'].replace('₹', '').replace(',', '')
        cost_realtime += float(cost_str)

print(f"    ✅ Total weekly cost: Rs {cost_realtime:.2f}")
print(f"    📋 {len(plan_realtime['weekly_plan'])} days, {len(plan_realtime['weekly_plan']) * 3} meals")

# Comparison
print("\n" + "="*70)
print("📊 COMPARISON:")
print(f"   Static:     Rs {cost_static:.2f}")
print(f"   Real-time:  Rs {cost_realtime:.2f}")
print(f"   Difference: Rs {abs(cost_realtime - cost_static):.2f}")
if cost_realtime > cost_static:
    percent = ((cost_realtime - cost_static) / cost_static) * 100
    print(f"   Real-time is {percent:.1f}% higher")
elif cost_static > cost_realtime:
    percent = ((cost_static - cost_realtime) / cost_static) * 100
    print(f"   Real-time is {percent:.1f}% lower")
print("="*70 + "\n")

print("🎯 Real-time pricing uses actual prices from:")
print("   - BigBasket")
print("   - Zepto")
print("   - Swiggy Instamart")
print("\n✨ Location-aware, cached for performance, with smart fallback!")
