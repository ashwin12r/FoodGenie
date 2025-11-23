"""
Direct Bright Data Integration for Real-Time Grocery Prices
Pure Python solution - bypasses n8n completely
Fetches live prices from BigBasket, Zepto, Swiggy using Bright Data proxy
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from datetime import datetime
from typing import Dict, List, Optional
import os

class BrightDataGroceryScraper:
    """
    Direct integration with Bright Data for real-time grocery scraping.
    No n8n needed - pure Python with Bright Data proxy.
    """
    
    def __init__(self, location: str = "Chennai"):
        """
        Initialize with Bright Data credentials.
        
        Args:
            location: City for location-based pricing (default: Chennai)
        """
        # Your Bright Data credentials
        self.proxy_url = "http://brd-customer-hl_dde66e96-zone-webscrape:18y4rj198mpn@brd.superproxy.io:33335"
        self.location = location
        
        # Proxy configuration for requests
        self.proxies = {
            'http': self.proxy_url,
            'https': self.proxy_url
        }
        
        # Headers to look like a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Cache for prices (1 hour expiry)
        self.cache_file = "brightdata_price_cache.json"
        self.cache_duration = 3600  # 1 hour
        
        # Fallback prices (same as before)
        self.FALLBACK_PRICES = {
            # Grains & Staples
            "rice": 60, "basmati rice": 120, "brown rice": 80,
            "wheat flour": 40, "atta": 42, "maida": 35, "besan": 80,
            "gram flour": 80, "chickpea flour": 80, "corn flour": 60,
            "semolina": 45, "rava": 45, "rice flour": 55,
            
            # Pulses & Lentils
            "dal": 100, "moong dal": 110, "toor dal": 120,
            "urad dal": 130, "chana dal": 90, "masoor dal": 95,
            "pigeon peas": 85, "chickpeas": 80, "chole": 85,
            "red kidney beans": 140, "rajma": 140,
            
            # Vegetables
            "tomato": 50, "tomatoes": 50, "potato": 30, "potatoes": 30,
            "onion": 40, "red onion": 45, "garlic": 120, "ginger": 100,
            "cauliflower": 35, "cabbage": 30, "carrot": 40,
            "beans": 60, "green beans": 60, "peas": 80, "green peas": 80,
            "capsicum": 60, "bell pepper": 60, "bell peppers": 60, "shimla mirch": 60,
            "brinjal": 40, "eggplant": 40, "bhindi": 50, "ladies finger": 50,
            "palak": 40, "spinach": 40, "methi": 60, "fenugreek leaves": 60,
            "bottle gourd": 30, "bitter gourd": 40, "cucumber": 35,
            "mushroom": 150, "wild mushrooms": 180, "baby corn": 120,
            
            # Dairy
            "milk": 60, "curd": 50, "yogurt": 55, "greek yogurt": 80,
            "paneer": 350, "cottage cheese": 350, "cheese": 400,
            "butter": 400, "ghee": 500, "cream": 80, "malai": 70,
            "whipping cream": 120,
            
            # Spices & Seasonings
            "turmeric": 200, "haldi": 200, "chili powder": 180, "chilli powder": 180,
            "coriander powder": 150, "cumin": 300, "mustard seeds": 200,
            "fenugreek seeds": 180, "curry leaves": 20, "bay leaf": 400,
            "cinnamon": 800, "cinnamon stick": 800, "cardamom": 1200,
            "cloves": 1500, "black pepper": 600, "garam masala": 300,
            "garam masala powder": 300, "tandoori masala": 250,
            "kasuri methi": 150, "amchur powder": 200,
            
            # Oils
            "oil": 150, "cooking oil": 150, "sunflower oil": 140,
            "mustard oil": 180, "coconut oil": 200, "olive oil": 600,
            "sesame oil": 250, "groundnut oil": 160,
            
            # Others
            "salt": 20, "sugar": 45, "jaggery": 60, "gur": 60,
            "tamarind": 150, "imli": 150, "coconut": 35,
            "cashew nuts": 700, "almonds": 800, "raisins": 350,
            "honey": 350, "sesame seeds": 180, "poppy seeds": 400,
            "bread crumbs": 100, "cornflakes": 180
        }
    
    def fetch_bigbasket_price(self, item: str) -> Optional[float]:
        """
        Fetch real-time price from BigBasket using Bright Data proxy.
        
        Args:
            item: Item name (e.g., "rice", "dal")
            
        Returns:
            Price in Rs or None if not found
        """
        try:
            # Clean item for URL
            search_term = item.lower().replace(' ', '%20')
            url = f"https://www.bigbasket.com/ps/?q={search_term}"
            
            # print(f"   Scraping BigBasket for: {item}")
            
            response = requests.get(
                url,
                proxies=self.proxies,
                headers=self.headers,
                timeout=30,
                verify=False  # Ignore SSL with proxy
            )
            
            if response.status_code == 200:
                # Extract all prices with ₹ symbol (most reliable pattern)
                prices = re.findall(r'₹[\s]*(\d+(?:,\d{3})*(?:\.\d{2})?)', response.text)
                
                if prices:
                    # Convert to floats and filter reasonable range
                    valid_prices = []
                    for price_str in prices[:20]:  # Check first 20 matches
                        try:
                            price = float(price_str.replace(',', ''))
                            if 10 <= price <= 10000:  # Reasonable range
                                valid_prices.append(price)
                        except:
                            continue
                    
                    if valid_prices:
                        # Return median price for better accuracy
                        valid_prices.sort()
                        median_price = valid_prices[len(valid_prices) // 2]
                        print(f"   ✓ BigBasket: Rs {median_price:.2f}")
                        return median_price
            
            return None
            
        except Exception as e:
            print(f"   ✗ BigBasket error: {str(e)[:50]}")
            return None
    
    def fetch_zepto_price(self, item: str) -> Optional[float]:
        """Fetch from Zepto"""
        try:
            search_term = item.lower().replace(' ', '%20')
            url = f"https://www.zeptonow.com/search?query={search_term}"
            
            # print(f"   Scraping Zepto for: {item}")
            
            response = requests.get(
                url,
                proxies=self.proxies,
                headers=self.headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                # Extract prices
                prices = re.findall(r'₹[\s]*(\d+(?:\.\d{2})?)', response.text)
                
                if prices:
                    valid_prices = []
                    for price_str in prices[:20]:
                        try:
                            price = float(price_str)
                            if 10 <= price <= 10000:
                                valid_prices.append(price)
                        except:
                            continue
                    
                    if valid_prices:
                        valid_prices.sort()
                        median_price = valid_prices[len(valid_prices) // 2]
                        print(f"   ✓ Zepto: Rs {median_price:.2f}")
                        return median_price
            
            return None
            
        except Exception as e:
            print(f"   ✗ Zepto error: {str(e)[:50]}")
            return None
            return None
            
        except Exception as e:
            print(f"   ✗ Zepto error: {str(e)[:50]}")
            return None
    
    def fetch_swiggy_price(self, item: str) -> Optional[float]:
        """Fetch from Swiggy Instamart"""
        try:
            search_term = item.lower().replace(' ', '%20')
            url = f"https://www.swiggy.com/instamart/search?query={search_term}"
            
            # print(f"   Scraping Swiggy for: {item}")
            
            response = requests.get(
                url,
                proxies=self.proxies,
                headers=self.headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                # Extract prices
                prices = re.findall(r'₹[\s]*(\d+(?:\.\d{2})?)', response.text)
                
                if prices:
                    valid_prices = []
                    for price_str in prices[:20]:
                        try:
                            price = float(price_str)
                            if 10 <= price <= 10000:
                                valid_prices.append(price)
                        except:
                            continue
                    
                    if valid_prices:
                        valid_prices.sort()
                        median_price = valid_prices[len(valid_prices) // 2]
                        print(f"   ✓ Swiggy: Rs {median_price:.2f}")
                        return median_price
            
            return None
            
        except Exception as e:
            print(f"   ✗ Swiggy error: {str(e)[:50]}")
            return None
    
    def get_realtime_price(self, item: str) -> float:
        """
        Get real-time price with multi-store averaging and fallback.
        
        Args:
            item: Ingredient name
            
        Returns:
            Price in Rs (always returns a value)
        """
        item_lower = item.lower().strip()
        
        # Check cache first
        cached = self._get_cached_price(item_lower)
        if cached:
            print(f"   >> Cached: {item} = Rs {cached}")
            return cached
        
        # Try scraping from all 3 stores
        prices = []
        
        # BigBasket
        price = self.fetch_bigbasket_price(item)
        if price:
            prices.append(price)
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
        
        # Zepto
        price = self.fetch_zepto_price(item)
        if price:
            prices.append(price)
        
        time.sleep(0.5)
        
        # Swiggy
        price = self.fetch_swiggy_price(item)
        if price:
            prices.append(price)
        
        # Calculate average if we got prices
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"   >> Real-time: {item} = Rs {avg_price:.2f} (from {len(prices)} stores)")
            self._cache_price(item_lower, avg_price)
            return avg_price
        
        # Fallback to database
        fallback = self.FALLBACK_PRICES.get(item_lower, 80)
        print(f"   >> Fallback: {item} = Rs {fallback}")
        return fallback
    
    def _get_cached_price(self, item: str) -> Optional[float]:
        """Check if price is in cache and still valid"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                    
                    # Check expiry
                    cache_time = datetime.fromisoformat(cache.get('timestamp', ''))
                    if (datetime.now() - cache_time).seconds < self.cache_duration:
                        return cache.get('prices', {}).get(item)
        except:
            pass
        return None
    
    def _cache_price(self, item: str, price: float):
        """Save price to cache"""
        try:
            cache = {}
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
            
            if 'prices' not in cache:
                cache['prices'] = {}
            
            cache['prices'][item] = price
            cache['timestamp'] = datetime.now().isoformat()
            cache['location'] = self.location
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
                
        except Exception as e:
            print(f"   Cache save error: {e}")


class BrightDataCostEstimator:
    """
    Cost estimator using Bright Data for real-time prices.
    Drop-in replacement for RealTimeCostEstimator!
    """
    
    def __init__(self, location: str = "Chennai"):
        self.scraper = BrightDataGroceryScraper(location)
        self.location = location
        print(f">> Bright Data Real-Time Pricing: Enabled")
        print(f">> Location: {location}")
    
    def estimate_dish_cost(self, ingredients: str, servings: int = 2) -> float:
        """
        Estimate dish cost using real-time prices from Bright Data.
        
        Args:
            ingredients: Comma-separated ingredient string
            servings: Number of servings
            
        Returns:
            Total cost in Rupees
        """
        total_cost = 0
        ingredient_list = [i.strip().lower() for i in ingredients.split(',')]
        
        for ingredient in ingredient_list:
            if not ingredient:
                continue
            
            # Get real-time price
            price_per_kg = self.scraper.get_realtime_price(ingredient)
            
            # Estimate quantity based on ingredient type
            if any(grain in ingredient for grain in ['rice', 'wheat', 'flour', 'atta', 'maida', 'rava']):
                quantity = 0.15 * servings  # 150g per serving
            elif any(veg in ingredient for veg in ['tomato', 'potato', 'onion', 'carrot', 'beans']):
                quantity = 0.1 * servings  # 100g per serving
            elif 'paneer' in ingredient or 'cheese' in ingredient:
                quantity = 0.1 * servings  # 100g per serving
            elif 'dal' in ingredient or 'lentil' in ingredient:
                quantity = 0.08 * servings  # 80g per serving
            elif any(spice in ingredient for spice in ['turmeric', 'chili', 'cumin', 'masala']):
                quantity = 0.005 * servings  # 5g per serving
            elif 'oil' in ingredient or 'ghee' in ingredient:
                quantity = 0.02 * servings  # 20ml per serving
            else:
                quantity = 0.05 * servings  # Default 50g
            
            item_cost = price_per_kg * quantity
            total_cost += item_cost
        
        return round(total_cost, 2)


# Example usage and testing
if __name__ == "__main__":
    print("="*70)
    print("BRIGHT DATA REAL-TIME GROCERY PRICE SCRAPER")
    print("="*70)
    print("\nLocation: Chennai")
    print("Stores: BigBasket, Zepto, Swiggy Instamart")
    print("\n" + "="*70)
    
    # Initialize
    estimator = BrightDataCostEstimator(location="Chennai")
    
    # Test with sample dishes
    test_dishes = [
        ("Sambar", "dal, tomato, drumstick, tamarind, sambar powder, curry leaves, oil"),
        ("Paneer Butter Masala", "paneer, tomato, butter, cream, onion, garam masala, oil"),
        ("Dal Tadka", "dal, tomato, onion, garlic, cumin, turmeric, ghee")
    ]
    
    print("\n" + "="*70)
    print("TESTING REAL-TIME PRICE ESTIMATION")
    print("="*70)
    
    for dish_name, ingredients in test_dishes:
        print(f"\n📝 {dish_name}")
        print(f"   Ingredients: {ingredients[:60]}...")
        cost = estimator.estimate_dish_cost(ingredients, servings=2)
        print(f"   💰 Total Cost: Rs {cost:.2f} (for 2 servings)")
        print("-" * 70)
    
    print("\n✅ Real-time pricing system ready!")
    print("   - Fetches live prices from grocery stores")
    print("   - Uses Bright Data proxy to bypass restrictions")
    print("   - Caches prices for 1 hour")
    print("   - Falls back to database if scraping fails")
