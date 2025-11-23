"""
MealCraft-AI REST API
Flask-based API for serving meal plans
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from mealcraft_ai import MealCraftAI, UserPreferences
import json

app = Flask(__name__)
CORS(app)

# Initialize AI system
ai = MealCraftAI("indian_food_healthy.csv")


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "MealCraft-AI"}), 200


@app.route('/api/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    """
    Generate personalized meal plan
    
    Expected JSON input:
    {
        "diet": "Vegetarian",
        "preferred_cuisines": ["North Indian"],
        "daily_calorie_target": 2000,
        "weekly_budget": 1200,
        "preferred_flavors": ["spicy"],
        "cooking_time_limit": 45,
        "region": "North",
        "goals": ["weight loss"],
        "cost_per_meal_limit": 75
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'diet', 'daily_calorie_target', 'weekly_budget', 
            'cooking_time_limit', 'cost_per_meal_limit'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Set defaults for optional fields
        data.setdefault('preferred_cuisines', [])
        data.setdefault('preferred_flavors', ['spicy', 'mild'])
        data.setdefault('region', 'All')
        data.setdefault('goals', [])
        
        # Create user preferences
        user_prefs = UserPreferences(**data)
        
        # Generate meal plan
        meal_plan = ai.generate_weekly_plan(user_prefs)
        
        # Check for errors
        if "error" in meal_plan:
            return jsonify(meal_plan), 400
        
        return jsonify(meal_plan), 200
        
    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500


@app.route('/api/available-options', methods=['GET'])
def get_available_options():
    """Get available diet types, regions, flavors, and goals"""
    return jsonify({
        "diets": [
            "Vegetarian", "Non-Vegetarian", "Vegan", "Jain", 
            "Gluten-Free", "Keto", "High-Protein", "Low-Carb"
        ],
        "regions": ["North", "South", "East", "West", "North East", "Central", "All"],
        "flavors": ["spicy", "mild", "sweet", "sour", "bitter"],
        "goals": ["weight loss", "muscle gain", "energy", "immunity", "maintenance"],
        "cuisines": [
            "North Indian", "South Indian", "East Indian", "West Indian",
            "Gujarati", "Punjabi", "Bengali", "Tamil", "Kerala", "Maharashtra"
        ]
    }), 200


@app.route('/api/dishes', methods=['GET'])
def get_dishes():
    """
    Get filtered list of dishes
    Query params: diet, region, course
    """
    diet = request.args.get('diet')
    region = request.args.get('region')
    course = request.args.get('course')
    
    df = ai.df.copy()
    
    if diet:
        df = df[df['diet'] == diet.lower()]
    if region and region != 'All':
        df = df[df['region'] == region]
    if course:
        df = df[df['course'] == course.lower()]
    
    # Limit to 50 results
    dishes = df.head(50)[['name', 'ingredients', 'diet', 'course', 'region']].to_dict('records')
    
    return jsonify({
        "count": len(dishes),
        "dishes": dishes
    }), 200


@app.route('/api/nutrition-estimate', methods=['POST'])
def estimate_nutrition():
    """
    Estimate nutrition for a dish
    Input: {"dish_name": "Butter Chicken"}
    """
    try:
        data = request.get_json()
        dish_name = data.get('dish_name')
        
        if not dish_name:
            return jsonify({"error": "dish_name is required"}), 400
        
        # Find dish in dataset
        dish = ai.df[ai.df['name'].str.lower() == dish_name.lower()]
        
        if dish.empty:
            return jsonify({"error": "Dish not found"}), 404
        
        dish = dish.iloc[0]
        
        nutrition = ai.nutrition_estimator.estimate_nutrition(
            dish['ingredients'],
            dish['course']
        )
        
        cost = ai.cost_estimator.estimate_cost(
            dish['ingredients'],
            dish['cook_time'],
            dish['prep_time']
        )
        
        return jsonify({
            "dish": dish['name'],
            "nutrition": nutrition,
            "cost": f"₹{cost}",
            "prep_time": f"{dish['prep_time']} min",
            "cook_time": f"{dish['cook_time']} min",
            "total_time": f"{dish['total_time']} min"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting MealCraft-AI API Server...")
    print("📍 API will be available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /api/generate-meal-plan - Generate meal plan")
    print("  GET  /api/available-options  - Get diet/region options")
    print("  GET  /api/dishes             - Search dishes")
    print("  POST /api/nutrition-estimate - Estimate nutrition")
    print("  GET  /health                 - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
