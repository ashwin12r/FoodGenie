"""
Quick demo of real-time grocery pricing feature
Shows price comparison between static and dynamic pricing
"""

from mealcraft_ai import MealCraftAI, UserPreferences

def quick_demo():
    """Quick demonstration of real-time pricing"""
    
    print("\n" + "="*70)
    print("🛒 MealCraft-AI Real-Time Grocery Pricing Demo")
    print("="*70)
    
    # User preferences
    user_prefs = UserPreferences(
        diet="vegetarian",
        preferred_cuisines=["south indian", "north indian"],
        daily_calorie_target=2000,
        weekly_budget=1400,
        preferred_flavors=["spicy", "tangy"],
        cooking_time_limit=60,
        region="south",
        goals=["health", "budget"],
        cost_per_meal_limit=100
    )
    
    print("\n📋 User Preferences:")
    print(f"   Diet: {user_prefs.diet}")
    print(f"   Cuisines: {', '.join(user_prefs.preferred_cuisines)}")
    print(f"   Weekly Budget: Rs {user_prefs.weekly_budget}")
    print(f"   Daily Calories: {user_prefs.daily_calorie_target}")
    
    # Test with STATIC prices
    print("\n\n[1] Generating meal plan with STATIC PRICES...")
    print("-" * 70)
    
    ai_static = MealCraftAI(
        dataset_path='indian_food_healthy.csv',
        use_healthy_mode=True,
        use_realtime_prices=False
    )
    
    plan_static = ai_static.generate_weekly_plan(user_prefs)
    
    # Count meals and calculate cost
    static_meals = sum(len(course) for course in plan_static.values())
    static_cost = sum(
        dish['cost'] for course in plan_static.values() 
        for dish in course
    )
    
    print(f"\n✅ Static pricing complete!")
    print(f"   Total meals: {static_meals}")
    print(f"   Total cost: Rs {static_cost:.2f}")
    print(f"   Avg per meal: Rs {static_cost/static_meals:.2f}")
    
    # Show sample dishes
    print(f"\n   Sample dishes:")
    if 'breakfast' in plan_static and len(plan_static['breakfast']) > 0:
        dish = plan_static['breakfast'][0]
        print(f"   - {dish['name']}: Rs {dish['cost']:.2f}")
    if 'lunch' in plan_static and len(plan_static['lunch']) > 0:
        dish = plan_static['lunch'][0]
        print(f"   - {dish['name']}: Rs {dish['cost']:.2f}")
    
    # Test with REAL-TIME prices
    print("\n\n[2] Generating meal plan with REAL-TIME GROCERY PRICES...")
    print("-" * 70)
    print("   (Fetching live prices from BigBasket, Zepto, Swiggy Instamart)")
    
    ai_realtime = MealCraftAI(
        dataset_path='indian_food_healthy.csv',
        use_healthy_mode=True,
        use_realtime_prices=True,
        location="Bengaluru"  # You can also use None for auto-detect
    )
    
    plan_realtime = ai_realtime.generate_weekly_plan(user_prefs)
    
    # Count meals and calculate cost
    realtime_meals = sum(len(course) for course in plan_realtime.values())
    realtime_cost = sum(
        dish['cost'] for course in plan_realtime.values() 
        for dish in course
    )
    
    print(f"\n✅ Real-time pricing complete!")
    print(f"   Total meals: {realtime_meals}")
    print(f"   Total cost: Rs {realtime_cost:.2f}")
    print(f"   Avg per meal: Rs {realtime_cost/realtime_meals:.2f}")
    
    # Show sample dishes
    print(f"\n   Sample dishes:")
    if 'breakfast' in plan_realtime and len(plan_realtime['breakfast']) > 0:
        dish = plan_realtime['breakfast'][0]
        print(f"   - {dish['name']}: Rs {dish['cost']:.2f}")
    if 'lunch' in plan_realtime and len(plan_realtime['lunch']) > 0:
        dish = plan_realtime['lunch'][0]
        print(f"   - {dish['name']}: Rs {dish['cost']:.2f}")
    
    # Comparison
    print("\n\n[3] PRICING COMPARISON")
    print("=" * 70)
    print(f"\n   📊 Static Pricing:      Rs {static_cost:.2f}")
    print(f"   🛒 Real-Time Pricing:   Rs {realtime_cost:.2f}")
    print(f"   💰 Difference:          Rs {abs(realtime_cost - static_cost):.2f}")
    
    if realtime_cost > static_cost:
        percent = ((realtime_cost - static_cost) / static_cost) * 100
        print(f"   📈 Real-time is {percent:.1f}% higher than static")
    elif realtime_cost < static_cost:
        percent = ((static_cost - realtime_cost) / static_cost) * 100
        print(f"   📉 Real-time is {percent:.1f}% lower than static")
    else:
        print(f"   ➡️  Prices are identical")
    
    # Features summary
    print("\n\n[4] FEATURE SUMMARY")
    print("=" * 70)
    print("""
    ✅ Real-time price fetching from:
       - BigBasket
       - Zepto  
       - Swiggy Instamart
    
    ✅ Location-based pricing:
       - Auto-detect via IP geolocation
       - Manual location specification
       - City-specific price variations
    
    ✅ Smart fallback system:
       - Fallback database with 200+ items
       - Price averaging across stores
       - Graceful handling of scraping failures
    
    ✅ Performance optimization:
       - 1-hour price caching
       - Reduces API calls
       - Faster subsequent requests
    
    ✅ Fully integrated:
       - Works with healthy mode
       - Works with meal combinations
       - Works with variety enforcement
    """)
    
    print("\n" + "="*70)
    print("✅ Demo Complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        quick_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
