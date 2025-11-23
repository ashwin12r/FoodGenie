"""
Interactive command-line interface for MealCraft-AI
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json
from typing import Dict


class MealCraftCLI:
    """Command-line interface for meal planning"""
    
    def __init__(self):
        self.ai = MealCraftAI("indian_food_healthy.csv")
        
    def run(self):
        """Main CLI loop"""
        print("=" * 70)
        print("🍽️  WELCOME TO MEALCRAFT-AI")
        print("   Your Intelligent Indian Meal Planning Assistant")
        print("=" * 70)
        print()
        
        user_prefs = self.gather_user_input()
        
        print("\n🤖 Generating your personalized meal plan...")
        print("⏳ This may take a few seconds...\n")
        
        meal_plan = self.ai.generate_weekly_plan(user_prefs)
        
        if "error" in meal_plan:
            print(f"❌ Error: {meal_plan['error']}")
            return
        
        self.display_meal_plan(meal_plan)
        self.save_meal_plan(meal_plan)
        
    def gather_user_input(self) -> UserPreferences:
        """Interactive input gathering"""
        print("📋 Please provide your preferences:\n")
        
        # Diet
        print("1️⃣  DIETARY PREFERENCE")
        print("   Options: Vegetarian, Non-Vegetarian, Vegan, Jain,")
        print("            Gluten-Free, Keto, High-Protein, Low-Carb")
        diet = input("   Your choice: ").strip() or "Vegetarian"
        
        # Region
        print("\n2️⃣  REGIONAL PREFERENCE")
        print("   Options: North, South, East, West, North East, Central, All")
        region = input("   Your choice: ").strip() or "North"
        
        # Daily calories
        print("\n3️⃣  DAILY CALORIE TARGET")
        daily_calories = input("   Enter target (default 2000): ").strip()
        daily_calories = int(daily_calories) if daily_calories else 2000
        
        # Weekly budget
        print("\n4️⃣  WEEKLY FOOD BUDGET (INR)")
        weekly_budget = input("   Enter budget (default 1200): ").strip()
        weekly_budget = float(weekly_budget) if weekly_budget else 1200
        
        # Cost per meal limit
        print("\n5️⃣  COST PER MEAL LIMIT (INR)")
        cost_per_meal = input("   Enter limit (default 75): ").strip()
        cost_per_meal = float(cost_per_meal) if cost_per_meal else 75
        
        # Cooking time
        print("\n6️⃣  COOKING TIME LIMIT (minutes)")
        cooking_time = input("   Enter limit (default 45): ").strip()
        cooking_time = int(cooking_time) if cooking_time else 45
        
        # Flavor preferences
        print("\n7️⃣  FLAVOR PREFERENCES")
        print("   Options: spicy, mild, sweet, sour, bitter")
        flavors_input = input("   Enter flavors (comma-separated): ").strip()
        flavors = [f.strip() for f in flavors_input.split(',')] if flavors_input else ["spicy", "mild"]
        
        # Goals
        print("\n8️⃣  HEALTH GOALS")
        print("   Options: weight loss, muscle gain, energy, immunity")
        goals_input = input("   Enter goals (comma-separated): ").strip()
        goals = [g.strip() for g in goals_input.split(',')] if goals_input else []
        
        return UserPreferences(
            diet=diet,
            preferred_cuisines=[],
            daily_calorie_target=daily_calories,
            weekly_budget=weekly_budget,
            preferred_flavors=flavors,
            cooking_time_limit=cooking_time,
            region=region,
            goals=goals,
            cost_per_meal_limit=cost_per_meal
        )
    
    def display_meal_plan(self, meal_plan: Dict):
        """Display meal plan in a formatted way"""
        print("\n" + "=" * 70)
        print("📅 YOUR 7-DAY MEAL PLAN")
        print("=" * 70)
        
        for day_plan in meal_plan['weekly_plan']:
            print(f"\n{'─' * 70}")
            print(f"📆 {day_plan['day'].upper()}")
            print(f"{'─' * 70}")
            
            for meal_type, meal in day_plan['meals'].items():
                print(f"\n  🍴 {meal_type.upper()}")
                print(f"     Dish: {meal['dish']}")
                print(f"     Time: {meal['time']} | Cost: {meal['cost']}")
                print(f"     Nutrition: {meal['calories']} | Protein: {meal['protein']} | Carbs: {meal['carbs']} | Fat: {meal['fat']}")
                print(f"     Why: {meal['reason']}")
        
        # Summary
        summary = meal_plan['summary']
        print(f"\n\n{'=' * 70}")
        print("📊 WEEKLY SUMMARY")
        print(f"{'=' * 70}")
        print(f"  💰 Total Cost: {summary['total_cost']} (Budget: {summary['weekly_budget']})")
        print(f"  📈 Budget Status: {summary['budget_status'].upper()}")
        print(f"  🍽️  Avg Cost/Meal: {summary['avg_cost_per_meal']}")
        print(f"  🔥 Daily Avg Calories: {summary['daily_avg_calories']} kcal")
        print(f"  💪 Daily Avg Protein: {summary['daily_avg_protein']}")
        print(f"  🎯 Calorie Accuracy: {summary['calorie_balance_accuracy']}")
        print(f"  ♻️  Ingredient Reuse: {summary['ingredient_overlap_score']}")
        
        # Shopping list
        if 'shopping_list' in meal_plan:
            print(f"\n\n{'=' * 70}")
            print("🛒 TOP INGREDIENTS TO BUY")
            print(f"{'=' * 70}")
            for idx, (ingredient, count) in enumerate(list(meal_plan['shopping_list'].items())[:15], 1):
                print(f"  {idx:2d}. {ingredient.title()} (used {count}x)")
        
        # Batch cooking
        if meal_plan.get('batch_cooking_suggestions'):
            print(f"\n\n{'=' * 70}")
            print("👨‍🍳 BATCH COOKING TIPS")
            print(f"{'=' * 70}")
            for idx, suggestion in enumerate(meal_plan['batch_cooking_suggestions'], 1):
                print(f"  {idx}. {suggestion}")
        
        print("\n" + "=" * 70)
    
    def save_meal_plan(self, meal_plan: Dict):
        """Save meal plan to JSON file"""
        filename = 'my_meal_plan.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(meal_plan, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Meal plan saved to: {filename}")
        print("📄 You can open this file to view your complete plan anytime!")


def main():
    """Run the CLI"""
    cli = MealCraftCLI()
    cli.run()


if __name__ == "__main__":
    main()
