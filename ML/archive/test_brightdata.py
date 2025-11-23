"""
Test Bright Data Proxy Connection
Verifies that your proxy credentials work correctly
"""

import urllib.request
import ssl

# Your Bright Data credentials
proxy = 'http://brd-customer-hl_dde66e96-zone-webscrape:18y4rj198mpn@brd.superproxy.io:33335'

print("="*60)
print("🔍 Testing Bright Data Proxy Connection")
print("="*60)

# Test 1: Basic connectivity test
print("\n[Test 1] Basic Proxy Test...")
url = 'https://geo.brdtest.com/welcome.txt?product=resi&method=native'

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({'https': proxy, 'http': proxy}),
    urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
)

try:
    response = opener.open(url).read().decode()
    print("✅ Proxy connection successful!")
    print(f"Response: {response[:200]}...")
except Exception as e:
    print(f"❌ Proxy connection failed: {e}")
    exit(1)

# Test 2: Test with actual BigBasket
print("\n[Test 2] Testing BigBasket Access...")
bigbasket_url = 'https://www.bigbasket.com/ps/?q=rice'

try:
    response = opener.open(bigbasket_url, timeout=10)
    content = response.read().decode('utf-8', errors='ignore')
    print(f"✅ BigBasket accessible via proxy!")
    print(f"   Status: {response.status}")
    print(f"   Content length: {len(content)} bytes")
    
    # Check if we bypassed Cloudflare
    if "cloudflare" in content.lower():
        print("⚠️  Warning: Still seeing Cloudflare protection")
    else:
        print("✅ Cloudflare bypassed successfully!")
        
except Exception as e:
    print(f"❌ BigBasket access failed: {e}")

# Test 3: Check IP location
print("\n[Test 3] Checking Proxy IP Location...")
ip_check_url = 'https://ipinfo.io/json'

try:
    response = opener.open(ip_check_url)
    ip_info = response.read().decode()
    print("✅ IP Info:")
    print(ip_info)
except Exception as e:
    print(f"❌ IP check failed: {e}")

print("\n" + "="*60)
print("✅ Bright Data Proxy Tests Complete!")
print("="*60)
print("\n📋 Your Proxy Details:")
print(f"   Username: brd-customer-hl_dde66e96-zone-webscrape")
print(f"   Password: 18y4rj198mpn")
print(f"   Host: brd.superproxy.io")
print(f"   Port: 33335")
print("\n🚀 Ready to use in n8n workflow!")
