"""
MealCraft Backend API Server
FastAPI server integrating ML model with frontend
"""

# CRITICAL: Set event loop policy BEFORE any asyncio imports
# This fixes Playwright subprocess issues on Windows
import sys
import asyncio
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uvicorn
import json
import numpy as np

# Import ML system
from mealcraft_ai import MealCraftAI, UserPreferences

# Import database
from database import db

# Import recipe data
from recipe_instructions import get_recipe_instructions
from recipe_images import get_recipe_image


def convert_numpy_types(obj):
    """Convert NumPy types to Python native types recursively"""
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

# Import grocery scraper
try:
    from local_grocery_scraper import ChennaiCostEstimator
    SCRAPER_AVAILABLE = True
except:
    SCRAPER_AVAILABLE = False
    print("⚠️  Grocery scraper not available")

# Initialize FastAPI app
app = FastAPI(
    title="MealCraft API",
    description="AI-Powered Meal Planning Backend",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML system
try:
    meal_planner = MealCraftAI(
        dataset_path="indian_food_cleaned.csv",
        location="Chennai",
        use_realtime_prices=False  # Use database pricing
    )
    print("[OK] ML system initialized")
except Exception as e:
    print(f"[ERROR] Error initializing ML system: {e}")
    meal_planner = None

# Initialize grocery scraper
if SCRAPER_AVAILABLE:
    grocery_scraper = ChennaiCostEstimator()
    print("[OK] Grocery scraper initialized")


# ===== PYDANTIC MODELS =====

class UserCreate(BaseModel):
    email: str
    user_name: str = "User"
    family_size: int = 1
    city: str = "Chennai"


class UserPreferencesInput(BaseModel):
    email: str
    diet: str = "Vegetarian"
    preferred_cuisines: List[str] = ["North Indian"]
    dietary_restrictions: List[str] = []
    cooking_time_limit: int = 45
    cooking_complexity: str = "intermediate"
    daily_calorie_target: int = 2000
    weekly_budget: float = 1200
    health_goals: List[str] = []
    preferred_flavors: List[str] = ["spicy", "mild"]
    region: str = "All"
    cost_per_meal_limit: float = 75


class MealPlanRequest(BaseModel):
    email: str
    preferences: Optional[UserPreferencesInput] = None


class GroceryPriceUpdate(BaseModel):
    store_name: str
    items: List[Dict[str, Any]]


class AutomateOrderRequest(BaseModel):
    store_name: str
    ingredients: List[str]
    meal_name: str = ""


class AuthSignupRequest(BaseModel):
    email: str
    password: str
    user_name: str
    family_size: int = 4
    city: str = "Chennai"


class AuthLoginRequest(BaseModel):
    email: str
    password: str


# ===== HEALTH CHECK =====

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "MealCraft API",
        "status": "online",
        "version": "1.0.0",
        "ml_status": "ready" if meal_planner else "unavailable",
        "scraper_status": "ready" if SCRAPER_AVAILABLE else "unavailable"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "ml_model": "ready" if meal_planner else "unavailable",
            "grocery_scraper": "ready" if SCRAPER_AVAILABLE else "unavailable"
        }
    }


# ===== AUTHENTICATION =====

@app.post("/api/auth/signup")
async def signup(request: AuthSignupRequest):
    """Sign up a new user"""
    try:
        # Check if user already exists
        existing_user = db.get_user_by_email(request.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        user_id = db.create_user(
            email=request.email,
            user_name=request.user_name,
            family_size=request.family_size,
            city=request.city
        )
        
        if not user_id:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        # Store password (in production, use proper password hashing!)
        db.save_user_password(user_id, request.password)
        
        # Get user data
        user = db.get_user_by_email(request.email)
        
        return {
            "success": True,
            "message": "Account created successfully",
            "user": user,
            "token": f"token_{user_id}_{request.email}"  # Simple token for demo
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/login")
async def login(request: AuthLoginRequest):
    """Login existing user"""
    try:
        # Get user
        user = db.get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not db.verify_user_password(user['id'], request.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        return {
            "success": True,
            "message": "Login successful",
            "user": user,
            "token": f"token_{user['id']}_{request.email}"  # Simple token for demo
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/user/dashboard/{email}")
async def get_user_dashboard(email: str):
    """Get user dashboard data"""
    try:
        user = db.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user stats
        meal_plans = db.get_user_meal_plans(user['id']) or []
        shopping_lists = db.get_user_shopping_lists(user['id']) or []
        preferences = db.get_user_preferences(user['id'])
        
        total_spent = sum([float(mp.get('total_cost', 0)) for mp in meal_plans])
        
        # Get recent items (last 5)
        recent_meal_plans = meal_plans[-5:] if meal_plans else []
        recent_shopping_lists = shopping_lists[-5:] if shopping_lists else []
        
        return {
            "total_meal_plans": len(meal_plans),
            "total_shopping_lists": len(shopping_lists),
            "total_spent": total_spent,
            "preferences_set": preferences is not None,
            "recent_meal_plans": recent_meal_plans,
            "recent_shopping_lists": recent_shopping_lists
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== USER MANAGEMENT =====

@app.post("/api/users/create")
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        user_id = db.create_user(
            email=user.email,
            user_name=user.user_name,
            family_size=user.family_size,
            city=user.city
        )
        if user_id:
            return {
                "success": True,
                "user_id": user_id,
                "message": "User created successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/users/{email}")
async def get_user(email: str):
    """Get user by email"""
    user = db.get_user_by_email(email)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


# ===== PREFERENCES =====

@app.post("/api/preferences/save")
async def save_preferences(prefs: UserPreferencesInput):
    """Save user preferences"""
    try:
        # Get or create user
        user = db.get_user_by_email(prefs.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found. Create user first.")
        
        # Save preferences
        preferences_dict = prefs.dict()
        preferences_dict.pop('email')
        
        success = db.save_user_preferences(user['id'], preferences_dict)
        
        if success:
            return {
                "success": True,
                "message": "Preferences saved successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save preferences")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/preferences/{email}")
async def get_preferences(email: str):
    """Get user preferences"""
    user = db.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    prefs = db.get_user_preferences(user['id'])
    if prefs:
        return prefs
    else:
        raise HTTPException(status_code=404, detail="Preferences not found")


# ===== MEAL PLAN GENERATION =====

@app.post("/api/meal-plan/generate")
async def generate_meal_plan(request: MealPlanRequest):
    """Generate AI-powered meal plan"""
    try:
        if not meal_planner:
            raise HTTPException(status_code=503, detail="ML system unavailable")
        
        # Get user
        user = db.get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get preferences (from request or database)
        if request.preferences:
            prefs_data = request.preferences.dict()
            prefs_data.pop('email')
        else:
            prefs_data = db.get_user_preferences(user['id'])
            if not prefs_data:
                raise HTTPException(status_code=404, detail="User preferences not found")
        
        # Convert to UserPreferences object for ML system
        user_prefs = UserPreferences(
            diet=prefs_data.get('diet', 'Vegetarian'),
            preferred_cuisines=prefs_data.get('preferred_cuisines', []),
            daily_calorie_target=prefs_data.get('daily_calorie_target', 2000),
            weekly_budget=prefs_data.get('weekly_budget', 1200),
            preferred_flavors=prefs_data.get('preferred_flavors', ['spicy']),
            cooking_time_limit=prefs_data.get('cooking_time_limit', 45),
            region=prefs_data.get('region', 'All'),
            goals=prefs_data.get('health_goals', []),
            cost_per_meal_limit=prefs_data.get('cost_per_meal_limit', 75)
        )
        
        # Generate meal plan using ML
        meal_plan = meal_planner.generate_weekly_plan(user_prefs)
        
        if 'error' in meal_plan:
            raise HTTPException(status_code=400, detail=meal_plan['error'])
        
        # Convert all NumPy types to Python types
        meal_plan = convert_numpy_types(meal_plan)
        
        # Save to database
        today = datetime.now().date()
        end_date = today + timedelta(days=6)
        
        meal_plan_id = db.save_meal_plan(
            user_id=user['id'],
            plan_data=meal_plan,
            start_date=today.isoformat(),
            end_date=end_date.isoformat()
        )
        
        # Save shopping list if available
        if 'shopping_list' in meal_plan and meal_plan_id:
            shopping_items = meal_plan['shopping_list']
            total_cost = float(meal_plan.get('summary', {}).get('total_cost', '0').replace('₹', '').replace(',', ''))
            
            db.save_shopping_list(
                meal_plan_id=meal_plan_id,
                user_id=user['id'],
                items=shopping_items,
                total_cost=total_cost
            )
        
        return {
            "success": True,
            "meal_plan_id": meal_plan_id,
            "meal_plan": meal_plan,
            "message": "Meal plan generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating meal plan: {str(e)}")


@app.get("/api/meal-plan/{meal_plan_id}")
async def get_meal_plan(meal_plan_id: int):
    """Get a specific meal plan"""
    meal_plan = db.get_meal_plan(meal_plan_id)
    if meal_plan:
        return meal_plan
    else:
        raise HTTPException(status_code=404, detail="Meal plan not found")


@app.get("/api/meal-plan/user/{email}")
async def get_user_meal_plans(email: str, limit: int = 10):
    """Get user's meal plans"""
    user = db.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    meal_plans = db.get_user_meal_plans(user['id'], limit)
    return {
        "user_email": email,
        "meal_plans": meal_plans,
        "count": len(meal_plans)
    }


# ===== GROCERY PRICING & WEB SCRAPING =====

@app.get("/api/grocery/prices")
async def get_grocery_prices(store: Optional[str] = None):
    """Get grocery prices from database"""
    try:
        prices = db.get_grocery_prices(store_name=store)
        return {
            "success": True,
            "store": store or "all",
            "prices": prices,
            "count": len(prices)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/grocery/scrape")
async def scrape_grocery_prices(stores: List[str] = Body(["Grace Daily", "KPN Fresh"])):
    """Trigger web scraping for grocery prices"""
    if not SCRAPER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Grocery scraper unavailable")
    
    try:
        all_prices = []
        
        for store in stores:
            if store.lower() == "grace daily":
                prices = grocery_scraper.get_grace_daily_prices()
                all_prices.extend(prices)
            elif store.lower() == "kpn fresh":
                prices = grocery_scraper.get_kpn_fresh_prices()
                all_prices.extend(prices)
        
        # Update database
        count = db.update_grocery_prices(all_prices)
        
        return {
            "success": True,
            "stores_scraped": stores,
            "prices_updated": count,
            "message": f"Successfully scraped {count} prices"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")


@app.get("/api/grocery/compare")
async def compare_prices(item_name: str):
    """Compare prices across stores for a specific item"""
    try:
        conn = db.get_connection()
        with conn.cursor(cursor_factory=db.RealDictCursor) as cur:
            cur.execute("""
                SELECT store_name, price, unit, in_stock, scraped_at
                FROM grocery_prices
                WHERE LOWER(item_name) = LOWER(%s)
                ORDER BY price ASC
            """, (item_name,))
            results = [dict(row) for row in cur.fetchall()]
        
        db.return_connection(conn)
        
        if results:
            return {
                "item": item_name,
                "stores": results,
                "best_price": results[0] if results else None
            }
        else:
            raise HTTPException(status_code=404, detail="Item not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== AVAILABLE OPTIONS =====

@app.get("/api/options")
async def get_available_options():
    """Get available dietary options, regions, cuisines, etc."""
    return {
        "diets": [
            "Vegetarian", "Non-Vegetarian", "Vegan", "Jain",
            "Gluten-Free", "Keto", "High-Protein", "Low-Carb"
        ],
        "regions": ["North", "South", "East", "West", "North East", "Central", "All"],
        "flavors": ["spicy", "mild", "sweet", "sour", "bitter", "tangy"],
        "goals": ["weight loss", "muscle gain", "energy", "immunity", "maintenance", "healthy eating"],
        "cuisines": [
            "North Indian", "South Indian", "East Indian", "West Indian",
            "Gujarati", "Punjabi", "Bengali", "Tamil", "Kerala", "Maharashtra",
            "Rajasthani", "Hyderabadi"
        ],
        "cooking_complexity": ["beginner", "intermediate", "advanced"],
        "stores": ["Grace Daily", "KPN Fresh", "BigBasket", "Instamart", "Zepto"]
    }


# ===== RECIPE DISCOVERY ENDPOINTS =====

@app.get("/api/recipes/search")
async def search_recipes(
    query: Optional[str] = None,
    diet: Optional[str] = None,
    course: Optional[str] = None,
    region: Optional[str] = None,
    flavor: Optional[str] = None,
    max_time: Optional[int] = None,
    limit: int = 20
):
    """
    Search recipes from the Indian food database
    
    Query parameters:
    - query: Search by dish name
    - diet: Filter by diet type (vegetarian, non-vegetarian, vegan)
    - course: Filter by course (breakfast, lunch, dinner, snack, dessert)
    - region: Filter by region (North, South, East, West)
    - flavor: Filter by flavor profile (spicy, sweet, tangy, mild)
    - max_time: Maximum cooking time in minutes
    - limit: Maximum number of results (default 20)
    """
    try:
        import pandas as pd
        
        # Load the dataset
        df = pd.read_csv("indian_food_cleaned.csv")
        
        # Apply filters
        if query:
            df = df[df['name'].str.contains(query, case=False, na=False)]
        
        if diet:
            df = df[df['diet'].str.lower() == diet.lower()]
        
        if course:
            df = df[df['course'].str.lower() == course.lower()]
        
        if region and region.lower() != 'all':
            df = df[df['region'].str.contains(region, case=False, na=False)]
        
        if flavor:
            df = df[df['flavor_profile'].str.lower() == flavor.lower()]
        
        if max_time:
            df = df[df['total_time'] <= max_time]
        
        # Limit results
        df = df.head(limit)
        
        # Convert to dictionary and add images
        recipes = df.to_dict('records')
        
        # Add image URLs to each recipe
        for recipe in recipes:
            recipe['image_url'] = get_recipe_image(recipe['name'])
        
        return {
            "success": True,
            "count": len(recipes),
            "recipes": recipes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching recipes: {str(e)}")


@app.get("/api/recipes/{recipe_name}")
async def get_recipe_details(recipe_name: str):
    """
    Get detailed information about a specific recipe including preparation instructions
    """
    try:
        import pandas as pd
        
        # Load the dataset
        df = pd.read_csv("indian_food_cleaned.csv")
        
        # Find the recipe (case-insensitive)
        recipe = df[df['name'].str.lower() == recipe_name.lower()]
        
        if recipe.empty:
            raise HTTPException(status_code=404, detail=f"Recipe '{recipe_name}' not found")
        
        # Get the first match and convert to dict
        recipe_data = recipe.iloc[0].to_dict()
        
        # Convert numpy types to Python types
        for key, value in recipe_data.items():
            if hasattr(value, 'item'):  # NumPy types have .item() method
                recipe_data[key] = value.item()
        
        # Add image URL
        recipe_data['image_url'] = get_recipe_image(recipe_data['name'])
        
        # Get detailed instructions from database
        detailed_instructions = get_recipe_instructions(recipe_data['name'])
        
        if detailed_instructions:
            # Use detailed instructions if available
            recipe_data['instructions'] = detailed_instructions['instructions']
            recipe_data['tips'] = detailed_instructions.get('tips', '')
            recipe_data['serving'] = detailed_instructions.get('serving', '')
        else:
            # Fallback to generated instructions
            recipe_data['instructions'] = generate_cooking_instructions(recipe_data)
            recipe_data['tips'] = f"Traditional {recipe_data.get('region', 'Indian')} recipe. Adjust spices according to taste."
            recipe_data['serving'] = f"Serves 4 people"
        
        # Add nutritional info from ML model if available
        if meal_planner and hasattr(meal_planner, 'nutrition_estimator'):
            try:
                recipe_data['nutrition'] = meal_planner.nutrition_estimator.estimate_dish_nutrition(
                    recipe_data['name'],
                    recipe_data.get('ingredients', '')
                )
            except:
                recipe_data['nutrition'] = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        
        # Add cost estimation if available
        if meal_planner and hasattr(meal_planner, 'cost_estimator'):
            try:
                recipe_data['estimated_cost'] = meal_planner.cost_estimator.estimate_dish_cost(
                    recipe_data['name'],
                    recipe_data.get('ingredients', '')
                )
            except:
                recipe_data['estimated_cost'] = "₹50"
        
        return {
            "success": True,
            "recipe": recipe_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recipe details: {str(e)}")



def generate_cooking_instructions(recipe_data: dict) -> List[str]:
    """
    Generate cooking instructions based on dish type and ingredients
    This is a simplified version - can be enhanced with detailed recipes
    """
    name = recipe_data['name']
    ingredients = recipe_data.get('ingredients', '')
    course = recipe_data.get('course', 'main')
    prep_time = recipe_data.get('prep_time', 15)
    cook_time = recipe_data.get('cook_time', 30)
    
    # Generic instructions template
    instructions = [
        f"Gather all ingredients: {ingredients}",
        "Wash and clean all vegetables/ingredients thoroughly",
    ]
    
    # Add course-specific instructions
    if course.lower() in ['breakfast', 'snack']:
        instructions.extend([
            f"Preparation time: {prep_time} minutes",
            "Mix the main ingredients in a bowl",
            "Heat a pan on medium flame",
            f"Cook for approximately {cook_time} minutes until golden brown",
            "Serve hot with accompaniments"
        ])
    elif course.lower() == 'dessert':
        instructions.extend([
            f"Preparation time: {prep_time} minutes",
            "Mix dry ingredients separately",
            "Prepare sugar syrup or ghee as needed",
            "Combine ingredients and shape as required",
            f"Cook/set for {cook_time} minutes",
            "Let it cool before serving"
        ])
    elif 'rice' in name.lower() or 'biryani' in name.lower():
        instructions.extend([
            "Soak rice for 30 minutes",
            "Prepare masala with spices and aromatics",
            "Cook rice separately until 70% done",
            "Layer rice with masala",
            f"Dum cook on low heat for {cook_time} minutes",
            "Serve hot with raita or salad"
        ])
    elif 'curry' in name.lower() or 'gravy' in name.lower():
        instructions.extend([
            "Heat oil in a pan, add spices for tempering",
            "Add onions and sauté until golden",
            "Add tomatoes and cook until soft",
            "Add main ingredients and spices",
            f"Cook covered for {cook_time} minutes",
            "Garnish with coriander and serve with rice/roti"
        ])
    else:
        # Generic main course
        instructions.extend([
            f"Preparation time: {prep_time} minutes",
            "Heat oil/ghee in a cooking vessel",
            "Add spices and aromatics (onion, ginger, garlic)",
            "Add main ingredients and mix well",
            "Add water/stock as needed",
            f"Cook on medium heat for {cook_time} minutes",
            "Season with salt and garnish",
            "Serve hot with rice, roti, or bread"
        ])
    
    # Add final tips
    instructions.append(f"💡 Tip: This is a {recipe_data.get('region', 'Indian')} dish best enjoyed fresh and hot!")
    
    return instructions


@app.get("/api/recipes/random")
async def get_random_recipes(count: int = 6):
    """
    Get random recipe suggestions for discovery
    """
    try:
        import pandas as pd
        
        # Load the dataset
        df = pd.read_csv("indian_food_cleaned.csv")
        
        # Get random samples
        random_recipes = df.sample(n=min(count, len(df)))
        
        recipes = random_recipes.to_dict('records')
        
        # Add image URLs to each recipe
        for recipe in recipes:
            recipe['image_url'] = get_recipe_image(recipe['name'])
        
        return {
            "success": True,
            "count": len(recipes),
            "recipes": recipes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching random recipes: {str(e)}")


# ===== BROWSER AUTOMATION =====

@app.post("/api/automate-order")
async def automate_order(request: AutomateOrderRequest):
    """
    Automate grocery shopping using AI Agent (browser-use)
    EXACT architecture from BDAIScraperAgent video
    """
    try:
        # Import AI grocery agent
        try:
            from ai_grocery_agent import automate_grocery_shopping_ai
            print(f"[OK] AI agent module imported successfully")
        except ImportError as e:
            print(f"[ERROR] Failed to import AI agent: {e}")
            raise HTTPException(
                status_code=503,
                detail=f"AI Agent not available: {str(e)}. Please install: pip install browser-use langchain-anthropic"
            )
        except Exception as e:
            print(f"[ERROR] Error importing AI agent: {e}")
            raise HTTPException(
                status_code=503,
                detail=f"AI Agent initialization failed: {str(e)}"
            )
        
        print(f"[INFO] Starting AI automation for {request.store_name}")
        print(f"[INFO] Ingredients: {request.ingredients}")
        
        # Run AI automation
        result = await automate_grocery_shopping_ai(
            store_name=request.store_name,
            ingredients=request.ingredients
        )
        
        print(f"[OK] AI automation completed: {result}")
        
        return {
            "success": True,
            "automation_result": result,
            "message": f"AI Agent automation completed for {request.store_name}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error during automation: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error automating order: {str(e)}")


# ===== DATABASE INITIALIZATION =====

@app.on_event("startup")
async def startup_event():
    """Initialize database schema on startup"""
    try:
        db.initialize_schema()
        print("[OK] Database schema initialized")
    except Exception as e:
        print(f"[ERROR] Error initializing database: {e}")


# ===== RUN SERVER =====

if __name__ == "__main__":
    print("[INFO] Starting MealCraft Backend Server...")
    print("[INFO] Database: Neon PostgreSQL")
    print("[INFO] ML Model: MealCraft-AI")
    print("[INFO] Scraper: Chennai Local Stores")
    print("\n[INFO] Server will run on: http://localhost:8000")
    print("[INFO] API Docs: http://localhost:8000/docs")
    print("\n")
    
    uvicorn.run(
        "backend_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
