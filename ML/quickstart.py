"""
MealCraft-AI - Quick Start Script
Run this to verify your installation and generate a sample meal plan
"""

import sys
from pathlib import Path

print("=" * 80)
print("MEALCRAFT-AI - QUICK START")
print("=" * 80)

# Check Python version
print(f"\n✓ Python version: {sys.version.split()[0]}")

# Check dependencies
print("\n📦 Checking dependencies...")
required_packages = {
    'pandas': 'Data processing',
    'numpy': 'Numerical computing',
    'sklearn': 'Machine learning',
    'fastapi': 'REST API',
    'requests': 'HTTP requests',
    'beautifulsoup4': 'Web scraping'
}

missing = []
for package, description in required_packages.items():
    try:
        if package == 'sklearn':
            __import__('sklearn')
        elif package == 'beautifulsoup4':
            __import__('bs4')
        else:
            __import__(package)
        print(f"   ✓ {package:20s} - {description}")
    except ImportError:
        print(f"   ✗ {package:20s} - MISSING")
        missing.append(package)

if missing:
    print(f"\n⚠️  Missing packages: {', '.join(missing)}")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)

# Check data files
print("\n📊 Checking data files...")
data_files = {
    'indian_food_cleaned.csv': 'Production dataset',
    'indian_food.csv': 'Original dataset'
}

for file, description in data_files.items():
    if Path(file).exists():
        size = Path(file).stat().st_size / 1024
        print(f"   ✓ {file:30s} - {description} ({size:.1f} KB)")
    else:
        print(f"   ✗ {file:30s} - MISSING")

# Check core files
print("\n🔧 Checking core files...")
core_files = {
    'mealcraft_ai.py': 'Main ML system',
    'mealcraft_cli.py': 'CLI interface',
    'mealcraft_api.py': 'REST API',
    'local_grocery_scraper.py': 'Grocery scraper',
}

for file, description in core_files.items():
    if Path(file).exists():
        lines = len(Path(file).read_text(encoding='utf-8').split('\n'))
        print(f"   ✓ {file:30s} - {description} ({lines} lines)")
    else:
        print(f"   ✗ {file:30s} - MISSING")

# Test import
print("\n🧪 Testing system import...")
try:
    from mealcraft_ai import MealCraftAI, UserPreferences
    print("   ✓ MealCraftAI imported successfully")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Generate sample meal plan
print("\n🍽️  Generating sample meal plan...")
try:
    planner = MealCraftAI(
        dataset_path='indian_food_cleaned.csv',
        location='Chennai',
        use_realtime_prices=False
    )
    print("   ✓ System initialized")
    
    # Generate 3-day plan (quick test)
    prefs = UserPreferences(
        diet='vegetarian',
        preferred_cuisines=['south indian'],
        daily_calorie_target=2000,
        weekly_budget=500,
        preferred_flavors=['spicy', 'tangy'],
        cooking_time_limit=45,
        region='tamil nadu',
        goals=['healthy eating', 'budget-friendly'],
        cost_per_meal_limit=100
    )
    
    plan = planner.generate_weekly_plan(prefs)
    print("   ✓ Meal plan generated")
    
    # Debug: Check what keys exist
    print(f"\n   📋 Plan keys: {list(plan.keys())}")
    
    # Display summary
    print("\n" + "=" * 80)
    print("SAMPLE MEAL PLAN STRUCTURE")
    print("=" * 80)
    
    # Show plan structure
    print(f"\n📋 Weekly Plan: {len(plan['weekly_plan'])} days generated")
    print(f"💰 Total Cost: {plan['summary']['total_cost']}")
    print(f"� Shopping List: {len(plan['shopping_list'])} items")
    
    # Show first 2 days as sample
    for i, day_plan in enumerate(plan['weekly_plan'][:2], 1):
        print(f"\n📅 DAY {i}")
        for meal_type, meal in day_plan.items():
            if isinstance(meal, dict):
                cost = meal.get('cost', 0)
                cost_str = f"Rs {float(cost):.0f}" if isinstance(cost, (int, float)) else f"Rs {cost}"
                print(f"   • {meal_type.title():10s}: {meal.get('name', 'N/A')[:25]:25s} "
                      f"{cost_str} | {meal.get('calories', 0)} kcal")
    
    print("\n" + "-" * 80)
    print(f"✨ Successfully generated {len(plan['weekly_plan'])} day meal plan!")
    print(f"💰 Budget Status: Rs {plan['summary']['total_cost']}")
    
    # Export test
    print("\n💾 Exporting to JSON...")
    import json
    with open('quickstart_test.json', 'w') as f:
        json.dump(plan, f, indent=2)
    if Path('quickstart_test.json').exists():
        print("   ✓ Export successful: quickstart_test.json")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED - SYSTEM READY!")
    print("=" * 80)
    
    print("\n🚀 Next Steps:")
    print("   1. Run CLI:  python mealcraft_cli.py")
    print("   2. Run API:  python mealcraft_api.py")
    print("   3. Read docs: README.md")
    print()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
