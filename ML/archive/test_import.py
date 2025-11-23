"""Test that real-time pricing module loads correctly"""
import sys

print("Testing import...")
try:
    from grocery_price_scraper import RealTimeCostEstimator
    print("SUCCESS: RealTimeCostEstimator imported!")
    print(f"Class: {RealTimeCostEstimator}")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting MealCraftAI import...")
from mealcraft_ai import MealCraftAI, REALTIME_PRICES_AVAILABLE
print(f"REALTIME_PRICES_AVAILABLE: {REALTIME_PRICES_AVAILABLE}")

if REALTIME_PRICES_AVAILABLE:
    print("\n✓ Real-time pricing is AVAILABLE!")
else:
    print("\n✗ Real-time pricing is NOT available")
