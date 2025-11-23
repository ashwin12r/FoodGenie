"""
Real-time Grocery Price Scraper
Fetches current prices from BigBasket, Zepto, Swiggy Instamart
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional
import geocoder
import os

class GroceryPriceScraper:
    """
    Scrapes real-time grocery prices from multiple online stores.
    """
    
    def __init__(self, location: Optional[str] = None):
        """
        Initialize scraper with location detection.
        
        Args:
            location: Manual location (city name) or None for auto-detect
        """
        self.location = location or self._detect_location()
        self.cache_file = "price_cache.json"
        self.cache_duration = 3600  # 1 hour cache
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        print(f">> Location detected: {self.location}")
    
    def _detect_location(self) -> str:
        """Auto-detect user location using IP geolocation"""
        try:
            g = geocoder.ip('me')
            if g.ok:
                city = g.city or "Mumbai"  # Default to Mumbai
                print(f">> Auto-detected location: {city}")
                return city
            else:
                print(">> Location detection failed, using default: Mumbai")
                return "Mumbai"
        except Exception as e:
            print(f">> Location detection error: {e}, using default: Mumbai")
            return "Mumbai"
    
    def _load_cache(self) -> Dict:
        """Load cached prices if available and not expired"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                
                # Check if cache is still valid
                cache_time = datetime.fromisoformat(cache.get('timestamp', '2000-01-01'))
                if (datetime.now() - cache_time).seconds < self.cache_duration:
                    print(f">> Using cached prices (age: {(datetime.now() - cache_time).seconds // 60} minutes)")
                    return cache.get('prices', {})
        except Exception as e:
            print(f">> Cache load error: {e}")
        
        return {}
    
    def _save_cache(self, prices: Dict):
        """Save prices to cache"""
        try:
            cache = {
                'timestamp': datetime.now().isoformat(),
                'location': self.location,
                'prices': prices
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, indent=2, ensure_ascii=False)
            print(f">> Prices cached successfully")
        except Exception as e:
            print(f">> Cache save error: {e}")
    
    def fetch_bigbasket_price(self, item_name: str) -> Optional[float]:
        """
        Fetch price from BigBasket (web scraping).
        Note: BigBasket has anti-scraping measures, this is a simplified approach.
        """
        try:
            # Clean item name for search
            search_term = item_name.lower().replace(' ', '+')
            url = f"https://www.bigbasket.com/ps/?q={search_term}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # BigBasket uses different class names, try multiple patterns
                price_patterns = [
                    {'class': 'discnt-price'},
                    {'class': 'prod-price'},
                    {'class': 'sale-price'},
                    {'data-testid': 'product-price'}
                ]
                
                for pattern in price_patterns:
                    price_elem = soup.find('span', pattern)
                    if price_elem:
                        price_text = price_elem.text.strip()
                        # Extract number from price text (₹123 or 123.45)
                        match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                        if match:
                            return float(match.group())
            
            return None
        
        except Exception as e:
            print(f"   BigBasket error for {item_name}: {e}")
            return None
    
    def fetch_zepto_price(self, item_name: str) -> Optional[float]:
        """
        Fetch price from Zepto.
        Note: Zepto uses React/Next.js, requires API approach.
        """
        try:
            # Zepto API endpoint (may change)
            search_term = item_name.lower().replace(' ', '%20')
            
            # Try Zepto's search API (this is a mock - actual API may differ)
            api_url = f"https://www.zeptonow.com/api/v1/search?query={search_term}"
            
            headers_with_token = self.headers.copy()
            # Zepto may require auth token - this is placeholder
            
            response = requests.get(api_url, headers=headers_with_token, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse response (structure may vary)
                if 'products' in data and len(data['products']) > 0:
                    first_product = data['products'][0]
                    price = first_product.get('price', {}).get('mrp', None)
                    if price:
                        return float(price)
            
            return None
        
        except Exception as e:
            print(f"   Zepto error for {item_name}: {e}")
            return None
    
    def fetch_swiggy_instamart_price(self, item_name: str) -> Optional[float]:
        """
        Fetch price from Swiggy Instamart.
        Note: Swiggy uses GraphQL API.
        """
        try:
            # Swiggy Instamart API (simplified)
            search_term = item_name.lower()
            
            # Swiggy uses GraphQL - this is a mock structure
            api_url = "https://www.swiggy.com/api/instamart/search"
            
            payload = {
                'query': search_term,
                'lat': 19.0760,  # Mumbai coordinates (should be dynamic)
                'lng': 72.8777
            }
            
            response = requests.post(api_url, json=payload, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse Swiggy response structure
                if 'data' in data and 'items' in data['data']:
                    items = data['data']['items']
                    if len(items) > 0:
                        price = items[0].get('price', None)
                        if price:
                            return float(price)
            
            return None
        
        except Exception as e:
            print(f"   Swiggy error for {item_name}: {e}")
            return None
    
    def get_average_price(self, item_name: str, quantity: str = "1 kg") -> float:
        """
        Get average price from multiple sources with fallback.
        
        Args:
            item_name: Name of grocery item (e.g., "rice", "tomato")
            quantity: Quantity/unit (e.g., "1 kg", "500 g")
        
        Returns:
            Average price or estimated fallback price
        """
        print(f"\n   Fetching price for: {item_name} ({quantity})")
        
        # Check cache first
        cache = self._load_cache()
        cache_key = f"{item_name.lower()}_{quantity}"
        
        if cache_key in cache:
            print(f"   >> Cache hit: Rs{cache[cache_key]:.2f}")
            return cache[cache_key]
        
        prices = []
        
        # Try BigBasket
        bb_price = self.fetch_bigbasket_price(item_name)
        if bb_price:
            print(f"   >> BigBasket: Rs{bb_price:.2f}")
            prices.append(bb_price)
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
        
        # Try Zepto
        zepto_price = self.fetch_zepto_price(item_name)
        if zepto_price:
            print(f"   >> Zepto: Rs{zepto_price:.2f}")
            prices.append(zepto_price)
        
        time.sleep(0.5)
        
        # Try Swiggy Instamart
        swiggy_price = self.fetch_swiggy_instamart_price(item_name)
        if swiggy_price:
            print(f"   >> Swiggy: Rs{swiggy_price:.2f}")
            prices.append(swiggy_price)
        
        # Calculate average or use fallback
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"   >> Average from {len(prices)} source(s): Rs{avg_price:.2f}")
            
            # Update cache
            cache[cache_key] = avg_price
            self._save_cache(cache)
            
            return avg_price
        else:
            # Fallback to estimated prices
            fallback_price = self._get_fallback_price(item_name, quantity)
            print(f"   >> Using fallback estimate: Rs{fallback_price:.2f}")
            return fallback_price
    
    def _get_fallback_price(self, item_name: str, quantity: str) -> float:
        """
        Fallback price estimates based on typical Indian grocery prices.
        Updated regularly based on market trends.
        """
        # Comprehensive fallback price database (per kg/liter unless specified)
        fallback_prices = {
            # Grains & Cereals (per kg)
            'rice': 60, 'basmati rice': 120, 'brown rice': 90,
            'wheat flour': 40, 'atta': 40, 'maida': 35,
            'rava': 45, 'semolina': 45, 'suji': 45,
            'pearl millet': 50, 'bajra': 50,
            'ragi': 80, 'finger millet': 80,
            
            # Pulses/Lentils (per kg)
            'dal': 100, 'toor dal': 120, 'arhar dal': 120,
            'moong dal': 110, 'urad dal': 130,
            'chana dal': 90, 'masoor dal': 100,
            'rajma': 140, 'kidney beans': 140,
            'chickpeas': 80, 'kabuli chana': 90,
            'black gram': 130, 'green gram': 110,
            
            # Vegetables (per kg)
            'potato': 30, 'aloo': 30,
            'onion': 40, 'pyaz': 40,
            'tomato': 50, 'tamatar': 50,
            'cauliflower': 40, 'gobi': 40,
            'cabbage': 30, 'patta gobi': 30,
            'carrot': 45, 'gajar': 45,
            'beans': 60, 'french beans': 60,
            'peas': 80, 'matar': 80,
            'okra': 50, 'bhindi': 50, 'ladyfinger': 50,
            'eggplant': 45, 'brinjal': 45, 'baingan': 45,
            'spinach': 40, 'palak': 40,
            'methi': 60, 'fenugreek': 60,
            'coriander': 20, 'cilantro': 20, 'dhania': 20,
            'curry leaves': 15,
            'green chili': 80, 'chilli': 80,
            'ginger': 100, 'adrak': 100,
            'garlic': 120, 'lehsun': 120,
            'capsicum': 60, 'bell pepper': 60,
            'mushroom': 150,
            
            # Dairy (per liter/kg)
            'milk': 60, 'doodh': 60,
            'curd': 60, 'yogurt': 60, 'dahi': 60,
            'paneer': 350, 'cottage cheese': 350,
            'ghee': 500, 'clarified butter': 500,
            'butter': 400,
            'cheese': 450,
            
            # Oils (per liter)
            'oil': 150, 'cooking oil': 150,
            'mustard oil': 180, 'sarso ka tel': 180,
            'coconut oil': 200,
            'groundnut oil': 170, 'peanut oil': 170,
            'sunflower oil': 160,
            
            # Spices (per 100g)
            'turmeric': 40, 'haldi': 40,
            'chili powder': 50, 'lal mirch': 50,
            'coriander powder': 30, 'dhania powder': 30,
            'cumin': 60, 'jeera': 60,
            'mustard seeds': 50, 'rai': 50,
            'fenugreek seeds': 40, 'methi seeds': 40,
            'cardamom': 1200, 'elaichi': 1200,
            'cinnamon': 400, 'dalchini': 400,
            'cloves': 1000, 'laung': 1000,
            'bay leaf': 200, 'tej patta': 200,
            'garam masala': 300,
            'asafoetida': 800, 'hing': 800,
            
            # Nuts & Dry Fruits (per kg)
            'cashew': 700, 'kaju': 700,
            'almonds': 800, 'badam': 800,
            'raisins': 400, 'kishmish': 400,
            'peanuts': 120, 'moongfali': 120,
            'coconut': 50, 'nariyal': 50,
            
            # Sweeteners (per kg)
            'sugar': 45, 'chini': 45,
            'jaggery': 60, 'gur': 60,
            'honey': 350, 'shahad': 350,
            
            # Others
            'salt': 20, 'namak': 20,
            'tamarind': 150, 'imli': 150,
            'papad': 100,
            'pickle': 150, 'achar': 150,
            'soy sauce': 120,
            'vinegar': 80,
            'baking soda': 60,
            'baking powder': 150,
        }
        
        # Normalize item name
        item_lower = item_name.lower().strip()
        
        # Direct match
        if item_lower in fallback_prices:
            base_price = fallback_prices[item_lower]
        else:
            # Fuzzy match - check if any key is contained in item name
            matched = False
            for key, price in fallback_prices.items():
                if key in item_lower or item_lower in key:
                    base_price = price
                    matched = True
                    break
            
            if not matched:
                # Generic vegetable/ingredient price
                if any(word in item_lower for word in ['vegetable', 'sabzi', 'green']):
                    base_price = 50
                elif any(word in item_lower for word in ['dal', 'lentil', 'pulse']):
                    base_price = 100
                elif any(word in item_lower for word in ['spice', 'masala']):
                    base_price = 200
                else:
                    base_price = 80  # Generic fallback
        
        # Adjust for quantity if specified
        if 'g' in quantity.lower() or 'gram' in quantity.lower():
            # Extract grams
            match = re.search(r'(\d+)', quantity)
            if match:
                grams = int(match.group(1))
                if grams < 1000:
                    # Price is per kg, adjust for grams
                    return base_price * (grams / 1000)
        
        return base_price
    
    def fetch_all_ingredient_prices(self, ingredients: List[str]) -> Dict[str, float]:
        """
        Fetch prices for a list of ingredients.
        
        Args:
            ingredients: List of ingredient names
        
        Returns:
            Dictionary mapping ingredient to price
        """
        print(f"\n{'='*70}")
        print(f"FETCHING PRICES FOR {len(ingredients)} INGREDIENTS")
        print(f"Location: {self.location}")
        print(f"{'='*70}")
        
        prices = {}
        
        for ingredient in ingredients:
            price = self.get_average_price(ingredient)
            prices[ingredient] = price
        
        print(f"\n{'='*70}")
        print(f"PRICE FETCH COMPLETE")
        print(f"{'='*70}\n")
        
        return prices


# Integration with MealCraft-AI
class RealTimeCostEstimator:
    """
    Real-time cost estimator using live grocery prices.
    Replaces static cost estimation with dynamic web scraping.
    """
    
    def __init__(self, location: Optional[str] = None):
        """
        Initialize with price scraper.
        
        Args:
            location: User location (city) or None for auto-detect
        """
        self.scraper = GroceryPriceScraper(location)
        self.base_costs = {}  # Cache of ingredient costs
        
    def estimate_dish_cost(self, ingredients: str, servings: int = 2) -> float:
        """
        Estimate dish cost based on real-time ingredient prices.
        
        Args:
            ingredients: Comma-separated ingredient string
            servings: Number of servings (default 2)
        
        Returns:
            Estimated cost in rupees
        """
        if not ingredients or ingredients == '-1':
            return 50.0  # Default fallback
        
        ingredient_list = [ing.strip().lower() for ing in ingredients.split(',')]
        
        total_cost = 0.0
        
        for ingredient in ingredient_list:
            # Get or fetch price
            if ingredient not in self.base_costs:
                self.base_costs[ingredient] = self.scraper.get_average_price(ingredient)
            
            # Assume ~50g per ingredient per serving
            ingredient_cost = self.base_costs[ingredient] * 0.05 * servings
            total_cost += ingredient_cost
        
        return round(total_cost, 2)
    
    def update_price_cache(self, force: bool = False):
        """
        Update the price cache.
        
        Args:
            force: Force refresh even if cache is valid
        """
        if force:
            # Clear cache file to force refresh
            if os.path.exists(self.scraper.cache_file):
                os.remove(self.scraper.cache_file)
                print(">> Price cache cleared, will fetch fresh prices")


# Example usage and testing
if __name__ == "__main__":
    print("="*70)
    print("REAL-TIME GROCERY PRICE SCRAPER TEST")
    print("="*70)
    
    # Initialize scraper
    scraper = GroceryPriceScraper()
    
    # Test with common ingredients
    test_ingredients = [
        'rice',
        'tomato',
        'onion',
        'potato',
        'dal',
        'oil',
        'paneer',
        'milk',
        'flour'
    ]
    
    print("\nTesting price fetch for common ingredients...")
    prices = scraper.fetch_all_ingredient_prices(test_ingredients)
    
    print("\n" + "="*70)
    print("PRICE SUMMARY")
    print("="*70)
    
    for ingredient, price in prices.items():
        print(f"{ingredient.title():20s} : Rs {price:.2f}")
    
    print("\n" + "="*70)
    print("REAL-TIME COST ESTIMATOR TEST")
    print("="*70)
    
    # Test cost estimator
    estimator = RealTimeCostEstimator()
    
    # Example dish
    test_dish = "rice, dal, tomato, onion, oil, spices"
    cost = estimator.estimate_dish_cost(test_dish, servings=2)
    
    print(f"\nDish: {test_dish}")
    print(f"Servings: 2")
    print(f"Estimated Cost: Rs {cost:.2f}")
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
