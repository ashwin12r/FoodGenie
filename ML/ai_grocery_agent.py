"""
Grocery Shopping AI Agent using browser-use
EXACT architecture from BDAIScraperAgent (Google Flights video)

Uses:
- browser-use: LLM-powered browser automation
- Claude/OpenAI: AI model to understand web pages
- Playwright: Browser control
"""

from browser_use import Agent, Browser
from typing import List, Dict
import os
import sys
import asyncio
from dotenv import load_dotenv

# Fix for Python 3.13+ on Windows - Playwright subprocess issue
if sys.platform == 'win32' and sys.version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()


class LangChainModelWrapper:
    """Wrapper to make langchain models compatible with browser-use"""
    def __init__(self, model, provider_name, model_name):
        self._model = model
        self.provider = provider_name
        self.model_name = model_name
        
    def __getattr__(self, name):
        # Delegate all other attributes to the wrapped model
        return getattr(self._model, name)
    
    def invoke(self, *args, **kwargs):
        return self._model.invoke(*args, **kwargs)
    
    async def ainvoke(self, *args, **kwargs):
        return await self._model.ainvoke(*args, **kwargs)


def get_ai_model():
    """Initialize AI model for browser-use with proper wrapping"""
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if api_key and api_key != "your_anthropic_api_key_here":
        print("✅ Using Claude AI model (Anthropic)")
        from langchain_anthropic import ChatAnthropic
        base_model = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0,
            anthropic_api_key=api_key
        )
        # Wrap the model to add provider attribute
        return LangChainModelWrapper(base_model, "anthropic", "claude-3-5-sonnet-20241022")
    
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key != "your_openai_api_key_here":
        print("✅ Using OpenAI GPT-4o")
        from langchain_openai import ChatOpenAI
        base_model = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            openai_api_key=api_key
        )
        return LangChainModelWrapper(base_model, "openai", "gpt-4o")
    
    raise ValueError("No valid API key found. Please set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env file")


def grocery_shopping_task(ingredients: List[str], store_name: str) -> str:
    """
    Create an AI task for grocery shopping (like flight_scrape_task)
    The AI will understand and execute this natural language task
    """
    ingredients_list = "\n    - ".join(ingredients)
    
    return f"""Search for grocery items on {store_name}.

IMPORTANT: Just demonstrate the search capability. Don't try to add items to cart.

STEPS:
1. Close any popups (location, cookies, ads)
2. For each item below, search for it:
    - {ingredients_list}
3. When done searching all items, type "DONE" to finish

That's it! Just search and show results."""


def _run_playwright_sync(ingredients: List[str]) -> Dict:
    """
    Synchronous Playwright automation - runs in separate thread to avoid asyncio issues
    """
    from playwright.sync_api import sync_playwright
    
    print("🚀 Starting browser automation (sync mode)...")
    print(f"📝 Ingredients: {', '.join(ingredients)}")
    
    try:
        print("🤖 Launching Chrome with realistic user profile...")
        
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=False,
                executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--no-sandbox'
                ]
            )
            
            # Create context with realistic settings
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='en-IN',
                timezone_id='Asia/Kolkata',
                permissions=['geolocation'],
                geolocation={'latitude': 12.9716, 'longitude': 77.5946},
            )
            
            # Hide webdriver
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            page = context.new_page()
            
            # Navigate to BigBasket
            print("🌐 Opening BigBasket...")
            page.goto("https://www.bigbasket.com/", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            
            found_ingredients = []
            not_found = []
            
            for idx, ingredient in enumerate(ingredients, 1):
                print(f"� Searching for ingredient {idx}/{len(ingredients)}: {ingredient}")
                
                try:
                    # Find search box and search
                    search_box = page.locator('input[placeholder*="Search"], input[type="search"], input[qa="searchBar"]').first
                    search_box.click(force=True, timeout=5000)
                    search_box.fill("")
                    search_box.fill(ingredient)
                    page.wait_for_timeout(1000)
                    search_box.press("Enter")
                    page.wait_for_timeout(3000)
                    
                    # Check for results
                    no_results = page.locator('text=/no.*results|not.*found/i').count() > 0
                    has_products = page.locator('[class*="product"], [class*="Product"], [data-testid*="product"]').count() > 0
                    
                    if has_products and not no_results:
                        found_ingredients.append(ingredient)
                        print(f"  ✅ Found: {ingredient}")
                    else:
                        not_found.append(ingredient)
                        print(f"  ❌ Not found: {ingredient}")
                        
                except Exception as e:
                    print(f"  ⚠️ Error searching {ingredient}: {str(e)}")
                    not_found.append(ingredient)
            
            print(f"\n📊 Search complete: Found {len(found_ingredients)}/{len(ingredients)} ingredients")
            print("✅ Browser will stay open for manual review")
            
            # Keep browser open
            page.wait_for_timeout(60000)
            
            browser.close()
            
            return {
                'success': True,
                'found': found_ingredients,
                'not_found': not_found,
                'total': len(ingredients),
                'message': f"Found {len(found_ingredients)}/{len(ingredients)} ingredients"
            }
            
    except Exception as e:
        print(f"❌ Sync Playwright error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'message': f'Browser automation failed: {str(e)}'
        }


async def automate_bigbasket_shopping(ingredients: List[str]) -> Dict:
    """
    Full automation: Opens BigBasket and searches for ingredients
    Uses synchronous Playwright in thread pool to avoid Windows asyncio subprocess issues
    """
    try:
        print("🚀 Starting full browser automation...")
        print(f"📝 Ingredients: {', '.join(ingredients)}")
        
        # Run synchronous Playwright in executor to avoid asyncio subprocess issues
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = await loop.run_in_executor(executor, _run_playwright_sync, ingredients)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'message': f'AI Agent encountered an error: {str(e)}'
        }





async def automate_zepto_shopping(ingredients: List[str]) -> Dict:
    """
    Zepto automation using AI Agent
    """
    try:
        # Initialize AI model
        model = get_ai_model()
        
        browser = Browser(
            executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            headless=False
        )
        
        agent = Agent(
            task=f"Go to https://www.zeptonow.com and then: {grocery_shopping_task(ingredients, 'Zepto')}",
            llm=model,
            browser=browser,
        )
        
        history = await agent.run()
        result = history.final_result()
        
        return {
            "success": True,
            "result": result,
            "message": "AI shopping completed"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def automate_grocery_shopping_ai(store_name: str, ingredients: List[str]) -> Dict:
    """
    Main entry point - routes to appropriate store automation
    EXACTLY like scrape_flights() in their code
    """
    store_name_lower = store_name.lower()
    
    if 'bigbasket' in store_name_lower:
        return await automate_bigbasket_shopping(ingredients)
    elif 'zepto' in store_name_lower:
        return await automate_zepto_shopping(ingredients)
    else:
        # Generic fallback
        return await automate_bigbasket_shopping(ingredients)
