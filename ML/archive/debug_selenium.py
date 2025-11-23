"""
Debug Selenium scraping - check what's actually loaded
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_grace_daily_selenium():
    print("\n" + "="*80)
    print("TESTING GRACE DAILY WITH SELENIUM")
    print("="*80)
    
    chrome_options = Options()
    # Uncomment to see browser (not headless)
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Try home page first
        url = "https://gracedaily.com/"
        print(f"\n1. Loading home page: {url}")
        driver.get(url)
        time.sleep(5)  # Wait for React to render
        
        # Save screenshot
        driver.save_screenshot('grace_daily_home.png')
        print("   ✓ Screenshot saved: grace_daily_home.png")
        
        # Save page source
        with open('grace_daily_selenium.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source[:10000])
        print("   ✓ Page source saved: grace_daily_selenium.html")
        
        # Look for search box
        search_inputs = driver.find_elements(By.TAG_NAME, 'input')
        print(f"\n   Found {len(search_inputs)} input elements")
        
        # Look for product links
        links = driver.find_elements(By.TAG_NAME, 'a')
        product_links = [link.get_attribute('href') for link in links if link.get_attribute('href') and 'product' in link.get_attribute('href').lower()][:5]
        print(f"   Found {len(product_links)} product links:")
        for link in product_links[:5]:
            print(f"      → {link}")
        
        # Try a direct product URL if we found one
        if product_links:
            print(f"\n2. Loading product page: {product_links[0]}")
            driver.get(product_links[0])
            time.sleep(5)
            
            driver.save_screenshot('grace_daily_product.png')
            print("   ✓ Screenshot saved: grace_daily_product.png")
            
            # Look for price
            page_text = driver.page_source
            if '₹' in page_text or 'Rs' in page_text:
                print("   ✓ Found currency symbols in page!")
                import re
                prices = re.findall(r'[₹Rs\.]+[\s]*(\d+(?:,\d{3})*(?:\.\d{2})?)', page_text)
                print(f"   Found {len(prices)} price patterns: {prices[:10]}")
            else:
                print("   ✗ No currency symbols found")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        input("\nPress Enter to close browser...")
        driver.quit()

def test_kpn_fresh_selenium():
    print("\n" + "="*80)
    print("TESTING KPN FRESH WITH SELENIUM")
    print("="*80)
    
    chrome_options = Options()
    # Uncomment to see browser (not headless)
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Try home page
        url = "https://www.kpnfresh.com/"
        print(f"\n1. Loading home page: {url}")
        driver.get(url)
        time.sleep(5)  # Wait for Next.js to render
        
        # Save screenshot
        driver.save_screenshot('kpn_fresh_home.png')
        print("   ✓ Screenshot saved: kpn_fresh_home.png")
        
        # Save page source
        with open('kpn_fresh_selenium.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source[:10000])
        print("   ✓ Page source saved: kpn_fresh_selenium.html")
        
        # Look for search box
        search_inputs = driver.find_elements(By.TAG_NAME, 'input')
        print(f"\n   Found {len(search_inputs)} input elements")
        
        # Look for product links
        links = driver.find_elements(By.TAG_NAME, 'a')
        product_links = [link.get_attribute('href') for link in links if link.get_attribute('href') and 'product' in link.get_attribute('href').lower()][:5]
        print(f"   Found {len(product_links)} product links:")
        for link in product_links[:5]:
            print(f"      → {link}")
        
        # Try a direct product URL if we found one
        if product_links:
            print(f"\n2. Loading product page: {product_links[0]}")
            driver.get(product_links[0])
            time.sleep(5)
            
            driver.save_screenshot('kpn_fresh_product.png')
            print("   ✓ Screenshot saved: kpn_fresh_product.png")
            
            # Look for price
            page_text = driver.page_source
            if '₹' in page_text or 'Rs' in page_text:
                print("   ✓ Found currency symbols in page!")
                import re
                prices = re.findall(r'[₹Rs\.]+[\s]*(\d+(?:,\d{3})*(?:\.\d{2})?)', page_text)
                print(f"   Found {len(prices)} price patterns: {prices[:10]}")
            else:
                print("   ✗ No currency symbols found")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        input("\nPress Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    print("\nThis will open browser windows to debug what Selenium sees...")
    print("Screenshots and HTML will be saved for analysis.")
    
    choice = input("\nTest which store? (1=Grace Daily, 2=KPN Fresh, 3=Both): ")
    
    if choice in ['1', '3']:
        test_grace_daily_selenium()
    
    if choice in ['2', '3']:
        test_kpn_fresh_selenium()
    
    print("\n✅ Debug complete! Check the screenshots and HTML files.")
