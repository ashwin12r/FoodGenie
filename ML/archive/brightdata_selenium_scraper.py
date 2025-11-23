"""
Bright Data + Selenium Scraper for Real-Time Grocery Prices
Uses Selenium with headless Chrome through Bright Data proxy to scrape JavaScript-rendered pages
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class BrightDataSeleniumScraper:
    """
    Grocery price scraper using Selenium + Bright Data proxy.
    Handles JavaScript-rendered pages from BigBasket, Zepto, Swiggy.
    """
    
    def __init__(self, location: str = "Chennai"):
        self.location = location
        
        # Bright Data proxy
        self.proxy_url = "brd.superproxy.io:33335"
        self.proxy_user = "brd-customer-hl_dde66e96-zone-webscrape"
        self.proxy_pass = "18y4rj198mpn"
        
        # Cache settings
        self.cache_file = "brightdata_selenium_cache.json"
        self.cache_duration = timedelta(hours=1)
        self.cache = self._load_cache()
        
        # Fallback database
        self.fallback_prices = self._build_fallback_database()
        
    def _load_cache(self) -> Dict:
        """Load price cache from file"""
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
                # Convert string timestamps back to datetime
                for item in cache:
                    if 'timestamp' in cache[item]:
                        cache[item]['timestamp'] = datetime.fromisoformat(cache[item]['timestamp'])
                return cache
        except:
            return {}
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            # Convert datetime to ISO string for JSON
            cache_copy = {}
            for item in self.cache:
                cache_copy[item] = {
                    'price': self.cache[item]['price'],
                    'timestamp': self.cache[item]['timestamp'].isoformat()
                }
            with open(self.cache_file, 'w') as f:
                json.dump(cache_copy, f, indent=2)
        except Exception as e:
            print(f"   ⚠ Cache save error: {e}")
    
    def _get_cached_price(self, item: str) -> Optional[float]:
        """Get cached price if valid"""
        item_key = item.lower().strip()
        if item_key in self.cache:
            cached = self.cache[item_key]
            if datetime.now() - cached['timestamp'] < self.cache_duration:
                print(f"   📦 Cache hit: {item} = Rs {cached['price']}")
                return cached['price']
        return None
    
    def _cache_price(self, item: str, price: float):
        """Cache a price"""
        self.cache[item.lower().strip()] = {
            'price': price,
            'timestamp': datetime.now()
        }
        self._save_cache()
    
    def _build_fallback_database(self) -> Dict[str, float]:
        """Comprehensive fallback prices (Rs per kg/liter unless noted)"""
        return {
            # Grains
            "rice": 60, "basmati rice": 120, "ponni rice": 70, "sona masoori": 75,
            "wheat flour": 40, "atta": 40, "maida": 35, "sooji": 45, "rava": 45,
            
            # Pulses
            "dal": 100, "toor dal": 110, "moong dal": 120, "chana dal": 100,
            "urad dal": 130, "masoor dal": 90, "rajma": 140,
            
            # Vegetables (per kg)
            "tomato": 50, "potato": 30, "onion": 40, "garlic": 120, "ginger": 100,
            "cauliflower": 35, "cabbage": 30, "carrot": 40, "beans": 60,
            "peas": 80, "capsicum": 60, "bell pepper": 60, "brinjal": 40,
            "bhindi": 50, "palak": 40, "spinach": 40, "mushroom": 150,
            
            # Dairy
            "milk": 60, "curd": 50, "paneer": 350, "butter": 400,
            "ghee": 500, "cream": 80, "cheese": 400,
            
            # Spices (per 100g)
            "turmeric": 200, "chili powder": 180, "coriander powder": 150,
            "cumin": 300, "mustard seeds": 200, "curry leaves": 20,
            "garam masala": 300,
            
            # Oils (per liter)
            "oil": 150, "sunflower oil": 140, "mustard oil": 180,
            "coconut oil": 200, "olive oil": 600,
            
            # Others
            "salt": 20, "sugar": 45, "tamarind": 150, "coconut": 35,
            "cashew nuts": 700, "almonds": 800
        }
    
    def _create_driver(self) -> webdriver.Chrome:
        """Create Chrome driver with Bright Data proxy"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Configure Bright Data proxy
        proxy_full = f"{self.proxy_user}:{self.proxy_pass}@{self.proxy_url}"
        chrome_options.add_argument(f'--proxy-server=http://{proxy_full}')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        
        return driver
    
    def fetch_bigbasket_price(self, item: str) -> Optional[float]:
        """
        Fetch price from BigBasket using Selenium.
        BigBasket uses React - prices are loaded dynamically via JS.
        """
        driver = None
        try:
            print(f"   🔍 Scraping BigBasket for: {item}")
            
            search_term = item.lower().replace(' ', '+')
            url = f"https://www.bigbasket.com/ps/?q={search_term}"
            
            driver = self._create_driver()
            driver.get(url)
            
            # Wait for product cards to load
            wait = WebDriverWait(driver, 15)
            
            # BigBasket price selectors (they change frequently)
            price_selectors = [
                "span[class*='Price']",
                "div[class*='price']",
                "span[class*='selling-price']",
                "[data-qa='product-price']"
            ]
            
            for selector in price_selectors:
                try:
                    price_elements = wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                    )
                    
                    # Extract prices from elements
                    for elem in price_elements[:5]:  # Check first 5
                        text = elem.text.strip()
                        # Look for ₹XX or Rs XX patterns
                        match = re.search(r'[₹Rs\s]*(\d+(?:,\d{3})*(?:\.\d{2})?)', text)
                        if match:
                            price = float(match.group(1).replace(',', ''))
                            if 10 <= price <= 10000:  # Reasonable range
                                print(f"   ✓ BigBasket: Rs {price}")
                                return price
                except TimeoutException:
                    continue
            
            # If no price found with selectors, try regex on page source
            page_source = driver.page_source
            price_match = re.search(r'"sp":\s*(\d+(?:\.\d{2})?)', page_source)
            if price_match:
                price = float(price_match.group(1))
                if 10 <= price <= 10000:
                    print(f"   ✓ BigBasket (JSON): Rs {price}")
                    return price
            
            print(f"   ✗ BigBasket: No price found")
            return None
            
        except Exception as e:
            print(f"   ✗ BigBasket error: {str(e)[:60]}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def fetch_zepto_price(self, item: str) -> Optional[float]:
        """Fetch from Zepto"""
        driver = None
        try:
            print(f"   🔍 Scraping Zepto for: {item}")
            
            search_term = item.lower().replace(' ', '+')
            url = f"https://www.zeptonow.com/search?query={search_term}"
            
            driver = self._create_driver()
            driver.get(url)
            
            wait = WebDriverWait(driver, 15)
            
            # Zepto price selectors
            price_selectors = [
                "[data-testid='price']",
                "div[class*='price']",
                "span[class*='amount']"
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    text = price_elem.text.strip()
                    match = re.search(r'[₹Rs\s]*(\d+(?:\.\d{2})?)', text)
                    if match:
                        price = float(match.group(1))
                        if 10 <= price <= 10000:
                            print(f"   ✓ Zepto: Rs {price}")
                            return price
                except TimeoutException:
                    continue
            
            print(f"   ✗ Zepto: No price found")
            return None
            
        except Exception as e:
            print(f"   ✗ Zepto error: {str(e)[:60]}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def fetch_swiggy_price(self, item: str) -> Optional[float]:
        """Fetch from Swiggy Instamart"""
        driver = None
        try:
            print(f"   🔍 Scraping Swiggy for: {item}")
            
            search_term = item.lower().replace(' ', '+')
            url = f"https://www.swiggy.com/instamart/search?query={search_term}"
            
            driver = self._create_driver()
            driver.get(url)
            
            wait = WebDriverWait(driver, 15)
            
            # Swiggy price selectors
            price_selectors = [
                "span[class*='rupee']",
                "div[class*='Price']",
                "[data-testid='product-price']"
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    text = price_elem.text.strip()
                    match = re.search(r'[₹Rs\s]*(\d+(?:\.\d{2})?)', text)
                    if match:
                        price = float(match.group(1))
                        if 10 <= price <= 10000:
                            print(f"   ✓ Swiggy: Rs {price}")
                            return price
                except TimeoutException:
                    continue
            
            print(f"   ✗ Swiggy: No price found")
            return None
            
        except Exception as e:
            print(f"   ✗ Swiggy error: {str(e)[:60]}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def get_realtime_price(self, item: str) -> float:
        """
        Get real-time price for an item.
        1. Check cache
        2. Try scraping all 3 stores
        3. Average available prices
        4. Fallback to database
        """
        # Check cache first
        cached = self._get_cached_price(item)
        if cached:
            return cached
        
        # Try scraping
        print(f"\n📝 Fetching price: {item}")
        
        prices = []
        
        # Try BigBasket
        bb_price = self.fetch_bigbasket_price(item)
        if bb_price:
            prices.append(bb_price)
            time.sleep(1)  # Rate limiting
        
        # Try Zepto
        zepto_price = self.fetch_zepto_price(item)
        if zepto_price:
            prices.append(zepto_price)
            time.sleep(1)
        
        # Try Swiggy
        swiggy_price = self.fetch_swiggy_price(item)
        if swiggy_price:
            prices.append(swiggy_price)
        
        # Average if we got prices
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"   💰 Average: Rs {avg_price:.2f}")
            self._cache_price(item, avg_price)
            return avg_price
        
        # Fallback to database
        item_clean = item.lower().strip()
        fallback = self.fallback_prices.get(item_clean, 100)
        print(f"   ⚠ Using fallback: Rs {fallback}")
        return fallback


class BrightDataSeleniumCostEstimator:
    """
    Integration with MealCraft-AI.
    Estimates dish costs using real-time grocery prices via Selenium scraper.
    """
    
    def __init__(self, location: str = "Chennai"):
        self.scraper = BrightDataSeleniumScraper(location)
        self.location = location
        
    def estimate_dish_cost(self, ingredients: List[str], servings: int = 2) -> float:
        """
        Estimate cost for a dish based on ingredients.
        
        Args:
            ingredients: List of ingredient names
            servings: Number of servings
            
        Returns:
            Estimated cost in Rs
        """
        total_cost = 0
        
        for ingredient in ingredients:
            # Get price per kg/liter
            price_per_unit = self.scraper.get_realtime_price(ingredient)
            
            # Estimate quantity needed (in kg/liter)
            quantity = self._estimate_quantity(ingredient, servings)
            
            # Calculate cost
            cost = price_per_unit * quantity
            total_cost += cost
        
        return round(total_cost, 2)
    
    def _estimate_quantity(self, ingredient: str, servings: int) -> float:
        """Estimate quantity needed in kg/liter"""
        ingredient_lower = ingredient.lower()
        
        # Base quantities for 2 servings
        base_servings = 2
        multiplier = servings / base_servings
        
        # Grains: ~150g per serving
        if any(grain in ingredient_lower for grain in ['rice', 'wheat', 'flour', 'atta']):
            return (0.15 * servings)
        
        # Pulses: ~100g per serving
        if any(pulse in ingredient_lower for pulse in ['dal', 'lentil', 'rajma', 'chickpea']):
            return (0.10 * servings)
        
        # Vegetables: ~100g per serving
        if any(veg in ingredient_lower for veg in ['tomato', 'potato', 'onion', 'carrot', 'beans']):
            return (0.10 * servings)
        
        # Dairy: ~50g per serving for paneer, ~100ml for milk
        if 'paneer' in ingredient_lower or 'cheese' in ingredient_lower:
            return (0.05 * servings)
        if 'milk' in ingredient_lower or 'curd' in ingredient_lower:
            return (0.10 * servings)
        
        # Oils: ~10ml per serving
        if 'oil' in ingredient_lower or 'ghee' in ingredient_lower:
            return (0.01 * servings)
        
        # Spices: ~5g per serving
        if any(spice in ingredient_lower for spice in ['masala', 'powder', 'turmeric', 'cumin']):
            return (0.005 * servings)
        
        # Default: 50g per serving
        return (0.05 * servings)


# Test the scraper
if __name__ == "__main__":
    print("=" * 80)
    print("BRIGHT DATA + SELENIUM REAL-TIME GROCERY SCRAPER")
    print("=" * 80)
    print(f"\nLocation: Chennai")
    print("Method: Selenium with headless Chrome through Bright Data proxy")
    print("Stores: BigBasket, Zepto, Swiggy Instamart\n")
    
    print("=" * 80)
    print("TESTING WITH SAMPLE ITEMS")
    print("=" * 80)
    
    estimator = BrightDataSeleniumCostEstimator("Chennai")
    
    # Test items
    test_items = ["rice", "tomato", "onion"]
    
    for item in test_items:
        price = estimator.scraper.get_realtime_price(item)
        print(f"\n✅ Final price for {item}: Rs {price}\n")
        print("-" * 80)
    
    print("\n✅ Selenium scraper ready!")
    print("   - Uses headless Chrome for JavaScript rendering")
    print("   - Connects through Bright Data proxy")
    print("   - Handles dynamic content from React/JS apps")
