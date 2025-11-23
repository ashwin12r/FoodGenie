"""
Test to see what HTML is actually returned from the stores
"""
import requests
from bs4 import BeautifulSoup

def test_grace_daily():
    print("\n" + "="*80)
    print("TESTING GRACE DAILY")
    print("="*80)
    
    # Test product page directly
    url = "https://gracedaily.com/product/tomato/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        print(f"\n✓ Status: {response.status_code}")
        print(f"✓ Response length: {len(response.text)} chars")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for price elements
        print("\n🔍 Looking for price elements:")
        
        price_selectors = [
            'span.woocommerce-Price-amount bdi',
            'span.woocommerce-Price-amount',
            'span.amount bdi',
            'span.amount',
            'p.price',
            '.price'
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"   ✓ {selector}: Found {len(elements)} elements")
                for elem in elements[:3]:
                    print(f"      → {elem.get_text().strip()}")
        
        # Look for product info
        print("\n🔍 Looking for product structure:")
        products = soup.select('.product')
        print(f"   Products: {len(products)}")
        
        woo_products = soup.select('.woocommerce-product')
        print(f"   WooCommerce products: {len(woo_products)}")
        
        # Check if it's using React/Vue
        if 'wp-json' in response.text or 'application/json' in response.text:
            print("\n⚠️  Site might be using REST API / JavaScript")
        
        # Save a snippet
        with open('grace_daily_sample.html', 'w', encoding='utf-8') as f:
            f.write(response.text[:5000])
        print("\n💾 Saved first 5000 chars to grace_daily_sample.html")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")

def test_kpn_fresh():
    print("\n" + "="*80)
    print("TESTING KPN FRESH")
    print("="*80)
    
    # Test product page directly
    url = "https://www.kpnfresh.com/product/tomato/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        print(f"\n✓ Status: {response.status_code}")
        print(f"✓ Response length: {len(response.text)} chars")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for price elements
        print("\n🔍 Looking for price elements:")
        
        price_selectors = [
            'span.woocommerce-Price-amount bdi',
            'span.woocommerce-Price-amount',
            'span.amount bdi',
            'span.amount',
            'p.price',
            '.price'
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"   ✓ {selector}: Found {len(elements)} elements")
                for elem in elements[:3]:
                    print(f"      → {elem.get_text().strip()}")
        
        # Look for product info
        print("\n🔍 Looking for product structure:")
        products = soup.select('.product')
        print(f"   Products: {len(products)}")
        
        woo_products = soup.select('.woocommerce-product')
        print(f"   WooCommerce products: {len(woo_products)}")
        
        # Check if it's using React/Vue
        if 'wp-json' in response.text or 'application/json' in response.text:
            print("\n⚠️  Site might be using REST API / JavaScript")
        
        # Save a snippet
        with open('kpn_fresh_sample.html', 'w', encoding='utf-8') as f:
            f.write(response.text[:5000])
        print("\n💾 Saved first 5000 chars to kpn_fresh_sample.html")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    
    test_grace_daily()
    test_kpn_fresh()
