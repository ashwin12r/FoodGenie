"""
n8n Integration for Real-Time Grocery Pricing
Calls n8n workflow via ngrok tunnel to scrape prices using Bright Data
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import os

class N8nGroceryPriceFetcher:
    """
    Fetches grocery prices via n8n workflow with Bright Data scraping.
    Much more reliable than direct scraping!
    """
    
    def __init__(self, n8n_webhook_url: str, location: str = "Chennai"):
        """
        Initialize with n8n webhook URL (ngrok URL)
        
        Args:
            n8n_webhook_url: Your ngrok URL like "https://abc123.ngrok.io/webhook/grocery-prices"
            location: City for location-based pricing
        """
        self.webhook_url = n8n_webhook_url
        self.location = location
        self.cache_file = "n8n_price_cache.json"
        self.cache_duration = 3600  # 1 hour
        
    def fetch_prices(self, items: List[str]) -> Dict[str, float]:
        """
        Fetch prices for multiple items via n8n workflow.
        
        Args:
            items: List of ingredient names like ["rice", "dal", "tomato"]
            
        Returns:
            Dictionary of {item_name: price_per_kg}
        """
        # Check cache first
        cached_prices = self._load_cache()
        if cached_prices:
            # Return cached prices if all items found
            missing_items = [item for item in items if item not in cached_prices]
            if not missing_items:
                print(f"   >> Using cached prices ({len(items)} items)")
                return {item: cached_prices[item] for item in items}
        
        print(f"   >> Fetching {len(items)} prices via n8n + Bright Data...")
        
        try:
            # Send request to n8n webhook
            payload = {
                "items": items,
                "location": self.location,
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=120  # 2 minutes - scraping takes time
            )
            
            if response.status_code == 200:
                data = response.json()
                prices = data.get('prices', {})
                
                # Merge with cache
                cached_prices.update(prices)
                self._save_cache(cached_prices)
                
                success_rate = len(prices) / len(items) * 100
                print(f"   >> Success: {len(prices)}/{len(items)} items ({success_rate:.0f}%)")
                
                return prices
            else:
                print(f"   >> n8n error: Status {response.status_code}")
                return {}
                
        except requests.exceptions.Timeout:
            print(f"   >> n8n timeout (scraping took too long)")
            return {}
        except Exception as e:
            print(f"   >> n8n fetch error: {e}")
            return {}
    
    def fetch_single_price(self, item: str) -> Optional[float]:
        """Fetch price for a single item"""
        prices = self.fetch_prices([item])
        return prices.get(item)
    
    def _load_cache(self) -> Dict[str, float]:
        """Load cached prices"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                    cache_time = datetime.fromisoformat(cache['timestamp'])
                    
                    # Check if cache is still valid
                    if (datetime.now() - cache_time).seconds < self.cache_duration:
                        return cache.get('prices', {})
        except Exception:
            pass
        return {}
    
    def _save_cache(self, prices: Dict[str, float]):
        """Save prices to cache"""
        try:
            cache = {
                'timestamp': datetime.now().isoformat(),
                'location': self.location,
                'prices': prices
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
            print(f"   >> Cached {len(prices)} prices")
        except Exception as e:
            print(f"   >> Cache save error: {e}")


class N8nCostEstimator:
    """
    Integrates n8n price fetcher with MealCraft-AI.
    Drop-in replacement for RealTimeCostEstimator!
    """
    
    def __init__(self, n8n_webhook_url: str, location: str = "Chennai"):
        self.fetcher = N8nGroceryPriceFetcher(n8n_webhook_url, location)
        self.base_costs = {}  # Cache for ingredient costs
        
        # Fallback prices (same as before)
        self.FALLBACK_PRICES = {
            "rice": 60, "dal": 100, "tomato": 50, "potato": 30,
            "onion": 40, "garlic": 120, "ginger": 100, "oil": 150,
            "paneer": 350, "milk": 60, "curd": 50, "ghee": 500,
            # ... add more as needed
        }
    
    def estimate_dish_cost(self, ingredients: str, servings: int = 2) -> float:
        """
        Estimate total cost of a dish using n8n scraping.
        
        Args:
            ingredients: Comma-separated ingredient string
            servings: Number of servings (default 2)
            
        Returns:
            Total estimated cost in Rupees
        """
        total_cost = 0
        ingredient_list = [i.strip().lower() for i in ingredients.split(',')]
        
        # Batch fetch all missing prices
        missing = [ing for ing in ingredient_list if ing not in self.base_costs]
        if missing:
            fetched = self.fetcher.fetch_prices(missing)
            self.base_costs.update(fetched)
        
        # Calculate cost
        for ingredient in ingredient_list:
            # Try cached price from n8n
            if ingredient in self.base_costs:
                price = self.base_costs[ingredient]
            # Try fallback
            elif ingredient in self.FALLBACK_PRICES:
                price = self.FALLBACK_PRICES[ingredient]
            else:
                price = 80  # Default estimate
            
            # Estimate quantity (same logic as before)
            if any(grain in ingredient for grain in ['rice', 'wheat', 'flour', 'atta']):
                quantity = 0.15 * servings
            elif any(veg in ingredient for veg in ['tomato', 'potato', 'onion']):
                quantity = 0.1 * servings
            elif 'paneer' in ingredient or 'cheese' in ingredient:
                quantity = 0.1 * servings
            else:
                quantity = 0.05 * servings
            
            total_cost += (price * quantity)
        
        return round(total_cost, 2)


# Example usage
if __name__ == "__main__":
    # Your ngrok URL (you'll get this after running: ngrok http 5678)
    N8N_WEBHOOK = "https://YOUR-NGROK-URL.ngrok.io/webhook/grocery-prices"
    
    # Test the system
    estimator = N8nCostEstimator(N8N_WEBHOOK, location="Chennai")
    
    # Test dish
    ingredients = "rice, dal, tomato, onion, turmeric, oil"
    cost = estimator.estimate_dish_cost(ingredients, servings=2)
    
    print(f"\nDish cost: Rs {cost:.2f}")
