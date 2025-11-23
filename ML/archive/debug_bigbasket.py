"""
Debug script to see what BigBasket actually returns through Bright Data proxy
"""

import requests
from bs4 import BeautifulSoup
import re

# Bright Data proxy
proxy_url = "http://brd-customer-hl_dde66e96-zone-webscrape:18y4rj198mpn@brd.superproxy.io:33335"
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Test with a simple item
item = "rice"
url = f"https://www.bigbasket.com/ps/?q={item}"

print(f"Testing BigBasket with: {item}")
print(f"URL: {url}\n")

try:
    response = requests.get(url, proxies=proxies, headers=headers, timeout=30, verify=False)
    
    print(f"Status: {response.status_code}")
    print(f"Response length: {len(response.content)} bytes\n")
    
    # Save HTML for inspection
    with open("bigbasket_response.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("✓ Saved response to bigbasket_response.html")
    
    # Look for price patterns
    print("\n" + "=" * 80)
    print("SEARCHING FOR PRICE PATTERNS")
    print("=" * 80)
    
    patterns = [
        (r'₹\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', "Rupee symbol"),
        (r'"price":\s*(\d+(?:\.\d{2})?)', '"price":'),
        (r'"sp":\s*(\d+(?:\.\d{2})?)', '"sp": (selling price)'),
        (r'"mrp":\s*(\d+(?:\.\d{2})?)', '"mrp":'),
        (r'"discounted_price":\s*(\d+(?:\.\d{2})?)', '"discounted_price":'),
        (r'data-price="(\d+(?:\.\d{2})?)"', 'data-price attribute'),
        (r'<span[^>]*price[^>]*>.*?₹?(\d+(?:\.\d{2})?)', '<span> with price class'),
    ]
    
    for pattern, desc in patterns:
        matches = re.findall(pattern, response.text, re.IGNORECASE)
        if matches:
            print(f"\n✓ Found with {desc}:")
            print(f"  First 5 matches: {matches[:5]}")
    
    # Check for JSON-LD structured data
    soup = BeautifulSoup(response.content, 'html.parser')
    json_ld = soup.find_all('script', type='application/ld+json')
    if json_ld:
        print(f"\n✓ Found {len(json_ld)} JSON-LD scripts")
        for i, script in enumerate(json_ld[:2]):
            print(f"\nJSON-LD {i+1}:")
            print(script.string[:500] if script.string else "Empty")
    
    # Check meta tags
    meta_price = soup.find('meta', property='product:price:amount')
    if meta_price:
        print(f"\n✓ Found meta price: {meta_price.get('content')}")
    
    # Check for React data
    react_data = re.findall(r'window\.__PRELOADED_STATE__\s*=\s*({.*?});', response.text, re.DOTALL)
    if react_data:
        print(f"\n✓ Found React preloaded state")
        # Search for prices in the JSON
        price_in_json = re.findall(r'"(?:price|sp|mrp)":\s*(\d+(?:\.\d{2})?)', react_data[0])
        if price_in_json:
            print(f"  Prices in React state: {price_in_json[:10]}")
    
    print("\n" + "=" * 80)
    print("Open bigbasket_response.html to inspect the full HTML")
    print("=" * 80)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
