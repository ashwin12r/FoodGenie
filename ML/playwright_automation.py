"""
Advanced Browser Automation with Playwright Framework
Architecture: Automated Browser + Playwright + LLM for intelligent form filling
Similar to the architecture diagram shown
"""

import asyncio
import time
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
import re


class PlaywrightGroceryAutomation:
    """
    Advanced grocery automation using Playwright Framework
    Features:
    - Stealth mode (undetectable automation)
    - Smart element detection
    - AI-like form submission
    - BrightData-style scraping
    """
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        self.store_urls = {
            'bigbasket': 'https://www.bigbasket.com',
            'zepto': 'https://www.zeptonow.com',
            'blinkit': 'https://www.blinkit.com',
            'swiggy': 'https://www.swiggy.com/instamart',
            'amazon': 'https://www.amazon.in/alm/storefront?almBrandId=QW1hem9uIEZyZXNo',
            'jiomart': 'https://www.jiomart.com'
        }
    
    async def initialize_browser(self, headless: bool = False):
        """Initialize Playwright browser with stealth mode"""
        playwright = await async_playwright().start()
        
        # Launch browser with anti-detection
        self.browser = await playwright.chromium.launch(
            headless=headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-web-security',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--start-maximized'
            ]
        )
        
        # Create context with realistic user profile
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-IN',
            timezone_id='Asia/Kolkata',
            geolocation={'latitude': 13.0827, 'longitude': 80.2707},  # Chennai
            permissions=['geolocation']
        )
        
        # Create page and apply stealth mode manually
        self.page = await self.context.new_page()
        
        # Apply stealth scripts
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = {
                runtime: {}
            };
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)
        
        print("✅ Playwright browser initialized with stealth mode")
    
    async def close_browser(self):
        """Close browser and cleanup"""
        if self.browser:
            await self.browser.close()
            print("🔒 Browser closed")
    
    async def smart_wait(self, duration: float = 1.0):
        """Human-like wait with random variance"""
        import random
        wait_time = duration + random.uniform(-0.3, 0.5)
        await asyncio.sleep(max(0.5, wait_time))
    
    async def handle_popups(self):
        """Handle common popups and overlays"""
        try:
            # Close button patterns
            close_selectors = [
                'button:has-text("×")',
                'button:has-text("Close")',
                '[class*="close"]',
                '[aria-label="Close"]',
                '[data-dismiss="modal"]'
            ]
            
            for selector in close_selectors:
                try:
                    close_btn = await self.page.query_selector(selector)
                    if close_btn:
                        await close_btn.click()
                        await self.smart_wait(0.5)
                        print("🚫 Closed popup")
                except:
                    pass
        except:
            pass
    
    async def smart_search_and_add(self, item_name: str) -> bool:
        """
        Intelligently search for item and add to cart
        Uses LLM-like logic to find elements
        """
        try:
            print(f"🔍 Searching for: {item_name}")
            
            # Find search box using multiple strategies
            search_box = None
            search_selectors = [
                'input[placeholder*="Search"]',
                'input[placeholder*="search"]',
                'input[type="search"]',
                'input[name*="search"]',
                'input[class*="search"]',
                '[role="searchbox"]'
            ]
            
            for selector in search_selectors:
                try:
                    search_box = await self.page.wait_for_selector(selector, timeout=3000)
                    if search_box:
                        break
                except:
                    continue
            
            if not search_box:
                print(f"❌ Search box not found")
                return False
            
            # Clear and type with human-like speed
            await search_box.click()
            await self.smart_wait(0.3)
            await search_box.fill('')
            await self.smart_wait(0.2)
            
            # Type character by character
            for char in item_name:
                await search_box.type(char, delay=100)
            
            await self.smart_wait(0.5)
            await search_box.press('Enter')
            await self.smart_wait(2)
            
            # Find and click Add to Cart button
            add_button_selectors = [
                'button:has-text("Add to basket")',
                'button:has-text("ADD TO BASKET")',
                'button:has-text("Add to cart")',
                'button:has-text("ADD")',
                '[class*="add"][class*="cart"]',
                '[class*="add"][class*="basket"]'
            ]
            
            for selector in add_button_selectors:
                try:
                    # Wait for product results to load
                    await self.page.wait_for_selector(selector, timeout=5000)
                    
                    # Click first available add button
                    add_btn = await self.page.query_selector(selector)
                    if add_btn:
                        await add_btn.scroll_into_view_if_needed()
                        await self.smart_wait(0.5)
                        await add_btn.click()
                        print(f"✅ Added: {item_name}")
                        await self.smart_wait(1)
                        return True
                except:
                    continue
            
            print(f"⚠️ Add button not found for: {item_name}")
            return False
            
        except Exception as e:
            print(f"❌ Error adding {item_name}: {str(e)}")
            return False
    
    async def automate_bigbasket(self, ingredients: List[str]) -> Dict:
        """
        Automate BigBasket shopping with Playwright
        """
        try:
            await self.initialize_browser(headless=False)
            
            print("🌐 Opening BigBasket...")
            await self.page.goto(self.store_urls['bigbasket'], wait_until='networkidle')
            await self.smart_wait(2)
            
            # Handle location popup
            await self.handle_popups()
            
            results = {
                'success': True,
                'store': 'BigBasket',
                'items_added': [],
                'items_not_found': [],
                'message': 'Automation in progress...'
            }
            
            # Process each ingredient
            for ingredient in ingredients:
                success = await self.smart_search_and_add(ingredient)
                if success:
                    results['items_added'].append(ingredient)
                else:
                    results['items_not_found'].append(ingredient)
                
                await self.smart_wait(1)
            
            # Navigate to cart
            try:
                cart_selectors = [
                    'a[href*="basket"]',
                    'a[href*="cart"]',
                    '[class*="cart"]',
                    'button:has-text("Cart")'
                ]
                
                for selector in cart_selectors:
                    try:
                        cart_btn = await self.page.query_selector(selector)
                        if cart_btn:
                            await cart_btn.click()
                            await self.smart_wait(2)
                            print("🛒 Navigated to cart")
                            break
                    except:
                        continue
            except:
                pass
            
            results['message'] = f"✅ Added {len(results['items_added'])} items. Browser window open for checkout."
            
            # Keep browser open for user to checkout
            print(f"\n{'='*60}")
            print(f"✅ Automation complete!")
            print(f"✅ Added: {len(results['items_added'])} items")
            if results['items_not_found']:
                print(f"⚠️ Not found: {len(results['items_not_found'])} items")
            print(f"{'='*60}\n")
            
            # Don't close browser - let user complete checkout
            # await self.close_browser()
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error: {str(e)}'
            }
    
    async def automate_zepto(self, ingredients: List[str]) -> Dict:
        """
        Automate Zepto shopping with Playwright
        """
        try:
            await self.initialize_browser(headless=False)
            
            print("🌐 Opening Zepto...")
            await self.page.goto(self.store_urls['zepto'], wait_until='networkidle')
            await self.smart_wait(3)
            
            # Handle location
            try:
                location_input = await self.page.wait_for_selector('input[placeholder*="location"]', timeout=5000)
                if location_input:
                    await location_input.fill('Chennai')
                    await self.smart_wait(1)
                    await location_input.press('Enter')
                    await self.smart_wait(2)
            except:
                pass
            
            await self.handle_popups()
            
            results = {
                'success': True,
                'store': 'Zepto',
                'items_added': [],
                'items_not_found': []
            }
            
            for ingredient in ingredients:
                success = await self.smart_search_and_add(ingredient)
                if success:
                    results['items_added'].append(ingredient)
                else:
                    results['items_not_found'].append(ingredient)
                await self.smart_wait(1)
            
            results['message'] = f"✅ Added {len(results['items_added'])} items from Zepto"
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def automate_store(self, store_name: str, ingredients: List[str]) -> Dict:
        """
        Main automation function - routes to store-specific automation
        """
        store_name_lower = store_name.lower()
        
        try:
            if 'bigbasket' in store_name_lower:
                return await self.automate_bigbasket(ingredients)
            elif 'zepto' in store_name_lower:
                return await self.automate_zepto(ingredients)
            else:
                # Generic - just open the store
                await self.initialize_browser(headless=False)
                store_key = store_name_lower.split()[0]
                url = self.store_urls.get(store_key, self.store_urls['bigbasket'])
                await self.page.goto(url)
                
                return {
                    'success': True,
                    'message': f'Opened {store_name}. Please search and add items manually.',
                    'items_added': [],
                    'items_not_found': ingredients
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error: {str(e)}'
            }


# Global instance
automation = PlaywrightGroceryAutomation()


def automate_grocery_shopping_sync(store_name: str, ingredients: List[str]) -> Dict:
    """
    Synchronous wrapper for async automation
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(automation.automate_store(store_name, ingredients))
        return result
    finally:
        loop.close()


async def automate_grocery_shopping_async(store_name: str, ingredients: List[str]) -> Dict:
    """
    Async function for automation
    """
    return await automation.automate_store(store_name, ingredients)
