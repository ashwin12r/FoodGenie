"""
🍽️ Meal Combinations System
Defines realistic Indian meal combinations with complementary dishes.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import pandas as pd

@dataclass
class MealCombination:
    """Defines a complete meal combination"""
    main_dish: str
    main_course: str  # main course, snack, dessert
    accompaniments: List[str]  # What goes with it
    meal_types: List[str]  # breakfast, lunch, dinner
    region: str
    is_complete: bool = False  # If main_dish is already complete (like Chole Bhature)


class MealCombinationEngine:
    """
    Intelligently creates complete Indian meal combinations.
    
    Indian meals typically consist of:
    - Breakfast: Snack + Beverage (Idli + Sambar + Chutney)
    - Lunch: Rice/Roti + Gravy + Dry Sabzi + Dal + Pickle/Papad
    - Dinner: Similar to lunch but lighter
    """
    
    def __init__(self):
        self.combination_rules = self._define_combination_rules()
        self.accompaniment_priorities = self._define_accompaniments()
    
    def _define_combination_rules(self) -> Dict:
        """
        Define which dishes need accompaniments and what they need.
        """
        return {
            # Gravies that need rice/roti
            "gravies": {
                "dishes": [
                    "Sambar", "Rasam", "Kadhi", "Dal", "Rajma", "Chole", 
                    "Palak Paneer", "Paneer Butter Masala", "Butter Chicken",
                    "Chicken Curry", "Fish Curry", "Kuzhambu", "Kootu",
                    "Dal Makhani", "Dal Tadka", "Chana Masala", "Aloo Matar",
                    "Shahi Paneer", "Malai Kofta", "Mushroom Matar", "Kofta",
                    "Dalithoy", "Paruppu", "Mor Kuzhambu", "Vatha Kuzhambu"
                ],
                "needs": ["rice", "roti"],
                "optional": ["papad", "pickle", "raita"]
            },
            
            # Rice dishes (already complete but can have sides)
            "rice_dishes": {
                "dishes": [
                    "Biryani", "Pulao", "Pongal", "Lemon Rice", "Curd Rice",
                    "Tamarind Rice", "Coconut Rice", "Bisibelebath", "Khichdi",
                    "Thayir sadam", "Puli sadam", "Kothamali sadam", 
                    "Currivepillai sadam", "Paruppu sadam"
                ],
                "needs": [],  # Already complete
                "optional": ["papad", "pickle", "raita", "appalam"]
            },
            
            # Dry sabzis that need roti
            "dry_sabzi": {
                "dishes": [
                    "Aloo Gobi", "Bhindi Masala", "Baingan Bharta", "Poriyal",
                    "Thoran", "Palya", "Zunka", "Usal", "Keerai masiyal"
                ],
                "needs": ["roti"],
                "optional": ["dal", "rice"]
            },
            
            # Breakfast combinations
            "breakfast_with_gravy": {
                "dishes": ["Idli", "Dosa", "Uttapam", "Medu Vada", "Vada", "Pesarattu"],
                "needs": ["sambar", "chutney"],
                "optional": []
            },
            
            "breakfast_standalone": {
                "dishes": [
                    "Poha", "Upma", "Paratha", "Thepla", "Aloo Tikki",
                    "Kachori", "Samosa", "Dhokla", "Handvo"
                ],
                "needs": [],  # Can be eaten alone
                "optional": ["chutney", "pickle"]
            },
            
            # Complete combos (no additions needed)
            "complete_meals": {
                "dishes": [
                    "Chole Bhature", "Puri Bhaji", "Dosa Sambar", 
                    "Idli Sambar", "Thali", "Meals"
                ],
                "needs": [],
                "optional": []
            }
        }
    
    def _define_accompaniments(self) -> Dict:
        """
        Define common accompaniments and their properties.
        """
        return {
            # Bases (starches)
            "rice": {
                "names": ["Rice", "Steamed Rice", "Plain Rice", "Jeera Rice"],
                "cost": 10,
                "time": 20,
                "calories": 200,
                "protein": 4.0,
                "carbs": 45.0,
                "fat": 0.5,
                "course": "main course"
            },
            "roti": {
                "names": ["Roti", "Chapati", "Phulka"],
                "cost": 3,
                "time": 15,
                "calories": 80,
                "protein": 3.0,
                "carbs": 15.0,
                "fat": 1.0,
                "course": "main course",
                "quantity": "2 pieces"
            },
            "naan": {
                "names": ["Naan", "Butter Naan"],
                "cost": 15,
                "time": 20,
                "calories": 150,
                "protein": 4.0,
                "carbs": 25.0,
                "fat": 3.0,
                "course": "main course"
            },
            "paratha": {
                "names": ["Paratha", "Plain Paratha"],
                "cost": 12,
                "time": 20,
                "calories": 120,
                "protein": 3.5,
                "carbs": 20.0,
                "fat": 4.0,
                "course": "main course",
                "quantity": "2 pieces"
            },
            
            # Gravies for breakfast
            "sambar": {
                "names": ["Sambar", "Tiffin Sambar"],
                "cost": 15,
                "time": 30,
                "calories": 80,
                "protein": 4.0,
                "carbs": 12.0,
                "fat": 2.0,
                "course": "main course",
                "quantity": "1 bowl"
            },
            "chutney": {
                "names": ["Coconut Chutney", "Tomato Chutney", "Mint Chutney"],
                "cost": 5,
                "time": 10,
                "calories": 50,
                "protein": 1.0,
                "carbs": 6.0,
                "fat": 2.0,
                "course": "starter",
                "quantity": "1 small bowl"
            },
            
            # Sides
            "papad": {
                "names": ["Papad", "Papadum", "Appalam"],
                "cost": 2,
                "time": 2,
                "calories": 30,
                "protein": 1.0,
                "carbs": 5.0,
                "fat": 0.5,
                "course": "starter",
                "quantity": "2 pieces"
            },
            "pickle": {
                "names": ["Pickle", "Achar", "Lime Pickle", "Mango Pickle"],
                "cost": 3,
                "time": 0,
                "calories": 15,
                "protein": 0.3,
                "carbs": 1.0,
                "fat": 1.0,
                "course": "starter",
                "quantity": "1 tbsp"
            },
            "raita": {
                "names": ["Raita", "Cucumber Raita", "Boondi Raita"],
                "cost": 10,
                "time": 10,
                "calories": 60,
                "protein": 3.0,
                "carbs": 8.0,
                "fat": 2.0,
                "course": "starter",
                "quantity": "1 bowl"
            },
            "salad": {
                "names": ["Salad", "Kachumber", "Fresh Salad"],
                "cost": 8,
                "time": 5,
                "calories": 30,
                "protein": 1.0,
                "carbs": 6.0,
                "fat": 0.2,
                "course": "starter",
                "quantity": "1 bowl"
            }
        }
    
    def is_gravy_dish(self, dish_name: str) -> bool:
        """Check if dish is a gravy that needs rice/roti"""
        dish_lower = dish_name.lower()
        gravy_keywords = [d.lower() for d in self.combination_rules["gravies"]["dishes"]]
        return any(keyword in dish_lower or dish_lower in keyword for keyword in gravy_keywords)
    
    def is_rice_dish(self, dish_name: str) -> bool:
        """Check if dish is a rice-based dish"""
        dish_lower = dish_name.lower()
        rice_keywords = [d.lower() for d in self.combination_rules["rice_dishes"]["dishes"]]
        return any(keyword in dish_lower or dish_lower in keyword for keyword in rice_keywords)
    
    def is_dry_sabzi(self, dish_name: str) -> bool:
        """Check if dish is a dry vegetable dish"""
        dish_lower = dish_name.lower()
        sabzi_keywords = [d.lower() for d in self.combination_rules["dry_sabzi"]["dishes"]]
        return any(keyword in dish_lower or dish_lower in keyword for keyword in sabzi_keywords)
    
    def is_breakfast_with_gravy(self, dish_name: str) -> bool:
        """Check if breakfast dish needs sambar/chutney"""
        dish_lower = dish_name.lower()
        breakfast_keywords = [d.lower() for d in self.combination_rules["breakfast_with_gravy"]["dishes"]]
        return any(keyword in dish_lower or dish_lower in keyword for keyword in breakfast_keywords)
    
    def is_complete_meal(self, dish_name: str) -> bool:
        """Check if dish is already a complete meal"""
        dish_lower = dish_name.lower()
        complete_keywords = [d.lower() for d in self.combination_rules["complete_meals"]["dishes"]]
        return any(keyword in dish_lower or dish_lower in keyword for keyword in complete_keywords)
    
    def create_meal_combination(
        self, 
        main_dish: Dict,
        meal_type: str,  # breakfast, lunch, dinner
        user_budget_remaining: float,
        include_sides: bool = True
    ) -> Dict:
        """
        Create a complete meal combination based on the main dish.
        
        Args:
            main_dish: The primary dish (from dataset)
            meal_type: breakfast, lunch, or dinner
            user_budget_remaining: Remaining budget for this meal
            include_sides: Whether to include optional sides
        
        Returns:
            Complete meal combination with all components
        """
        dish_name = main_dish['dish']
        combination = {
            "main": main_dish,
            "accompaniments": [],
            "total_cost": main_dish['cost_value'],
            "total_calories": main_dish['calories_value'],
            "total_time": int(main_dish['time'].replace(' min', '')),
            "is_complete": False
        }
        
        # Check if it's already a complete meal
        if self.is_complete_meal(dish_name):
            combination["is_complete"] = True
            return combination
        
        # Breakfast combinations
        if meal_type == "breakfast":
            if self.is_breakfast_with_gravy(dish_name):
                # Add sambar and chutney
                sambar = self._create_accompaniment("sambar")
                chutney = self._create_accompaniment("chutney")
                
                if combination["total_cost"] + sambar["cost"] + chutney["cost"] <= user_budget_remaining:
                    combination["accompaniments"].extend([sambar, chutney])
                    combination["total_cost"] += sambar["cost"] + chutney["cost"]
                    combination["total_calories"] += sambar["calories"] + chutney["calories"]
                    combination["total_time"] = max(combination["total_time"], sambar["time"])
            else:
                # Standalone breakfast - optionally add chutney
                if include_sides:
                    chutney = self._create_accompaniment("chutney")
                    if combination["total_cost"] + chutney["cost"] <= user_budget_remaining:
                        combination["accompaniments"].append(chutney)
                        combination["total_cost"] += chutney["cost"]
                        combination["total_calories"] += chutney["calories"]
        
        # Lunch/Dinner combinations
        elif meal_type in ["lunch", "dinner"]:
            if self.is_gravy_dish(dish_name):
                # Gravy needs rice or roti
                base = self._create_accompaniment("rice")  # Default to rice
                if combination["total_cost"] + base["cost"] <= user_budget_remaining:
                    combination["accompaniments"].append(base)
                    combination["total_cost"] += base["cost"]
                    combination["total_calories"] += base["calories"]
                    combination["total_time"] = max(combination["total_time"], base["time"])
                    
                    # Add papad if budget allows
                    if include_sides:
                        papad = self._create_accompaniment("papad")
                        if combination["total_cost"] + papad["cost"] <= user_budget_remaining:
                            combination["accompaniments"].append(papad)
                            combination["total_cost"] += papad["cost"]
                            combination["total_calories"] += papad["calories"]
            
            elif self.is_dry_sabzi(dish_name):
                # Dry sabzi needs roti
                roti = self._create_accompaniment("roti")
                if combination["total_cost"] + roti["cost"] <= user_budget_remaining:
                    combination["accompaniments"].append(roti)
                    combination["total_cost"] += roti["cost"]
                    combination["total_calories"] += roti["calories"]
                    combination["total_time"] = max(combination["total_time"], roti["time"])
            
            elif self.is_rice_dish(dish_name):
                # Rice dish is complete, just add papad
                if include_sides:
                    papad = self._create_accompaniment("papad")
                    if combination["total_cost"] + papad["cost"] <= user_budget_remaining:
                        combination["accompaniments"].append(papad)
                        combination["total_cost"] += papad["cost"]
                        combination["total_calories"] += papad["calories"]
            
            else:
                # Other main courses - add rice by default
                rice = self._create_accompaniment("rice")
                if combination["total_cost"] + rice["cost"] <= user_budget_remaining:
                    combination["accompaniments"].append(rice)
                    combination["total_cost"] += rice["cost"]
                    combination["total_calories"] += rice["calories"]
                    combination["total_time"] = max(combination["total_time"], rice["time"])
        
        return combination
    
    def _create_accompaniment(self, accompaniment_type: str) -> Dict:
        """Create an accompaniment dish object"""
        acc = self.accompaniment_priorities[accompaniment_type]
        return {
            "name": acc["names"][0],
            "cost": acc["cost"],
            "time": acc["time"],
            "calories": acc["calories"],
            "protein": acc["protein"],
            "carbs": acc["carbs"],
            "fat": acc["fat"],
            "quantity": acc.get("quantity", "1 serving")
        }
    
    def format_combination_for_display(self, combination: Dict) -> str:
        """
        Format meal combination for display.
        
        Returns:
            "Sambar + Rice + Papad" or "Idli + Sambar + Chutney"
        """
        parts = [combination["main"]["dish"]]
        
        for acc in combination["accompaniments"]:
            parts.append(acc["name"])
        
        return " + ".join(parts)
    
    def get_combination_nutrition(self, combination: Dict) -> Dict:
        """Calculate total nutrition for the combination"""
        total_protein = combination["main"].get("protein", "0g")
        total_carbs = combination["main"].get("carbs", "0g")
        total_fat = combination["main"].get("fat", "0g")
        
        # Parse main dish values
        protein = float(total_protein.replace('g', ''))
        carbs = float(total_carbs.replace('g', ''))
        fat = float(total_fat.replace('g', ''))
        
        # Add accompaniments
        for acc in combination["accompaniments"]:
            protein += acc["protein"]
            carbs += acc["carbs"]
            fat += acc["fat"]
        
        return {
            "calories": combination["total_calories"],
            "protein": round(protein, 1),
            "carbs": round(carbs, 1),
            "fat": round(fat, 1),
            "cost": combination["total_cost"],
            "time": combination["total_time"]
        }


# Example usage
if __name__ == "__main__":
    engine = MealCombinationEngine()
    
    # Test with a sample dish
    sample_dish = {
        "dish": "Sambar",
        "cost": "₹20.0",
        "cost_value": 20.0,
        "calories": "150 kcal",
        "calories_value": 150,
        "protein": "8.0g",
        "carbs": "25.0g",
        "fat": "3.0g",
        "time": "30 min"
    }
    
    combination = engine.create_meal_combination(sample_dish, "lunch", 75)
    print("Complete Meal:", engine.format_combination_for_display(combination))
    print("Nutrition:", engine.get_combination_nutrition(combination))
