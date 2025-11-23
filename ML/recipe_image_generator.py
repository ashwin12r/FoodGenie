"""
Recipe Image Generator using Google Gemini AI
Generates realistic food images for Indian recipes
"""

import os
import requests
import base64
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

def generate_recipe_image(dish_name: str, description: str = "") -> Optional[str]:
    """
    Generate an image URL for a recipe using Gemini AI's Imagen
    Note: Gemini API doesn't directly generate images, so we'll use a placeholder service
    For actual image generation, you'd need Google's Imagen API or similar
    
    Args:
        dish_name: Name of the dish
        description: Optional description for better image generation
    
    Returns:
        Image URL or None if generation fails
    """
    
    # Since Gemini doesn't have direct image generation in the API,
    # we'll use Unsplash API as a fallback to get real food images
    # You can replace this with actual Imagen API when available
    
    try:
        # Use Unsplash API to search for food images
        search_query = f"indian food {dish_name}".replace(" ", "+")
        unsplash_url = f"https://source.unsplash.com/800x600/?{search_query}"
        
        return unsplash_url
        
    except Exception as e:
        print(f"Error generating image for {dish_name}: {e}")
        return get_fallback_image(dish_name)


def get_fallback_image(dish_name: str) -> str:
    """
    Get a fallback image from Pexels or similar service
    """
    # Use Pexels as fallback
    search_query = dish_name.replace(" ", "+")
    return f"https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800"


def get_placeholder_by_category(diet_type: str, course: str = "main") -> str:
    """
    Get category-based placeholder images
    """
    
    # Map of diet types and courses to high-quality stock images
    image_map = {
        "vegetarian": {
            "main": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800",
            "starter": "https://images.unsplash.com/photo-1567337710282-00832b415979?w=800",
            "dessert": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=800",
            "breakfast": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800"
        },
        "non vegetarian": {
            "main": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800",
            "starter": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
            "dessert": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800",
            "breakfast": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800"
        },
        "vegan": {
            "main": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800",
            "starter": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
            "dessert": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800",
            "breakfast": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=800"
        }
    }
    
    diet = diet_type.lower()
    course = course.lower()
    
    if diet in image_map and course in image_map[diet]:
        return image_map[diet][course]
    
    # Default fallback
    return "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800"


# Indian food specific images database
INDIAN_FOOD_IMAGES = {
    "biryani": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800",
    "dal": "https://images.unsplash.com/photo-1546833998-877b37c2e5c6?w=800",
    "paneer": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800",
    "samosa": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=800",
    "dosa": "https://images.unsplash.com/photo-1630383249896-424e482df921?w=800",
    "idli": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800",
    "curry": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800",
    "roti": "https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=800",
    "naan": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800",
    "tikka": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=800",
    "tandoori": "https://images.unsplash.com/photo-1610057099431-d73a1c9d2f2f?w=800",
    "kheer": "https://images.unsplash.com/photo-1626776876729-bab4eff451d5?w=800",
    "gulab jamun": "https://images.unsplash.com/photo-1626776877884-8ab6fa37ea2f?w=800",
    "pakora": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=800",
    "vada": "https://images.unsplash.com/photo-1606471191009-c3b9bedb8579?w=800",
}


def get_recipe_image_url(dish_name: str, diet_type: str = "vegetarian", course: str = "main") -> str:
    """
    Get the best possible image URL for a recipe
    
    Args:
        dish_name: Name of the dish
        diet_type: vegetarian, non vegetarian, or vegan
        course: main, starter, dessert, breakfast
    
    Returns:
        Image URL
    """
    
    # Check if we have a specific image for this dish
    dish_lower = dish_name.lower()
    
    for keyword, image_url in INDIAN_FOOD_IMAGES.items():
        if keyword in dish_lower:
            return image_url
    
    # Generate using Unsplash
    search_query = f"indian+food+{dish_name.replace(' ', '+')}"
    return f"https://source.unsplash.com/800x600/?{search_query}"
