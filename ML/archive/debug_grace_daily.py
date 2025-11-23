"""
Debug Grace Daily connection issues
Test different approaches to access the website
"""

import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

# Test 1: Direct access without proxy
print("=" * 80)
print("TEST 1: Direct Access (No Proxy)")
print("=" * 80)

try:
    response = requests.get("https://gracedaily.com", timeout=10, verify=False)
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Response length: {len(response.content)} bytes")
    print(f"✓ Direct access works!")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Search page
print("\n" + "=" * 80)
print("TEST 2: Search Page (No Proxy)")
print("=" * 80)

try:
    url = "https://gracedaily.com/?s=rice&post_type=product"
    response = requests.get(url, timeout=10, verify=False)
    print(f"✓ Status: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Check for WooCommerce prices
    prices = soup.select('span.woocommerce-Price-amount')
    print(f"✓ Found {len(prices)} price elements")
    
    if prices:
        for i, price in enumerate(prices[:5]):
            print(f"  Price {i+1}: {price.get_text().strip()}")
    
    # Check for product titles
    products = soup.select('h2.woocommerce-loop-product__title')
    print(f"✓ Found {len(products)} products")
    
    if products:
        for i, prod in enumerate(products[:5]):
            print(f"  Product {i+1}: {prod.get_text().strip()}")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: With Bright Data proxy
print("\n" + "=" * 80)
print("TEST 3: With Bright Data Proxy")
print("=" * 80)

proxy_url = "http://brd-customer-hl_dde66e96-zone-webscrape:18y4rj198mpn@brd.superproxy.io:33335"
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    url = "https://gracedaily.com/?s=rice&post_type=product"
    response = requests.get(url, proxies=proxies, headers=headers, timeout=30, verify=False)
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Response length: {len(response.content)} bytes")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    prices = soup.select('span.woocommerce-Price-amount')
    print(f"✓ Found {len(prices)} price elements with proxy")
    
except Exception as e:
    print(f"✗ Error with proxy: {str(e)[:100]}")

# Test 4: Check if Grace Daily is blocking requests
print("\n" + "=" * 80)
print("TEST 4: Analyze Response Headers")
print("=" * 80)

try:
    response = requests.get("https://gracedaily.com", timeout=10, verify=False)
    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    # Check for cloudflare or other protection
    if 'cloudflare' in response.text.lower():
        print("\n⚠️  Cloudflare detected!")
    if 'captcha' in response.text.lower():
        print("\n⚠️  CAPTCHA detected!")
    
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 80)
print("RECOMMENDATIONS")
print("=" * 80)
