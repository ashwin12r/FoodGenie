"""
Test script to verify recipe images and instructions integration
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from recipe_instructions import get_recipe_instructions
from recipe_images import get_recipe_image

# Test dishes
test_dishes = [
    "Dal tadka",
    "Butter chicken",
    "Masala dosa",
    "Biryani",
    "Unknown dish"
]

print("=" * 70)
print("RECIPE INTEGRATION TEST")
print("=" * 70)

for dish in test_dishes:
    print(f"\n🍽️  Testing: {dish}")
    print("-" * 70)
    
    # Test image
    image_url = get_recipe_image(dish)
    print(f"   Image URL: {image_url[:60]}...")
    
    # Test instructions
    instructions = get_recipe_instructions(dish)
    if instructions:
        print(f"   ✅ Instructions: {len(instructions['instructions'])} steps")
        print(f"   💡 Tips: {instructions.get('tips', 'N/A')[:50]}...")
        print(f"   🍽️  Serving: {instructions.get('serving', 'N/A')}")
    else:
        print(f"   ⚠️  No detailed instructions found (will use generated)")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
