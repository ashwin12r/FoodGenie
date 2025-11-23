"""
Debug Grace Daily vegetables page to see actual HTML structure
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=chrome_options)

try:
    url = "https://gracedaily.com/ct/vegetables"
    print(f"Loading: {url}")
    
    driver.get(url)
    print("Waiting 5 seconds for React to render...")
    time.sleep(5)
    
    # Save full page source
    html = driver.page_source
    
    with open('grace_vegetables_full.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✓ Saved full HTML ({len(html)} chars) to grace_vegetables_full.html")
    
    # Check if prices are visible
    if '₹' in html:
        print(f"✓ Found ₹ symbol in page!")
        import re
        prices = re.findall(r'₹\s*(\d+(?:\.\d{2})?)', html)
        print(f"✓ Found {len(prices)} prices: {prices[:10]}")
    else:
        print("✗ No ₹ symbol found in rendered HTML")
    
    # Check if product names are visible
    if 'tomato' in html.lower():
        print("✓ Found 'tomato' in page")
    else:
        print("✗ No 'tomato' found")
    
    if 'ginger' in html.lower():
        print("✓ Found 'ginger' in page")
    else:
        print("✗ No 'ginger' found")
    
    # Look for common HTML patterns
    print("\nSearching for common element patterns:")
    
    patterns = [
        ('div class="product', 'Product divs'),
        ('class="price', 'Price classes'),
        ('<span', 'Span elements'),
        ('data-price', 'Data-price attributes'),
        ('"name":', 'JSON name fields'),
        ('"price":', 'JSON price fields'),
    ]
    
    for pattern, desc in patterns:
        count = html.lower().count(pattern.lower())
        print(f"   {desc}: {count} occurrences")
    
finally:
    driver.quit()
    print("\n✓ Done! Check grace_vegetables_full.html for full content")
