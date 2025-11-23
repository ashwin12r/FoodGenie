"""
Real-Time Grocery Price Scraper for Chennai Local Stores
Uses Selenium for JavaScript-rendered sites (React/Next.js)
Grace Daily (React SPA) & KPN Fresh (Next.js)
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import re
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ChennaiSeleniumScraper:
    """
    Selenium-based scraper for Chennai grocery stores
    Handles JavaScript-rendered React and Next.js sites
    """
    
    def __init__(self, location: str = "Chennai"):
        self.location = location
        self.cache_file = "chennai_selenium_cache.json"
        self.cache_duration = timedelta(hours=1)
        self.cache = self._load_cache()
        
        # Setup Selenium WebDriver
        self.driver = None
        self._setup_selenium()
        
        # Fallback prices database (Rs per kg/liter)
        self.fallback_prices = self._build_fallback_database()
        
        # Grace Daily product name mappings (they use different names)
        self.grace_name_map = {
            'tomato': ['tomato nadu', 'tomato', 'tomatoes'],
            'ginger': ['ginger', 'inji'],
            'broad beans': ['broad beans', 'avarai', 'beans'],
            'coconut': ['coconut', 'thengai'],
            'banana': ['banana', 'raw banana', 'plantain'],
            'onion': ['onion', 'vengayam', 'small onion'],
            'brinjal': ['brinjal', 'eggplant', 'kathirikkai'],
            'carrot': ['carrot', 'carrot nadu'],
            'potato': ['potato', 'urulaikizhangu'],
            'drumstick': ['drumstick', 'murungakkai'],
            'curry leaves': ['curry leaves', 'karuveppilai'],
            'coriander': ['coriander', 'kothamalli'],
            'mint': ['mint', 'pudina'],
            'beetroot': ['beetroot', 'beet'],
            'cabbage': ['cabbage', 'muttaikose'],
            'cauliflower': ['cauliflower', 'gobi'],
            'capsicum': ['capsicum', 'bell pepper'],
            'chili': ['chili', 'green chilli', 'milagai'],
            'garlic': ['garlic', 'poondu'],
            'ladies finger': ['ladies finger', 'okra', 'vendakkai'],
            'radish': ['radish', 'mullangi'],
            'spinach': ['spinach', 'keerai'],
        }
        
        print("=" * 80)
        print("CHENNAI SELENIUM GROCERY SCRAPER")
        print("=" * 80)
        print(f"Location: {self.location}")
        print("Stores: Grace Daily (React) & KPN Fresh (Next.js)")
        print("Method: Selenium Chrome (JavaScript rendering)")
        print("=" * 80 + "\n")
    
    def _setup_selenium(self):
        """Setup Selenium WebDriver with Chrome"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✓ Selenium Chrome driver initialized")
        except Exception as e:
            print(f"✗ Selenium setup failed: {e}")
            print("   Will use fallback database only")
            self.driver = None
    
    def __del__(self):
        """Cleanup: Close Selenium driver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
    
    def _load_cache(self) -> Dict:
        """Load price cache from file"""
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
                return cache
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def _save_cache(self):
        """Save price cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"⚠️  Cache save failed: {e}")
    
    def _build_fallback_database(self) -> Dict[str, float]:
        """Comprehensive fallback price database for Chennai"""
        return {
            # Grains & Staples (per kg)
            'rice': 60, 'basmati rice': 120, 'brown rice': 100,
            'wheat': 40, 'atta': 40, 'maida': 45, 'rava': 50, 'sooji': 50,
            'poha': 80, 'vermicelli': 70, 'noodles': 90,
            
            # Pulses/Dals (per kg)
            'toor dal': 110, 'moong dal': 120, 'chana dal': 100,
            'urad dal': 130, 'masoor dal': 100, 'arhar dal': 110,
            'split peas': 100, 'chickpeas': 80, 'rajma': 150,
            'black gram': 130, 'green gram': 120,
            
            # Vegetables (per kg)
            'tomato': 50, 'onion': 40, 'potato': 30, 'carrot': 45,
            'cabbage': 35, 'cauliflower': 50, 'beans': 60, 'peas': 80,
            'brinjal': 40, 'eggplant': 40, 'okra': 50, 'ladyfinger': 50,
            'drumstick': 80, 'bitter gourd': 60, 'bottle gourd': 40,
            'ridge gourd': 50, 'snake gourd': 45, 'ash gourd': 30,
            'pumpkin': 35, 'cucumber': 35, 'bell pepper': 80, 'capsicum': 80,
            'green chili': 100, 'ginger': 150, 'garlic': 120,
            'beetroot': 45, 'radish': 40, 'spinach': 50, 'coriander': 50,
            'mint': 60, 'curry leaves': 20, 'plantain': 40, 'banana': 50,
            
            # Dairy (per liter/kg)
            'milk': 60, 'curd': 50, 'yogurt': 50, 'paneer': 350,
            'butter': 450, 'ghee': 500, 'cheese': 400, 'cream': 300,
            
            # Oils & Fats (per liter/kg)
            'sunflower oil': 150, 'groundnut oil': 180, 'coconut oil': 200,
            'sesame oil': 250, 'mustard oil': 160, 'olive oil': 400,
            'oil': 150,
            
            # Spices (per kg or 100g)
            'turmeric': 200, 'turmeric powder': 200, 'red chili': 180,
            'chili powder': 180, 'coriander powder': 150, 'cumin': 300,
            'mustard seeds': 200, 'fenugreek': 150, 'fennel': 250,
            'cardamom': 2000, 'cloves': 1500, 'cinnamon': 500,
            'black pepper': 600, 'bay leaf': 300, 'star anise': 400,
            'asafoetida': 800, 'hing': 800,
            
            # Powders & Masalas (per 100g)
            'sambar powder': 80, 'rasam powder': 70, 'garam masala': 100,
            'chat masala': 80, 'biryani masala': 90, 'curry powder': 85,
            
            # Dry Fruits & Nuts (per kg)
            'cashew': 800, 'almonds': 900, 'raisins': 350, 'dates': 400,
            'walnuts': 1000, 'pistachios': 1200,
            
            # Other Essentials
            'salt': 20, 'sugar': 45, 'jaggery': 80, 'tamarind': 150,
            'coconut': 40, 'coconut milk': 100, 'besan': 80,
            'gram flour': 80, 'cornflour': 90, 'tea': 400, 'coffee': 500,
        }
    
    def fetch_grace_daily_price(self, item: str) -> Optional[float]:
        """
        Fetch price from Grace Daily (gracedaily.com) - React SPA
        Uses category pages and name mapping for fuzzy matching
        """
        if not self.driver:
            return None
        
        try:
            print(f"   🔍 Grace Daily (Selenium): {item}...")
            
            # Get alternative names for this item
            item_lower = item.lower()
            search_terms = [item_lower]
            
            # Add mapped names if available
            for key, values in self.grace_name_map.items():
                if key in item_lower or item_lower in key:
                    search_terms.extend(values)
                    break
            
            # Determine category based on item type
            category_url = "https://gracedaily.com/ct/vegetables"  # Default to vegetables
            
            if any(word in item_lower for word in ['rice', 'dal', 'wheat', 'atta', 'rava', 'grain', 'flour']):
                category_url = "https://gracedaily.com/ct/foodgrains-oil-masalas"
            elif any(word in item_lower for word in ['milk', 'curd', 'paneer', 'butter', 'ghee', 'bread', 'dairy']):
                category_url = "https://gracedaily.com/ct/bakery-dairy"
            elif any(word in item_lower for word in ['powder', 'masala', 'spice', 'oil', 'salt', 'sugar']):
                category_url = "https://gracedaily.com/ct/foodgrains-oil-masalas"
            
            self.driver.get(category_url)
            time.sleep(4)  # Wait for React to render products
            
            # Get rendered HTML
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            page_text = soup.get_text().lower()
            
            # Try to find matching products with prices
            for search_term in search_terms:
                # Look for the search term followed by price within reasonable distance
                pattern = re.escape(search_term[:15])  # First 15 chars to avoid too specific
                
                matches = list(re.finditer(pattern, page_text))
                for match in matches:
                    # Get context around the match (300 chars)
                    start = max(0, match.start() - 100)
                    end = min(len(page_text), match.start() + 300)
                    context = page_text[start:end]
                    
                    # Find price in context using ₹ symbol
                    price_matches = re.findall(r'₹\s*(\d+(?:\.\d{2})?)', context)
                    
                    for price_str in price_matches:
                        try:
                            price = float(price_str)
                            if 10 <= price <= 10000:  # Reasonable price range
                                print(f"   ✓ Grace Daily: Rs {price:.2f} (matched: {search_term})")
                                return price
                        except:
                            continue
            
            print(f"   ✗ Grace Daily: No price found in {category_url.split('/')[-1]}")
            return None
            
        except Exception as e:
            print(f"   ✗ Grace Daily error: {str(e)[:60]}")
            return None
    
    def fetch_kpn_fresh_price(self, item: str) -> Optional[float]:
        """
        Fetch price from KPN Fresh (kpnfresh.com) - Next.js
        Uses Selenium to render JavaScript
        """
        if not self.driver:
            return None
        
        try:
            search_term = item.lower().replace(' ', '%20')
            url = f"https://www.kpnfresh.com/search?query={search_term}"
            
            print(f"   🔍 KPN Fresh (Selenium): {item}...")
            
            self.driver.get(url)
            
            # Wait for Next.js to render
            time.sleep(3)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                print(f"   ✗ KPN Fresh: Timeout")
                return None
            
            # Get rendered HTML
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Look for price patterns
            price_patterns = [
                r'₹[\s]*(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'Rs\.?[\s]*(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'INR[\s]*(\d+(?:,\d{3})*(?:\.\d{2})?)'
            ]
            
            prices = []
            for pattern in price_patterns:
                matches = re.findall(pattern, soup.get_text())
                for match in matches:
                    try:
                        price = float(match.replace(',', ''))
                        if 10 <= price <= 10000:
                            prices.append(price)
                    except:
                        continue
            
            if prices:
                prices.sort()
                median_price = prices[len(prices) // 2]
                print(f"   ✓ KPN Fresh: Rs {median_price:.2f}")
                return median_price
            
            print(f"   ✗ KPN Fresh: No price found")
            return None
            
        except Exception as e:
            print(f"   ✗ KPN Fresh error: {str(e)[:60]}")
            return None
    
    def get_realtime_price(self, item: str) -> float:
        """
        Get real-time price from Chennai stores with caching
        Returns average if multiple stores have prices
        Falls back to database if scraping fails
        """
        # Check cache first
        cache_key = f"{item.lower()}_{self.location.lower()}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            cache_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - cache_time < self.cache_duration:
                print(f"   💾 Using cached price: Rs {cached_data['price']}")
                return cached_data['price']
        
        # Try to fetch real-time prices
        prices = []
        
        grace_price = self.fetch_grace_daily_price(item)
        if grace_price:
            prices.append(grace_price)
        
        kpn_price = self.fetch_kpn_fresh_price(item)
        if kpn_price:
            prices.append(kpn_price)
        
        if prices:
            avg_price = sum(prices) / len(prices)
            
            # Cache the result
            self.cache[cache_key] = {
                'price': avg_price,
                'timestamp': datetime.now().isoformat(),
                'sources': len(prices)
            }
            self._save_cache()
            
            return avg_price
        
        # Fallback to database
        item_lower = item.lower()
        if item_lower in self.fallback_prices:
            fallback_price = self.fallback_prices[item_lower]
            print(f"   ⚠ Using fallback database: Rs {fallback_price}")
            return fallback_price
        
        # Try fuzzy matching
        for key in self.fallback_prices:
            if item_lower in key or key in item_lower:
                fallback_price = self.fallback_prices[key]
                print(f"   ⚠ Using fallback (fuzzy match '{key}'): Rs {fallback_price}")
                return fallback_price
        
        # Default fallback
        print(f"   ⚠ Item not found, using default: Rs 100")
        return 100.0
    
    def estimate_dish_cost(self, ingredients, servings: int = 2) -> float:
        """
        Estimate cost of a dish based on its ingredients
        """
        # Handle both string (comma-separated) and list inputs
        if isinstance(ingredients, str):
            ingredient_list = [ing.strip() for ing in ingredients.split(',') if ing.strip()]
        else:
            ingredient_list = ingredients
        
        total_cost = 0
        
        for ingredient in ingredient_list[:7]:  # Limit to first 7 main ingredients
            if not ingredient or len(ingredient) < 2:
                continue
            
            print(f"\n📝 Fetching real-time price: {ingredient}")
            price_per_kg = self.get_realtime_price(ingredient)
            
            # Estimate quantity needed (in kg) for 2 servings
            estimated_qty = 0.1  # Default 100g
            
            # Adjust based on ingredient type
            if any(word in ingredient.lower() for word in ['rice', 'dal', 'wheat', 'atta']):
                estimated_qty = 0.15  # 150g for staples
            elif any(word in ingredient.lower() for word in ['oil', 'ghee', 'butter']):
                estimated_qty = 0.02  # 20ml for oils
            elif any(word in ingredient.lower() for word in ['spice', 'masala', 'powder', 'salt', 'turmeric', 'chili']):
                estimated_qty = 0.01  # 10g for spices
            elif any(word in ingredient.lower() for word in ['vegetable', 'tomato', 'onion', 'potato']):
                estimated_qty = 0.12  # 120g for vegetables
            
            ingredient_cost = price_per_kg * estimated_qty
            total_cost += ingredient_cost
        
        # Scale for servings
        total_cost = (total_cost / 2) * servings
        
        return round(total_cost, 2)


class ChennaiCostEstimator:
    """
    Wrapper class for MealCraft-AI integration
    """
    
    def __init__(self, location: str = "Chennai"):
        self.scraper = ChennaiSeleniumScraper(location)
    
    def estimate_dish_cost(self, ingredients, servings: int = 2) -> float:
        """
        Estimate cost of a dish based on its ingredients
        """
        return self.scraper.estimate_dish_cost(ingredients, servings)
    
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'scraper'):
            del self.scraper


# Test the scraper
if __name__ == "__main__":
    print("\n" + "="*80)
    print("TESTING CHENNAI SELENIUM SCRAPER")
    print("="*80 + "\n")
    
    scraper = ChennaiSeleniumScraper()
    
    # Test with sample dishes
    test_dishes = [
        {
            'name': 'Sambar',
            'ingredients': 'toor dal, tomato, drumstick, tamarind, sambar powder, curry leaves, oil'
        },
        {
            'name': 'Curd Rice',
            'ingredients': 'rice, curd, cucumber, curry leaves, mustard seeds, oil'
        },
        {
            'name': 'Rasam',
            'ingredients': 'toor dal, tomato, tamarind, rasam powder, curry leaves, garlic'
        }
    ]
    
    print("\n" + "="*80)
    print("ESTIMATING COSTS FOR SAMPLE DISHES")
    print("="*80 + "\n")
    
    for dish in test_dishes:
        print(f"📝 {dish['name']}")
        print(f"   Ingredients: {dish['ingredients']}")
        
        cost = scraper.estimate_dish_cost(dish['ingredients'], servings=2)
        print(f"   💰 Total Cost: Rs {cost} (for 2 servings)")
        print("-" * 80 + "\n")
    
    print("✅ Chennai Selenium scraper ready!")
    print("   - Uses Selenium for JavaScript rendering")
    print("   - Scrapes Grace Daily (React SPA)")
    print("   - Scrapes KPN Fresh (Next.js)")
    print("   - 1-hour cache for efficiency")
    print("   - Comprehensive fallback database")
