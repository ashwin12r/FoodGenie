"""
Quick Demo of MealCraft-AI
Run this to see the system in action!
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_meal(meal_type, meal):
    """Print meal details"""
    print(f"\n  🍴 {meal_type.upper()}")
    print(f"     Dish: {meal['dish']}")
    print(f"     Time: {meal['time']} | Cost: {meal['cost']}")
    print(f"     Calories: {meal['calories']} | Protein: {meal['protein']}")
    print(f"     Reason: {meal['reason']}")


def demo_scenario_1():
    """Demo 1: Budget-conscious vegetarian"""
    print_section("DEMO 1: Budget-Conscious Vegetarian North Indian")
    
    ai = MealCraftAI("indian_food.csv")
    
    prefs = UserPreferences(
        diet="Vegetarian",
        preferred_cuisines=["North Indian"],
        daily_calorie_target=2000,
        weekly_budget=1000,
        preferred_flavors=["spicy", "mild"],
        cooking_time_limit=45,
        region="North",
        goals=["weight loss", "energy"],
        cost_per_meal_limit=60
    )
    
    print("\n📋 User Profile:")
    print(f"   Diet: {prefs.diet}")
    print(f"   Region: {prefs.region}")
    print(f"   Daily Calories: {prefs.daily_calorie_target}")
    print(f"   Weekly Budget: ₹{prefs.weekly_budget}")
    print(f"   Max Cost/Meal: ₹{prefs.cost_per_meal_limit}")
    print(f"   Goals: {', '.join(prefs.goals)}")
    
    print("\n⏳ Generating meal plan... (this takes 2-5 seconds)")
    
    meal_plan = ai.generate_weekly_plan(prefs)
    
    # Show first 2 days
    print("\n📅 Sample Days (Monday & Tuesday):")
    for day in meal_plan['weekly_plan'][:2]:
        print(f"\n{'─' * 70}")
        print(f"  📆 {day['day'].upper()}")
        print(f"{'─' * 70}")
        for meal_type, meal in day['meals'].items():
            print_meal(meal_type, meal)
    
    # Summary
    print_section("WEEKLY SUMMARY")
    summary = meal_plan['summary']
    print(f"\n  💰 Total Cost: {summary['total_cost']} (Budget: ₹{prefs.weekly_budget})")
    print(f"  📈 Budget Status: {summary['budget_status'].upper()}")
    print(f"  🍽️  Avg Cost/Meal: {summary['avg_cost_per_meal']}")
    print(f"  🔥 Daily Avg Calories: {summary['daily_avg_calories']} kcal")
    print(f"  💪 Daily Avg Protein: {summary['daily_avg_protein']}")
    print(f"  🎯 Calorie Accuracy: {summary['calorie_balance_accuracy']}")
    print(f"  ♻️  Ingredient Reuse: {summary['ingredient_overlap_score']}")
    
    # Shopping list
    print("\n🛒 Top 10 Ingredients:")
    for idx, (ingredient, count) in enumerate(list(meal_plan['shopping_list'].items())[:10], 1):
        print(f"  {idx:2d}. {ingredient.title():25s} → Used {count}x")
    
    # Save
    with open('demo_output_1.json', 'w', encoding='utf-8') as f:
        json.dump(meal_plan, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Full plan saved to: demo_output_1.json")


def demo_scenario_2():
    """Demo 2: High-protein non-vegetarian"""
    print_section("DEMO 2: High-Protein Non-Vegetarian for Muscle Gain")
    
    ai = MealCraftAI("indian_food.csv")
    
    prefs = UserPreferences(
        diet="High-Protein",
        preferred_cuisines=[],
        daily_calorie_target=2500,
        weekly_budget=1500,
        preferred_flavors=["spicy"],
        cooking_time_limit=60,
        region="All",
        goals=["muscle gain", "high-protein"],
        cost_per_meal_limit=90
    )
    
    print("\n📋 User Profile:")
    print(f"   Diet: {prefs.diet}")
    print(f"   Daily Calories: {prefs.daily_calorie_target} (higher for muscle gain)")
    print(f"   Weekly Budget: ₹{prefs.weekly_budget}")
    print(f"   Goals: {', '.join(prefs.goals)}")
    
    print("\n⏳ Generating meal plan...")
    
    meal_plan = ai.generate_weekly_plan(prefs)
    
    # Summary
    print_section("WEEKLY SUMMARY")
    summary = meal_plan['summary']
    print(f"\n  💰 Total Cost: {summary['total_cost']}")
    print(f"  💪 Daily Avg Protein: {summary['daily_avg_protein']} (HIGH!)")
    print(f"  🔥 Daily Avg Calories: {summary['daily_avg_calories']} kcal")
    print(f"  📈 Budget Status: {summary['budget_status'].upper()}")
    
    # Show Wednesday meals as example
    wednesday = meal_plan['weekly_plan'][2]
    print(f"\n📅 Sample Day (Wednesday):")
    print(f"{'─' * 70}")
    for meal_type, meal in wednesday['meals'].items():
        print_meal(meal_type, meal)
    
    with open('demo_output_2.json', 'w', encoding='utf-8') as f:
        json.dump(meal_plan, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Full plan saved to: demo_output_2.json")


def demo_scenario_3():
    """Demo 3: Vegan South Indian"""
    print_section("DEMO 3: Vegan South Indian Plant-Based")
    
    ai = MealCraftAI("indian_food.csv")
    
    prefs = UserPreferences(
        diet="Vegan",
        preferred_cuisines=["South Indian"],
        daily_calorie_target=1800,
        weekly_budget=1100,
        preferred_flavors=["spicy", "sour"],
        cooking_time_limit=40,
        region="South",
        goals=["immunity", "energy"],
        cost_per_meal_limit=65
    )
    
    print("\n📋 User Profile:")
    print(f"   Diet: {prefs.diet} (No dairy, eggs, or animal products)")
    print(f"   Region: {prefs.region}")
    print(f"   Daily Calories: {prefs.daily_calorie_target}")
    print(f"   Weekly Budget: ₹{prefs.weekly_budget}")
    
    print("\n⏳ Generating meal plan...")
    
    meal_plan = ai.generate_weekly_plan(prefs)
    
    # Summary
    print_section("WEEKLY SUMMARY")
    summary = meal_plan['summary']
    print(f"\n  💰 Total Cost: {summary['total_cost']}")
    print(f"  🌱 100% Plant-Based: YES")
    print(f"  🔥 Daily Avg Calories: {summary['daily_avg_calories']} kcal")
    print(f"  💪 Daily Avg Protein: {summary['daily_avg_protein']} (from plants)")
    
    # Batch cooking
    print("\n👨‍🍳 Batch Cooking Tips:")
    for idx, suggestion in enumerate(meal_plan['batch_cooking_suggestions'][:3], 1):
        print(f"  {idx}. {suggestion}")
    
    with open('demo_output_3.json', 'w', encoding='utf-8') as f:
        json.dump(meal_plan, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Full plan saved to: demo_output_3.json")


def main():
    """Run all demos"""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  🍽️  MEALCRAFT-AI DEMONSTRATION".center(68) + "█")
    print("█" + "  Intelligent Indian Meal Planning System".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    print("\n\nThis demo will showcase 3 different meal planning scenarios:")
    print("  1. Budget-conscious vegetarian (₹1000/week)")
    print("  2. High-protein non-vegetarian (₹1500/week)")
    print("  3. Vegan South Indian (₹1100/week)")
    
    input("\n\nPress ENTER to start the demo...")
    
    try:
        # Run demos
        demo_scenario_1()
        input("\n\nPress ENTER for next demo...")
        
        demo_scenario_2()
        input("\n\nPress ENTER for next demo...")
        
        demo_scenario_3()
        
        # Final message
        print_section("DEMO COMPLETE!")
        print("\n  ✅ All 3 meal plans generated successfully!")
        print("\n  📄 Output files created:")
        print("     - demo_output_1.json (Budget Vegetarian)")
        print("     - demo_output_2.json (High-Protein)")
        print("     - demo_output_3.json (Vegan)")
        print("\n  🚀 Next steps:")
        print("     - Open the JSON files to see complete plans")
        print("     - Run: python mealcraft_cli.py (for interactive mode)")
        print("     - Run: jupyter notebook mealcraft_demo.ipynb (for visuals)")
        print("     - Run: python test_mealcraft.py (to test the system)")
        
        print("\n" + "=" * 70)
        print("  Thank you for trying MealCraft-AI! 🍛✨")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Installed dependencies: pip install -r requirements.txt")
        print("  2. indian_food.csv file in the current directory")
        print("  3. All required Python files in place")


if __name__ == "__main__":
    main()
