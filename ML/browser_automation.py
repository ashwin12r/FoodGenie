"""
Browser Automation for AI Shopping Assistant
Uses Selenium to automate grocery shopping on various platforms
"""

import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class GroceryAutomation:
    """Automate grocery shopping across different platforms"""
    
    def __init__(self):
        self.driver = None
        self.store_urls = {
            'bigbasket': 'https://www.bigbasket.com',
            'zepto': 'https://www.zeptonow.com',
            'blinkit': 'https://www.blinkit.com',
            'swiggy': 'https://www.swiggy.com/instamart',
            'amazon': 'https://www.amazon.in/alm/storefront?almBrandId=QW1hem9uIEZyZXNo',
            'jiomart': 'https://www.jiomart.com'
        }
    
    def setup_driver(self):
        """Initialize Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def close_driver(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def search_and_add_to_cart_bigbasket(self, ingredients: List[str]) -> Dict:
        """
        Automate BigBasket shopping
        """
        try:
            if not self.driver:
                self.setup_driver()
            
            # Open BigBasket
            self.driver.get(self.store_urls['bigbasket'])
            time.sleep(3)
            
            results = {
                'success': True,
                'store': 'BigBasket',
                'items_added': [],
                'items_not_found': [],
                'message': 'Starting to add items to cart...'
            }
            
            # Handle location popup if exists
            try:
                location_close = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='close']"))
                )
                location_close.click()
                time.sleep(1)
            except:
                pass
            
            for ingredient in ingredients:
                try:
                    # Find search box
                    search_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Search']"))
                    )
                    
                    # Clear and search for ingredient
                    search_box.clear()
                    search_box.send_keys(ingredient)
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(2)
                    
                    # Try to find and click "Add to Basket" button
                    try:
                        add_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to basket') or contains(text(), 'ADD')]"))
                        )
                        add_button.click()
                        results['items_added'].append(ingredient)
                        time.sleep(1)
                        print(f"✅ Added: {ingredient}")
                    except:
                        results['items_not_found'].append(ingredient)
                        print(f"❌ Not found: {ingredient}")
                    
                except Exception as e:
                    print(f"Error processing {ingredient}: {str(e)}")
                    results['items_not_found'].append(ingredient)
            
            # Go to cart
            try:
                cart_button = self.driver.find_element(By.CSS_SELECTOR, "a[href*='basket']")
                cart_button.click()
                time.sleep(2)
            except:
                pass
            
            results['message'] = f"Added {len(results['items_added'])} items to cart. Please review and checkout."
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error automating BigBasket: {str(e)}'
            }
    
    def search_and_add_to_cart_zepto(self, ingredients: List[str]) -> Dict:
        """
        Automate Zepto shopping
        """
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(self.store_urls['zepto'])
            time.sleep(3)
            
            results = {
                'success': True,
                'store': 'Zepto',
                'items_added': [],
                'items_not_found': [],
                'message': 'Starting to add items to cart...'
            }
            
            # Handle location popup
            try:
                location_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Enter']"))
                )
                location_input.send_keys("Chennai")
                time.sleep(1)
                location_input.send_keys(Keys.RETURN)
                time.sleep(2)
            except:
                pass
            
            for ingredient in ingredients:
                try:
                    # Find search
                    search_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
                    )
                    search_box.clear()
                    search_box.send_keys(ingredient)
                    time.sleep(2)
                    
                    # Click first product's add button
                    try:
                        add_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ADD')]"))
                        )
                        add_button.click()
                        results['items_added'].append(ingredient)
                        time.sleep(1)
                    except:
                        results['items_not_found'].append(ingredient)
                except:
                    results['items_not_found'].append(ingredient)
            
            results['message'] = f"Added {len(results['items_added'])} items. Please proceed to checkout."
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def automate_store(self, store_name: str, ingredients: List[str]) -> Dict:
        """
        Main function to automate shopping based on store
        """
        store_name = store_name.lower()
        
        if 'bigbasket' in store_name:
            return self.search_and_add_to_cart_bigbasket(ingredients)
        elif 'zepto' in store_name:
            return self.search_and_add_to_cart_zepto(ingredients)
        else:
            # Generic approach - just open the website
            try:
                if not self.driver:
                    self.setup_driver()
                
                store_key = store_name.split()[0].lower()
                url = self.store_urls.get(store_key, self.store_urls['bigbasket'])
                self.driver.get(url)
                
                return {
                    'success': True,
                    'message': f'Opened {store_name}. Please manually search and add items.',
                    'items_added': [],
                    'items_not_found': ingredients
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e)
                }


# Global instance
automation = GroceryAutomation()


def automate_grocery_shopping(store_name: str, ingredients: List[str]) -> Dict:
    """
    Wrapper function to automate grocery shopping
    """
    result = automation.automate_store(store_name, ingredients)
    return result


def cleanup_automation():
    """Clean up automation resources"""
    automation.close_driver()
