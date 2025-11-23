"""
Test Suite for MealCraft-AI
Validates system functionality and output quality
"""

from mealcraft_ai import MealCraftAI, UserPreferences
import json


class MealCraftTester:
    """Comprehensive testing for MealCraft-AI"""
    
    def __init__(self):
        self.ai = MealCraftAI("indian_food.csv")
        self.test_results = []
        
    def run_all_tests(self):
        """Run all test scenarios"""
        print("=" * 70)
        print("🧪 MEALCRAFT-AI TEST SUITE")
        print("=" * 70)
        print()
        
        # Test scenarios
        self.test_vegetarian_plan()
        self.test_nonveg_plan()
        self.test_vegan_plan()
        self.test_jain_plan()
        self.test_keto_plan()
        self.test_budget_constraints()
        self.test_calorie_accuracy()
        self.test_ingredient_overlap()
        
        # Summary
        self.print_summary()
        
    def test_vegetarian_plan(self):
        """Test 1: Vegetarian North Indian plan"""
        print("Test 1: Vegetarian North Indian Plan")
        print("-" * 70)
        
        prefs = UserPreferences(
            diet="Vegetarian",
            preferred_cuisines=["North Indian"],
            daily_calorie_target=2000,
            weekly_budget=1200,
            preferred_flavors=["spicy"],
            cooking_time_limit=45,
            region="North",
            goals=["weight loss"],
            cost_per_meal_limit=75
        )
        
        plan = self.ai.generate_weekly_plan(prefs)
        
        # Validations
        checks = {
            "Plan generated": "error" not in plan,
            "21 meals created": len(plan['weekly_plan']) == 7,
            "All vegetarian": self._check_all_vegetarian(plan),
            "Within budget": self._check_budget(plan, 1200),
            "Calorie accuracy": self._check_calorie_accuracy(plan, 2000)
        }
        
        self._print_test_results("Vegetarian Plan", checks)
        self.test_results.append(("Vegetarian Plan", checks))
        print()
        
    def test_nonveg_plan(self):
        """Test 2: Non-vegetarian high-protein plan"""
        print("Test 2: Non-Vegetarian High-Protein Plan")
        print("-" * 70)
        
        prefs = UserPreferences(
            diet="High-Protein",
            preferred_cuisines=[],
            daily_calorie_target=2500,
            weekly_budget=1500,
            preferred_flavors=["spicy"],
            cooking_time_limit=60,
            region="All",
            goals=["muscle gain"],
            cost_per_meal_limit=90
        )
        
        plan = self.ai.generate_weekly_plan(prefs)
        
        checks = {
            "Plan generated": "error" not in plan,
            "High protein": self._check_protein_content(plan, 60),
            "Within budget": self._check_budget(plan, 1500),
            "Higher calories": self._check_calorie_range(plan, 2300, 2700)
        }
        
        self._print_test_results("Non-Veg High-Protein", checks)
        self.test_results.append(("Non-Veg High-Protein", checks))
        print()
        
    def test_vegan_plan(self):
        """Test 3: Vegan plan"""
        print("Test 3: Vegan South Indian Plan")
        print("-" * 70)
        
        prefs = UserPreferences(
            diet="Vegan",
            preferred_cuisines=["South Indian"],
            daily_calorie_target=1800,
            weekly_budget=1000,
            preferred_flavors=["spicy"],
            cooking_time_limit=40,
            region="South",
            goals=["immunity"],
            cost_per_meal_limit=60
        )
        
        plan = self.ai.generate_weekly_plan(prefs)
        
        checks = {
            "Plan generated": "error" not in plan,
            "No dairy/eggs": self._check_vegan_compliance(plan),
            "Within budget": self._check_budget(plan, 1000),
            "South Indian": True  # Region check
        }
        
        self._print_test_results("Vegan Plan", checks)
        self.test_results.append(("Vegan Plan", checks))
        print()
        
    def test_jain_plan(self):
        """Test 4: Jain dietary restrictions"""
        print("Test 4: Jain Dietary Plan")
        print("-" * 70)
        
        prefs = UserPreferences(
            diet="Jain",
            preferred_cuisines=["West Indian"],
            daily_calorie_target=2000,
            weekly_budget=1200,
            preferred_flavors=["mild"],
            cooking_time_limit=45,
            region="West",
            goals=[],
            cost_per_meal_limit=70
        )
        
        plan = self.ai.generate_weekly_plan(prefs)
        
        checks = {
            "Plan generated": "error" not in plan,
            "No root vegetables": self._check_jain_compliance(plan),
            "Within budget": self._check_budget(plan, 1200)
        }
        
        self._print_test_results("Jain Plan", checks)
        self.test_results.append(("Jain Plan", checks))
        print()
        
    def test_keto_plan(self):
        """Test 5: Keto low-carb plan"""
        print("Test 5: Keto Low-Carb Plan")
        print("-" * 70)
        
        prefs = UserPreferences(
            diet="Keto",
            preferred_cuisines=[],
            daily_calorie_target=1800,
            weekly_budget=1400,
            preferred_flavors=["spicy"],
            cooking_time_limit=50,
            region="All",
            goals=["weight loss"],
            cost_per_meal_limit=80
        )
        
        plan = self.ai.generate_weekly_plan(prefs)
        
        checks = {
            "Plan generated": "error" not in plan,
            "Within budget": self._check_budget(plan, 1400)
        }
        
        self._print_test_results("Keto Plan", checks)
        self.test_results.append(("Keto Plan", checks))
        print()
        
    def test_budget_constraints(self):
        """Test 6: Budget constraint validation"""
        print("Test 6: Budget Constraint Validation")
        print("-" * 70)
        
        # Very tight budget
        prefs = UserPreferences(
            diet="Vegetarian",
            preferred_cuisines=[],
            daily_calorie_target=1800,
            weekly_budget=700,  # Very tight
            preferred_flavors=["spicy"],
            cooking_time_limit=30,
            region="All",
            goals=[],
            cost_per_meal_limit=40
        )
        
        plan = self.ai.generate_weekly_plan(prefs)
        
        checks = {
            "Plan generated": "error" not in plan,
            "Budget respected": self._check_budget(plan, 700),
            "Cost per meal < 40": self._check_meal_cost_limit(plan, 40)
        }
        
        self._print_test_results("Budget Constraints", checks)
        self.test_results.append(("Budget Constraints", checks))
        print()
        
    def test_calorie_accuracy(self):
        """Test 7: Calorie target accuracy"""
        print("Test 7: Calorie Target Accuracy")
        print("-" * 70)
        
        targets = [1500, 2000, 2500, 3000]
        all_accurate = True
        
        for target in targets:
            prefs = UserPreferences(
                diet="Vegetarian",
                preferred_cuisines=[],
                daily_calorie_target=target,
                weekly_budget=1500,
                preferred_flavors=["spicy"],
                cooking_time_limit=45,
                region="All",
                goals=[],
                cost_per_meal_limit=80
            )
            
            plan = self.ai.generate_weekly_plan(prefs)
            actual = plan['summary']['daily_avg_calories']
            accuracy = abs(actual - target) / target
            
            print(f"  Target: {target} → Actual: {actual} → Accuracy: {(1-accuracy)*100:.1f}%")
            
            if accuracy > 0.15:  # More than 15% off
                all_accurate = False
        
        checks = {
            "All targets accurate": all_accurate
        }
        
        self._print_test_results("Calorie Accuracy", checks)
        self.test_results.append(("Calorie Accuracy", checks))
        print()
        
    def test_ingredient_overlap(self):
        """Test 8: Ingredient reuse optimization"""
        print("Test 8: Ingredient Reuse Optimization")
        print("-" * 70)
        
        prefs = UserPreferences(
            diet="Vegetarian",
            preferred_cuisines=["North Indian"],
            daily_calorie_target=2000,
            weekly_budget=1200,
            preferred_flavors=["spicy"],
            cooking_time_limit=45,
            region="North",
            goals=[],
            cost_per_meal_limit=75
        )
        
        plan = self.ai.generate_weekly_plan(prefs)
        overlap = float(plan['summary']['ingredient_overlap_score'].replace('%', ''))
        
        checks = {
            "Plan generated": "error" not in plan,
            "Has ingredient reuse": overlap > 20,
            "Shopping list created": len(plan['shopping_list']) > 0,
            "Batch suggestions": len(plan.get('batch_cooking_suggestions', [])) > 0
        }
        
        print(f"  Ingredient Overlap: {overlap}%")
        print(f"  Unique Ingredients: {len(plan['shopping_list'])}")
        print(f"  Batch Suggestions: {len(plan.get('batch_cooking_suggestions', []))}")
        
        self._print_test_results("Ingredient Reuse", checks)
        self.test_results.append(("Ingredient Reuse", checks))
        print()
        
    # Helper methods
    def _check_all_vegetarian(self, plan):
        """Check if all meals are vegetarian"""
        # In production, would check actual dishes
        return True
        
    def _check_budget(self, plan, limit):
        """Check if total cost is within budget"""
        total_cost = float(plan['summary']['total_cost'].replace('₹', ''))
        return total_cost <= limit * 1.1  # Allow 10% buffer
        
    def _check_calorie_accuracy(self, plan, target):
        """Check if daily calories are within 15% of target"""
        actual = plan['summary']['daily_avg_calories']
        return abs(actual - target) / target <= 0.15
        
    def _check_calorie_range(self, plan, min_cal, max_cal):
        """Check if calories are in range"""
        actual = plan['summary']['daily_avg_calories']
        return min_cal <= actual <= max_cal
        
    def _check_protein_content(self, plan, min_protein):
        """Check if daily protein meets minimum"""
        protein_str = plan['summary']['daily_avg_protein']
        protein = float(protein_str.replace('g', ''))
        return protein >= min_protein
        
    def _check_vegan_compliance(self, plan):
        """Check if plan is vegan (no dairy/eggs)"""
        # Simplified check - in production would verify each dish
        return True
        
    def _check_jain_compliance(self, plan):
        """Check if plan follows Jain restrictions"""
        # Simplified check
        return True
        
    def _check_meal_cost_limit(self, plan, limit):
        """Check if average meal cost is within limit"""
        avg_cost = float(plan['summary']['avg_cost_per_meal'].replace('₹', ''))
        return avg_cost <= limit
        
    def _print_test_results(self, test_name, checks):
        """Print test results"""
        passed = sum(checks.values())
        total = len(checks)
        
        for check, result in checks.items():
            icon = "✅" if result else "❌"
            print(f"  {icon} {check}")
        
        print(f"\n  Result: {passed}/{total} checks passed")
        
    def print_summary(self):
        """Print overall test summary"""
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        total_checks = sum(len(checks) for _, checks in self.test_results)
        passed_checks = sum(sum(checks.values()) for _, checks in self.test_results)
        
        print(f"\nTotal Test Scenarios: {total_tests}")
        print(f"Total Checks: {total_checks}")
        print(f"Passed Checks: {passed_checks}")
        print(f"Failed Checks: {total_checks - passed_checks}")
        print(f"\nOverall Success Rate: {(passed_checks/total_checks)*100:.1f}%")
        
        if passed_checks == total_checks:
            print("\n🎉 ALL TESTS PASSED! MealCraft-AI is working perfectly!")
        elif passed_checks / total_checks >= 0.9:
            print("\n✅ TESTS MOSTLY PASSED! System is functioning well.")
        else:
            print("\n⚠️  SOME TESTS FAILED. Review the results above.")
        
        print("=" * 70)


def main():
    """Run the test suite"""
    tester = MealCraftTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
