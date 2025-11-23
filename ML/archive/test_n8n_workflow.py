"""
Test n8n workflow - Simple version without emojis
"""
import requests
import json

webhook_url = "http://horace-biforate-cinthia.ngrok-free.dev/webhook/grocery-prices"

payload = {
    "items": ["rice", "dal", "tomato"],
    "location": "Chennai"
}

print("Testing n8n Grocery Price Scraper")
print("=" * 60)
print(f"URL: {webhook_url}")
print(f"Items: {payload['items']}")
print("\nSending request (may take 30-60 seconds)...")

try:
    response = requests.post(webhook_url, json=payload, timeout=120)
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        print("SUCCESS! Workflow executed.")
        result = response.json()
        print("\n" + "=" * 60)
        print("RESULTS:")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        
        if 'prices' in result:
            print("\nPrices Found:")
            for item, price in result['prices'].items():
                print(f"  {item}: Rs {price}")
                
        if 'stats' in result:
            stats = result['stats']
            print(f"\nSuccess Rate: {stats['success']}/{stats['total']}")
    else:
        print(f"ERROR: Status {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"ERROR: {e}")
