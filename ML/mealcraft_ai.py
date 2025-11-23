"""
MealCraft-AI: Intelligent Indian Meal Planning System
A deterministic ML-powered meal planner optimized for Indian cuisine,
regional availability, nutritional goals, and budget constraints.
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
from meal_combinations import MealCombinationEngine

# Import real-time price scraper (optional)
try:
    from grocery_price_scraper import RealTimeCostEstimator
    REALTIME_PRICES_AVAILABLE = True
except ImportError as e:
    REALTIME_PRICES_AVAILABLE = False
    print(f">> Note: Real-time price scraper dependencies missing: {e}")
    print(">> Install with: pip install beautifulsoup4 requests geocoder")
except Exception as e:
    REALTIME_PRICES_AVAILABLE = False
    print(f">> Note: Real-time price scraper import failed: {e}")

# Import Chennai local grocery scraper (PREFERRED - Grace Daily & KPN Fresh)
try:
    from local_grocery_scraper import ChennaiCostEstimator
    CHENNAI_SCRAPER_AVAILABLE = True
    print(">> Chennai local scraper loaded (Grace Daily & KPN Fresh)")
except Exception as e:
    CHENNAI_SCRAPER_AVAILABLE = False
    print(f">> Note: Chennai scraper not available: {e}")

# Import Bright Data scraper (fallback for BigBasket/Zepto/Swiggy)
try:
    from brightdata_scraper import BrightDataCostEstimator
    BRIGHTDATA_AVAILABLE = True
except Exception as e:
    BRIGHTDATA_AVAILABLE = False
    print(f">> Note: Bright Data scraper not available: {e}")


@dataclass
class UserPreferences:
    """User dietary preferences and constraints"""
    diet: str
    preferred_cuisines: List[str]
    daily_calorie_target: int
    weekly_budget: float
    preferred_flavors: List[str]
    cooking_time_limit: int
    region: str
    goals: List[str]
    cost_per_meal_limit: float


class NutritionEstimator:
    """Estimates nutritional values for Indian dishes"""
    
    # Approximate nutrition database (per 100g serving)
    INGREDIENT_NUTRITION = {
        # Grains & Flours
        "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
        "wheat flour": {"calories": 340, "protein": 10, "carbs": 72, "fat": 1.5},
        "atta": {"calories": 340, "protein": 10, "carbs": 72, "fat": 1.5},
        "maida": {"calories": 364, "protein": 10, "carbs": 76, "fat": 1},
        "semolina": {"calories": 360, "protein": 12, "carbs": 72, "fat": 1},
        "rava": {"calories": 360, "protein": 12, "carbs": 72, "fat": 1},
        
        # Proteins
        "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
        "fish": {"calories": 120, "protein": 20, "carbs": 0, "fat": 5},
        "paneer": {"calories": 265, "protein": 18, "carbs": 1.2, "fat": 20},
        "chhena": {"calories": 265, "protein": 18, "carbs": 1.2, "fat": 20},
        "cottage cheese": {"calories": 265, "protein": 18, "carbs": 1.2, "fat": 20},
        "egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11},
        "mutton": {"calories": 294, "protein": 25, "carbs": 0, "fat": 21},
        "beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15},
        "pork": {"calories": 242, "protein": 27, "carbs": 0, "fat": 14},
        "prawns": {"calories": 99, "protein": 24, "carbs": 0.2, "fat": 0.3},
        
        # Legumes
        "dal": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.4},
        "moong dal": {"calories": 347, "protein": 24, "carbs": 63, "fat": 1.2},
        "arhar dal": {"calories": 343, "protein": 22, "carbs": 62, "fat": 1.5},
        "urad dal": {"calories": 341, "protein": 25, "carbs": 59, "fat": 1.6},
        "chana dal": {"calories": 360, "protein": 22, "carbs": 60, "fat": 6},
        "chickpeas": {"calories": 164, "protein": 9, "carbs": 27, "fat": 2.6},
        "kidney beans": {"calories": 127, "protein": 8.7, "carbs": 23, "fat": 0.5},
        
        # Vegetables
        "potato": {"calories": 77, "protein": 2, "carbs": 17, "fat": 0.1},
        "aloo": {"calories": 77, "protein": 2, "carbs": 17, "fat": 0.1},
        "tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2},
        "onion": {"calories": 40, "protein": 1.1, "carbs": 9, "fat": 0.1},
        "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
        "palak": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
        "cauliflower": {"calories": 25, "protein": 1.9, "carbs": 5, "fat": 0.3},
        "gobi": {"calories": 25, "protein": 1.9, "carbs": 5, "fat": 0.3},
        "carrot": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2},
        "beans": {"calories": 31, "protein": 1.8, "carbs": 7, "fat": 0.1},
        "peas": {"calories": 81, "protein": 5, "carbs": 14, "fat": 0.4},
        "bottle gourd": {"calories": 14, "protein": 0.6, "carbs": 3.4, "fat": 0.0},
        "brinjal": {"calories": 25, "protein": 1, "carbs": 6, "fat": 0.2},
        "mushroom": {"calories": 22, "protein": 3.1, "carbs": 3.3, "fat": 0.3},
        
        # Dairy
        "milk": {"calories": 42, "protein": 3.4, "carbs": 5, "fat": 1},
        "curd": {"calories": 60, "protein": 3.5, "carbs": 4.7, "fat": 3.3},
        "yogurt": {"calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
        "cream": {"calories": 195, "protein": 2.2, "carbs": 4.3, "fat": 19},
        "butter": {"calories": 717, "protein": 0.9, "carbs": 0.1, "fat": 81},
        "ghee": {"calories": 900, "protein": 0, "carbs": 0, "fat": 100},
        
        # Oils & Fats
        "oil": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100},
        "coconut oil": {"calories": 862, "protein": 0, "carbs": 0, "fat": 100},
        
        # Sweeteners
        "sugar": {"calories": 387, "protein": 0, "carbs": 100, "fat": 0},
        "jaggery": {"calories": 383, "protein": 0.4, "carbs": 98, "fat": 0.1},
        "gur": {"calories": 383, "protein": 0.4, "carbs": 98, "fat": 0.1},
        
        # Nuts
        "cashew": {"calories": 553, "protein": 18, "carbs": 30, "fat": 44},
        "almond": {"calories": 579, "protein": 21, "carbs": 22, "fat": 50},
        "peanut": {"calories": 567, "protein": 26, "carbs": 16, "fat": 49},
    }
    
    # Average portion sizes for Indian courses (in grams)
    PORTION_SIZES = {
        "breakfast": 250,
        "lunch": 400,
        "dinner": 350,
        "snack": 150,
        "dessert": 100,
        "main course": 350,
        "starter": 150
    }
    
    @staticmethod
    def estimate_nutrition(ingredients: str, course: str) -> Dict[str, float]:
        """Estimate calories and macros from ingredients"""
        ingredients_lower = ingredients.lower()
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        matched_ingredients = 0
        
        for ingredient, nutrition in NutritionEstimator.INGREDIENT_NUTRITION.items():
            if ingredient in ingredients_lower:
                # Weight ingredients based on typical quantities
                weight_factor = 0.3 if ingredient in ["oil", "ghee", "butter"] else 1.0
                total_calories += nutrition["calories"] * weight_factor
                total_protein += nutrition["protein"] * weight_factor
                total_carbs += nutrition["carbs"] * weight_factor
                total_fat += nutrition["fat"] * weight_factor
                matched_ingredients += 1
        
        # If no ingredients matched, use course-based defaults
        if matched_ingredients == 0:
            defaults = NutritionEstimator._get_default_nutrition(course)
            return defaults
        
        # Normalize based on portion size
        portion = NutritionEstimator.PORTION_SIZES.get(course, 300)
        normalization_factor = portion / (matched_ingredients * 100)
        
        return {
            "calories": round(total_calories * normalization_factor, 0),
            "protein": round(total_protein * normalization_factor, 1),
            "carbs": round(total_carbs * normalization_factor, 1),
            "fat": round(total_fat * normalization_factor, 1)
        }
    
    @staticmethod
    def _get_default_nutrition(course: str) -> Dict[str, float]:
        """Default nutrition values by course type"""
        defaults = {
            "breakfast": {"calories": 350, "protein": 10, "carbs": 55, "fat": 8},
            "snack": {"calories": 200, "protein": 5, "carbs": 30, "fat": 6},
            "main course": {"calories": 450, "protein": 15, "carbs": 60, "fat": 12},
            "dessert": {"calories": 250, "protein": 4, "carbs": 45, "fat": 6},
            "starter": {"calories": 180, "protein": 8, "carbs": 20, "fat": 7}
        }
        return defaults.get(course, {"calories": 350, "protein": 10, "carbs": 50, "fat": 10})


class CostEstimator:
    """Estimates meal costs based on ingredient complexity"""
    
    # Base cost factors per ingredient category (in INR)
    INGREDIENT_COSTS = {
        # Proteins (expensive)
        "chicken": 15, "fish": 18, "paneer": 12, "chhena": 10, "cottage cheese": 12,
        "mutton": 25, "beef": 20, "pork": 18, "prawns": 30, "egg": 6,
        
        # Grains (cheap)
        "rice": 2, "wheat flour": 1.5, "atta": 1.5, "maida": 1.5, 
        "semolina": 2, "rava": 2,
        
        # Legumes (moderate)
        "dal": 3, "moong dal": 3, "arhar dal": 3, "urad dal": 3.5,
        "chana dal": 3, "chickpeas": 3, "kidney beans": 3,
        
        # Vegetables (cheap to moderate)
        "potato": 1, "aloo": 1, "tomato": 1.5, "onion": 1,
        "spinach": 1.5, "palak": 1.5, "cauliflower": 2, "gobi": 2,
        "carrot": 1.5, "beans": 2, "peas": 2.5,
        
        # Dairy (moderate)
        "milk": 2, "curd": 2, "yogurt": 2.5, "cream": 5, 
        "butter": 8, "ghee": 10,
        
        # Nuts & Premium ingredients (expensive)
        "cashew": 15, "almond": 18, "pistachio": 20, "saffron": 50,
        "khoa": 12, "mawa": 12,
        
        # Sweeteners (cheap)
        "sugar": 1.5, "jaggery": 2, "gur": 2,
        
        # Oils & spices (moderate)
        "oil": 2, "ghee": 10, "garam masala": 3,
    }
    
    @staticmethod
    def estimate_cost(ingredients: str, cook_time: int, prep_time: int) -> float:
        """Estimate meal cost based on ingredients and complexity"""
        ingredients_lower = ingredients.lower()
        total_cost = 0
        matched_count = 0
        
        for ingredient, cost in CostEstimator.INGREDIENT_COSTS.items():
            if ingredient in ingredients_lower:
                total_cost += cost
                matched_count += 1
        
        # Base cost if no matches (simple dish)
        if matched_count == 0:
            total_cost = 30
        
        # Add complexity premium for longer cooking
        time_premium = ((cook_time + prep_time) / 60) * 5
        
        # Count number of ingredients (proxy for complexity)
        ingredient_count = len(ingredients.split(','))
        complexity_premium = ingredient_count * 1.5
        
        final_cost = total_cost + time_premium + complexity_premium
        return round(max(15, min(final_cost, 150)), 2)  # Cap between 15-150 INR


class MealScorer:
    """Scores meals based on multiple criteria"""
    
    @staticmethod
    def score_meal(
        dish: pd.Series,
        user_prefs: UserPreferences,
        nutrition: Dict[str, float],
        cost: float,
        ingredient_pool: List[str]
    ) -> float:
        """
        Calculate composite score for a meal
        Higher score = better match
        """
        score = 100.0
        
        # 1. Cost Score (30% weight) - prefer cheaper meals
        cost_score = max(0, (user_prefs.cost_per_meal_limit - cost) / user_prefs.cost_per_meal_limit * 100)
        
        # 2. Time Score (20% weight)
        total_time = dish['prep_time'] + dish['cook_time']
        if total_time <= 0:
            total_time = 30  # Default if missing
        time_score = max(0, (user_prefs.cooking_time_limit - total_time) / user_prefs.cooking_time_limit * 100)
        time_score = min(100, time_score)
        
        # 3. Nutrition Score (25% weight) - match calorie goals
        calorie_target = user_prefs.daily_calorie_target / 3  # Per meal
        calorie_diff = abs(nutrition['calories'] - calorie_target)
        nutrition_score = max(0, 100 - (calorie_diff / calorie_target * 100))
        
        # 4. Protein Score (15% weight) - boost for high protein goals
        protein_bonus = 0
        if any(goal in ["muscle gain", "weight loss", "high-protein"] for goal in user_prefs.goals):
            if nutrition['protein'] >= 15:
                protein_bonus = 20
            elif nutrition['protein'] >= 10:
                protein_bonus = 10
        
        # 5. Flavor Match (10% weight)
        flavor_score = 0
        if pd.notna(dish['flavor_profile']):
            if dish['flavor_profile'] in user_prefs.preferred_flavors:
                flavor_score = 100
            else:
                flavor_score = 50
        else:
            flavor_score = 50
        
        # 6. Ingredient Reuse Bonus
        reuse_bonus = 0
        dish_ingredients = set(dish['ingredients'].lower().split(','))
        for pool_ingredient in ingredient_pool:
            if any(pool_ingredient in ing for ing in dish_ingredients):
                reuse_bonus += 5
        reuse_bonus = min(reuse_bonus, 20)
        
        # Weighted composite score
        final_score = (
            cost_score * 0.30 +
            time_score * 0.20 +
            nutrition_score * 0.25 +
            flavor_score * 0.10 +
            protein_bonus +
            reuse_bonus
        )
        
        return final_score


class MealCraftAI:
    """Main meal planning AI system"""
    
    def __init__(self, dataset_path: str = "indian_food_healthy.csv", use_healthy_mode: bool = True, use_meal_combinations: bool = True, use_realtime_prices: bool = False, location: str = None):
        """
        Initialize with Indian food dataset
        
        Args:
            dataset_path: Path to the CSV dataset (default: indian_food_healthy.csv with better breakfast classification)
            use_healthy_mode: If True, filters for health-focused meals (default: True)
            use_meal_combinations: If True, creates complete meal combinations (Sambar + Rice + Papad) (default: True)
            use_realtime_prices: If True, fetches live prices from Chennai grocery stores (default: False)
            location: User location for price fetching (city name, e.g., "Chennai", "Mumbai")
        """
        self.df = pd.read_csv(dataset_path)
        self.use_healthy_mode = use_healthy_mode
        self.use_meal_combinations = use_meal_combinations
        self.use_realtime_prices = use_realtime_prices
        
        # Initialize real-time price estimator (prefer Chennai local stores)
        if use_realtime_prices:
            if CHENNAI_SCRAPER_AVAILABLE:
                self.realtime_cost_estimator = ChennaiCostEstimator(location or "Chennai")
                print(">> Using Chennai local stores (Grace Daily & KPN Fresh) for real-time prices!")
            elif BRIGHTDATA_AVAILABLE:
                self.realtime_cost_estimator = BrightDataCostEstimator(location or "Chennai")
                print(">> Using Bright Data for real-time prices!")
            elif REALTIME_PRICES_AVAILABLE:
                self.realtime_cost_estimator = RealTimeCostEstimator(location=location)
                print(">> Using fallback scraper for real-time prices")
            else:
                print(">> Warning: Real-time prices requested but no scraper available")
                print(">> Install dependencies or check brightdata_scraper.py")
                self.use_realtime_prices = False
        
        # Initialize meal combination engine
        if use_meal_combinations:
            self.combination_engine = MealCombinationEngine()
            print(">> Meal Combination Mode: Enabled (will create complete meals)")
        
        self._clean_data()
        self.nutrition_estimator = NutritionEstimator()
        self.cost_estimator = CostEstimator()
        self.meal_scorer = MealScorer()
        
    def _clean_data(self):
        """Clean and prepare dataset"""
        # Replace -1 values with reasonable defaults
        self.df['prep_time'] = self.df['prep_time'].replace(-1, 15)
        self.df['cook_time'] = self.df['cook_time'].replace(-1, 30)
        
        # Handle missing values
        self.df['prep_time'] = self.df['prep_time'].fillna(15)
        self.df['cook_time'] = self.df['cook_time'].fillna(30)
        self.df['region'] = self.df['region'].replace('-1', 'All')
        self.df['region'] = self.df['region'].fillna('All')
        self.df['state'] = self.df['state'].replace('-1', 'All India')
        self.df['state'] = self.df['state'].fillna('All India')
        self.df['flavor_profile'] = self.df['flavor_profile'].replace('-1', 'mild')
        self.df['flavor_profile'] = self.df['flavor_profile'].fillna('mild')
        
        # Calculate total time
        self.df['total_time'] = self.df['prep_time'] + self.df['cook_time']
        
        # If healthy mode is enabled, filter for health-focused meals
        if self.use_healthy_mode:
            self._apply_healthy_filter()
    
    def _apply_healthy_filter(self):
        """
        Filter dataset for health-focused meals:
        - Keep all main courses
        - Keep healthy snacks suitable for breakfast (not sweet desserts)
        - Remove most desserts (keep only milk-based healthy ones)
        - Keep starters for variety
        """
        # Define healthy breakfast snacks (savory, not sweet)
        healthy_breakfast_snacks = [
            'Poha', 'Upma', 'Idli', 'Dosa', 'Uttapam', 'Pesarattu',
            'Dhokla', 'Thepla', 'Paratha', 'Aloo tikki', 'Vada',
            'Handvo', 'Muthiya', 'Idiappam', 'Puttu', 'Thalipeeth',
            'Sabudana Khichadi', 'Sevai', 'Paniyaram', 'Kachori',
            'Litti chokha', 'Misi roti', 'Sattu ki roti', 'Attu',
            'Puri Bhaji', 'Fara'
        ]
        
        # Define healthy desserts (milk-based, less sugar)
        healthy_desserts = [
            'Kheer', 'Payasam', 'Phirni', 'Misti doi', 
            'Basundi', 'Shrikhand', 'Rabri'
        ]
        
        # Keep: main courses, healthy breakfast snacks, starters, some desserts
        self.df['is_healthy'] = (
            (self.df['course'] == 'main course') |
            ((self.df['course'] == 'snack') & (self.df['name'].isin(healthy_breakfast_snacks))) |
            (self.df['course'] == 'starter') |
            ((self.df['course'] == 'dessert') & (self.df['name'].isin(healthy_desserts)))
        )
        
        # Filter to only healthy dishes
        original_count = len(self.df)
        self.df = self.df[self.df['is_healthy']].copy()
        filtered_count = len(self.df)
        
        print(f">> Healthy mode enabled: Filtered {original_count} -> {filtered_count} dishes")
        print(f"   Main courses: {len(self.df[self.df['course'] == 'main course'])}")
        print(f"   Healthy breakfast: {len(self.df[self.df['course'] == 'snack'])}")
        print(f"   Starters: {len(self.df[self.df['course'] == 'starter'])}")
        print(f"   Healthy desserts: {len(self.df[self.df['course'] == 'dessert'])}")
        
    def generate_weekly_plan(self, user_prefs: UserPreferences) -> Dict:
        """
        Generate optimized 7-day meal plan
        
        This is the main entry point for the AI system
        """
        # Step 1: Filter dataset based on constraints
        filtered_df = self._filter_dataset(user_prefs)
        
        if filtered_df.empty:
            return {"error": "No dishes match your dietary preferences"}
        
        # Step 2: Enrich with nutrition and cost data
        enriched_df = self._enrich_dataset(filtered_df)
        
        # Step 3: Generate meal plan
        weekly_plan = self._build_weekly_plan(enriched_df, user_prefs)
        
        # Step 4: Validate and rebalance
        weekly_plan = self._validate_and_rebalance(weekly_plan, user_prefs)
        
        # Step 5: Generate additional outputs
        shopping_list = self._generate_shopping_list(weekly_plan)
        batch_suggestions = self._generate_batch_cooking_suggestions(weekly_plan)
        nutrition_summary = self._generate_nutrition_summary(weekly_plan, user_prefs)
        
        # Step 6: Format output
        return self._format_output(
            weekly_plan, 
            shopping_list, 
            batch_suggestions, 
            nutrition_summary,
            user_prefs
        )
    
    def _filter_dataset(self, user_prefs: UserPreferences) -> pd.DataFrame:
        """Filter dataset by diet, region, and time constraints"""
        filtered = self.df.copy()
        
        # Diet filter (STRICT)
        diet_map = {
            "Vegetarian": "vegetarian",
            "Non-Vegetarian": ["vegetarian", "non vegetarian"],
            "Vegan": "vegetarian",  # Further filtered later
            "Jain": "vegetarian",
            "Gluten-Free": "vegetarian",  # Need ingredient check
            "Keto": ["vegetarian", "non vegetarian"],
            "High-Protein": ["vegetarian", "non vegetarian"],
            "Low-Carb": ["vegetarian", "non vegetarian"]
        }
        
        diet_filter = diet_map.get(user_prefs.diet, "vegetarian")
        if isinstance(diet_filter, list):
            filtered = filtered[filtered['diet'].isin(diet_filter)]
        else:
            filtered = filtered[filtered['diet'] == diet_filter]
        
        # Vegan filter (exclude dairy/eggs)
        if user_prefs.diet == "Vegan":
            vegan_excludes = ["milk", "curd", "yogurt", "ghee", "butter", "paneer", "egg", "cream", "cheese"]
            for exclude in vegan_excludes:
                filtered = filtered[~filtered['ingredients'].str.lower().str.contains(exclude, na=False)]
        
        # Jain filter (exclude onion, garlic, root vegetables)
        if user_prefs.diet == "Jain":
            jain_excludes = ["onion", "garlic", "potato", "ginger"]
            for exclude in jain_excludes:
                filtered = filtered[~filtered['ingredients'].str.lower().str.contains(exclude, na=False)]
        
        # Gluten-Free filter
        if user_prefs.diet == "Gluten-Free":
            gluten_items = ["wheat", "maida", "atta", "flour", "naan", "roti"]
            for item in gluten_items:
                filtered = filtered[~filtered['ingredients'].str.lower().str.contains(item, na=False)]
        
        # Region preference (soft filter)
        if user_prefs.region and user_prefs.region != "All":
            regional = filtered[filtered['region'] == user_prefs.region]
            if len(regional) >= 15:  # If enough regional dishes
                filtered = regional
        
        # Time constraint
        if user_prefs.cooking_time_limit > 0:
            filtered = filtered[filtered['total_time'] <= user_prefs.cooking_time_limit * 1.5]  # Allow 50% buffer
        
        return filtered
    
    def _enrich_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add nutrition and cost estimates to each dish"""
        enriched = df.copy()
        
        nutrition_data = []
        cost_data = []
        
        # If real-time prices enabled, print notification
        if self.use_realtime_prices:
            print(f"\n>> Fetching real-time prices for {len(enriched)} dishes...")
            print(f">> This may take a moment...\n")
        
        for idx, row in enriched.iterrows():
            nutrition = self.nutrition_estimator.estimate_nutrition(
                row['ingredients'], 
                row['course']
            )
            
            # Use real-time price estimator if enabled
            if self.use_realtime_prices:
                cost = self.realtime_cost_estimator.estimate_dish_cost(
                    row['ingredients'],
                    servings=2
                )
                if idx < 3:  # Show first 3 for demo
                    print(f"   {row['name']}: Rs {cost:.2f} (real-time)")
            else:
                cost = self.cost_estimator.estimate_cost(
                    row['ingredients'],
                    row['cook_time'],
                    row['prep_time']
                )
            
            nutrition_data.append(nutrition)
            cost_data.append(cost)
        
        if self.use_realtime_prices:
            print(f"\n>> Real-time price fetch complete!\n")
        
        enriched['calories'] = [n['calories'] for n in nutrition_data]
        enriched['protein'] = [n['protein'] for n in nutrition_data]
        enriched['carbs'] = [n['carbs'] for n in nutrition_data]
        enriched['fat'] = [n['fat'] for n in nutrition_data]
        enriched['cost'] = cost_data
        
        return enriched
    
    def _build_weekly_plan(self, df: pd.DataFrame, user_prefs: UserPreferences) -> List[Dict]:
        """Build 7-day meal plan using scoring algorithm"""
        weekly_plan = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Separate dishes by meal type - HEALTH FOCUSED
        # Breakfast: Use ONLY healthy snacks (like Poha, Upma, Idli, Dosa)
        breakfast_df = df[df['course'] == 'snack'].copy()
        
        # If not enough breakfast options, use light main courses
        if len(breakfast_df) < 7:
            light_main_courses = df[
                (df['course'] == 'main course') & 
                (df['total_time'] <= 30)  # Quick to prepare
            ].copy()
            if len(light_main_courses) > 0:
                breakfast_df = pd.concat([breakfast_df, light_main_courses])
        
        # Lunch & Dinner: Use main courses ONLY
        main_course_df = df[df['course'] == 'main course'].copy()
        
        # Fallback if no main courses (shouldn't happen in healthy mode)
        if len(main_course_df) < 14:  # Need 14 for lunch+dinner
            print("⚠️  Warning: Limited main course options. Including starters.")
            starters = df[df['course'] == 'starter'].copy()
            main_course_df = pd.concat([main_course_df, starters])
        
        used_dishes = set()
        recently_used = []  # Track last 3 meals to avoid immediate repetition
        ingredient_pool = []
        
        for day in days:
            daily_meals = {}
            
            # Breakfast - Use ONLY snacks (healthy breakfast items)
            breakfast = self._select_best_meal(
                breakfast_df, user_prefs, 'breakfast', 
                ingredient_pool, used_dishes, recently_used
            )
            daily_meals['breakfast'] = breakfast
            # Track the main dish name, not the combination
            main_dish = breakfast.get('main_dish_name', breakfast['dish'].split('+')[0].strip())
            used_dishes.add(main_dish)
            recently_used.append(main_dish)
            if len(recently_used) > 6:  # Keep last 6 dishes (2 days worth)
                recently_used.pop(0)
            ingredient_pool.extend(breakfast.get('ingredients', '').lower().split(','))
            
            # Lunch - Use ONLY main courses
            lunch = self._select_best_meal(
                main_course_df, user_prefs, 'lunch',
                ingredient_pool, used_dishes, recently_used
            )
            daily_meals['lunch'] = lunch
            # Track the main dish name, not the combination
            main_dish = lunch.get('main_dish_name', lunch['dish'].split('+')[0].strip())
            used_dishes.add(main_dish)
            recently_used.append(main_dish)
            if len(recently_used) > 6:
                recently_used.pop(0)
            ingredient_pool.extend(lunch.get('ingredients', '').lower().split(','))
            
            # Dinner - Use ONLY main courses  
            dinner = self._select_best_meal(
                main_course_df, user_prefs, 'dinner',
                ingredient_pool, used_dishes, recently_used
            )
            daily_meals['dinner'] = dinner
            # Track the main dish name, not the combination
            main_dish = dinner.get('main_dish_name', dinner['dish'].split('+')[0].strip())
            used_dishes.add(main_dish)
            recently_used.append(main_dish)
            if len(recently_used) > 6:
                recently_used.pop(0)
            ingredient_pool.extend(dinner.get('ingredients', '').lower().split(','))
            
            weekly_plan.append({
                "day": day,
                "meals": daily_meals
            })
        
        return weekly_plan
    
    def _select_best_meal(
        self, 
        df: pd.DataFrame, 
        user_prefs: UserPreferences,
        meal_type: str,
        ingredient_pool: List[str],
        used_dishes: set,
        recently_used: List[str] = None
    ) -> Dict:
        """
        Select the best meal using scoring algorithm with variety enforcement.
        
        Args:
            df: Available dishes dataframe
            user_prefs: User preferences
            meal_type: breakfast, lunch, or dinner
            ingredient_pool: Previously used ingredients for reuse bonus
            used_dishes: Set of dishes already used this week (no repeats)
            recently_used: List of last 6 dishes to penalize immediate repetition
        """
        if recently_used is None:
            recently_used = []
        
        # Filter out already used dishes
        available = df[~df['name'].isin(used_dishes)].copy()
        
        if available.empty:
            # If all dishes used, allow reuse but still avoid recent ones
            available = df.copy()
            print(f"   Note: Reusing dishes for {meal_type} due to limited options")
        
        # Score all available meals
        scores = []
        for _, dish in available.iterrows():
            nutrition = {
                'calories': dish['calories'],
                'protein': dish['protein'],
                'carbs': dish['carbs'],
                'fat': dish['fat']
            }
            score = self.meal_scorer.score_meal(
                dish, user_prefs, nutrition, dish['cost'], ingredient_pool
            )
            
            # Penalty for recently used dishes (to ensure variety)
            if dish['name'] in recently_used:
                # Higher penalty for more recent usage
                recency_index = recently_used.index(dish['name'])
                penalty = (len(recently_used) - recency_index) * 0.15  # 0.15 penalty per recent position
                score = score * (1 - penalty)
            
            scores.append(score)
        
        available['score'] = scores
        
        # Select top-scoring meal
        best_meal = available.nlargest(1, 'score').iloc[0]
        
        # Generate selection reason
        reason = self._generate_selection_reason(best_meal, user_prefs)
        
        # Create base meal dict
        meal_dict = {
            "dish": best_meal['name'],
            "main_dish_name": best_meal['name'],  # Store original name for tracking
            "time": f"{int(best_meal['total_time'])} min",
            "calories": f"{int(best_meal['calories'])} kcal",
            "protein": f"{best_meal['protein']}g",
            "carbs": f"{best_meal['carbs']}g",
            "fat": f"{best_meal['fat']}g",
            "cost": f"₹{best_meal['cost']}",
            "cost_value": best_meal['cost'],
            "calories_value": best_meal['calories'],
            "reason": reason,
            "ingredients": best_meal['ingredients']
        }
        
        # If meal combinations enabled, create complete meal
        if self.use_meal_combinations:
            budget_remaining = user_prefs.cost_per_meal_limit - best_meal['cost']
            combination = self.combination_engine.create_meal_combination(
                meal_dict, 
                meal_type, 
                budget_remaining,
                include_sides=True
            )
            
            # Update meal dict with combination info
            if combination["accompaniments"]:
                # Format as "Main Dish + Accompaniment 1 + Accompaniment 2"
                meal_dict["dish"] = self.combination_engine.format_combination_for_display(combination)
                meal_dict["accompaniments"] = combination["accompaniments"]
                
                # Update nutrition and cost with combination totals
                nutrition = self.combination_engine.get_combination_nutrition(combination)
                meal_dict["calories"] = f"{int(nutrition['calories'])} kcal"
                meal_dict["calories_value"] = nutrition['calories']
                meal_dict["protein"] = f"{nutrition['protein']}g"
                meal_dict["carbs"] = f"{nutrition['carbs']}g"
                meal_dict["fat"] = f"{nutrition['fat']}g"
                meal_dict["cost"] = f"₹{nutrition['cost']}"
                meal_dict["cost_value"] = nutrition['cost']
                meal_dict["time"] = f"{nutrition['time']} min"
        
        return meal_dict
    
    def _generate_selection_reason(self, dish: pd.Series, user_prefs: UserPreferences) -> str:
        """Generate human-readable reason for meal selection"""
        reasons = []
        
        if dish['cost'] < user_prefs.cost_per_meal_limit * 0.7:
            reasons.append("budget-friendly")
        
        if dish['total_time'] <= user_prefs.cooking_time_limit * 0.7:
            reasons.append("quick to prepare")
        
        if dish['protein'] >= 15:
            reasons.append("high protein")
        
        if dish.get('region') == user_prefs.region:
            reasons.append(f"regional {user_prefs.region} dish")
        
        if pd.notna(dish['flavor_profile']) and dish['flavor_profile'] in user_prefs.preferred_flavors:
            reasons.append(f"{dish['flavor_profile']} flavor match")
        
        if not reasons:
            reasons.append("balanced nutrition")
        
        return ", ".join(reasons[:3])
    
    def _validate_and_rebalance(self, weekly_plan: List[Dict], user_prefs: UserPreferences) -> List[Dict]:
        """Validate constraints and rebalance if needed"""
        total_cost = sum(
            sum(meal['cost_value'] for meal in day['meals'].values())
            for day in weekly_plan
        )
        
        # If over budget, replace most expensive meals with cheaper alternatives
        if total_cost > user_prefs.weekly_budget:
            # This is a simplified rebalancing - in production, implement more sophisticated logic
            pass
        
        return weekly_plan
    
    def _generate_shopping_list(self, weekly_plan: List[Dict]) -> Dict[str, int]:
        """Generate consolidated shopping list"""
        ingredients_counter = {}
        
        for day in weekly_plan:
            for meal in day['meals'].values():
                ingredients = meal.get('ingredients', '').split(',')
                for ingredient in ingredients:
                    ingredient = ingredient.strip().lower()
                    if ingredient:
                        ingredients_counter[ingredient] = ingredients_counter.get(ingredient, 0) + 1
        
        # Sort by frequency (most used first)
        sorted_ingredients = dict(sorted(
            ingredients_counter.items(), 
            key=lambda x: x[1], 
            reverse=True
        ))
        
        return sorted_ingredients
    
    def _generate_batch_cooking_suggestions(self, weekly_plan: List[Dict]) -> List[str]:
        """Suggest batch cooking opportunities"""
        suggestions = []
        ingredient_days = {}
        
        # Track which days use which ingredients
        for day_idx, day in enumerate(weekly_plan):
            for meal in day['meals'].values():
                ingredients = meal.get('ingredients', '').lower().split(',')
                for ingredient in ingredients:
                    ingredient = ingredient.strip()
                    if ingredient not in ingredient_days:
                        ingredient_days[ingredient] = []
                    ingredient_days[ingredient].append(day_idx)
        
        # Find ingredients used multiple times in adjacent days
        for ingredient, days in ingredient_days.items():
            if len(days) >= 3:
                suggestions.append(
                    f"Batch prep {ingredient} - used on days {', '.join([weekly_plan[d]['day'] for d in days[:3]])}"
                )
        
        return suggestions[:5]  # Top 5 suggestions
    
    def _generate_nutrition_summary(self, weekly_plan: List[Dict], user_prefs: UserPreferences) -> Dict:
        """Generate weekly nutrition summary"""
        total_calories = 0
        total_protein = 0
        total_cost = 0
        
        for day in weekly_plan:
            for meal in day['meals'].values():
                total_calories += meal['calories_value']
                total_protein += float(meal['protein'].replace('g', ''))
                total_cost += meal['cost_value']
        
        daily_avg_calories = total_calories / 7
        target_daily = user_prefs.daily_calorie_target
        calorie_accuracy = 100 - abs((daily_avg_calories - target_daily) / target_daily * 100)
        
        return {
            "total_weekly_calories": round(total_calories, 0),
            "daily_avg_calories": round(daily_avg_calories, 0),
            "total_weekly_protein": round(total_protein, 1),
            "daily_avg_protein": round(total_protein / 7, 1),
            "calorie_target_accuracy": f"{round(calorie_accuracy, 1)}%",
            "total_cost": round(total_cost, 2)
        }
    
    def _format_output(
        self, 
        weekly_plan: List[Dict],
        shopping_list: Dict,
        batch_suggestions: List[str],
        nutrition_summary: Dict,
        user_prefs: UserPreferences
    ) -> Dict:
        """Format final JSON output"""
        total_cost = sum(
            sum(meal['cost_value'] for meal in day['meals'].values())
            for day in weekly_plan
        )
        
        avg_cost_per_meal = total_cost / 21  # 7 days × 3 meals
        
        # Determine budget status
        budget_ratio = total_cost / user_prefs.weekly_budget
        if budget_ratio <= 0.9:
            budget_status = "under"
        elif budget_ratio <= 1.0:
            budget_status = "optimal"
        elif budget_ratio <= 1.15:
            budget_status = "slightly over"
        else:
            budget_status = "exceeds"
        
        # Calculate ingredient overlap score
        unique_ingredients = len(shopping_list)
        total_ingredient_uses = sum(shopping_list.values())
        overlap_score = round((1 - unique_ingredients / total_ingredient_uses) * 100, 1)
        
        # Format weekly plan (remove internal fields)
        formatted_plan = []
        for day in weekly_plan:
            formatted_day = {
                "day": day['day'],
                "meals": {}
            }
            for meal_type, meal in day['meals'].items():
                formatted_day['meals'][meal_type] = {
                    "dish": meal['dish'],
                    "time": meal['time'],
                    "calories": meal['calories'],
                    "protein": meal['protein'],
                    "carbs": meal['carbs'],
                    "fat": meal['fat'],
                    "cost": meal['cost'],
                    "reason": meal['reason']
                }
            formatted_plan.append(formatted_day)
        
        return {
            "weekly_plan": formatted_plan,
            "summary": {
                "total_cost": f"₹{round(total_cost, 2)}",
                "avg_cost_per_meal": f"₹{round(avg_cost_per_meal, 2)}",
                "weekly_budget": f"₹{user_prefs.weekly_budget}",
                "budget_status": budget_status,
                "calorie_balance_accuracy": nutrition_summary['calorie_target_accuracy'],
                "daily_avg_calories": nutrition_summary['daily_avg_calories'],
                "daily_avg_protein": f"{nutrition_summary['daily_avg_protein']}g",
                "ingredient_overlap_score": f"{overlap_score}%"
            },
            "shopping_list": dict(list(shopping_list.items())[:20]),  # Top 20 ingredients
            "batch_cooking_suggestions": batch_suggestions,
            "nutrition_summary": nutrition_summary
        }


def main():
    """Example usage of MealCraft-AI"""
    
    # Initialize the AI system
    ai = MealCraftAI("indian_food.csv")
    
    # Define user preferences
    user_input = {
        "diet": "Vegetarian",
        "preferred_cuisines": ["North Indian", "West Indian"],
        "daily_calorie_target": 2000,
        "weekly_budget": 1200,
        "preferred_flavors": ["spicy", "mild"],
        "cooking_time_limit": 45,
        "region": "North",
        "goals": ["weight loss", "energy"],
        "cost_per_meal_limit": 75
    }
    
    user_prefs = UserPreferences(**user_input)
    
    # Generate meal plan
    print("🍽️  Generating your personalized weekly meal plan...")
    print("=" * 60)
    
    meal_plan = ai.generate_weekly_plan(user_prefs)
    
    # Output as formatted JSON
    print(json.dumps(meal_plan, indent=2, ensure_ascii=False))
    
    # Save to file
    with open('meal_plan_output.json', 'w', encoding='utf-8') as f:
        json.dump(meal_plan, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Meal plan generated successfully!")
    print("📄 Saved to: meal_plan_output.json")


if __name__ == "__main__":
    main()
