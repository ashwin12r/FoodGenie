"""
🍳 Breakfast Classification Fix
Enhances the dataset to properly classify breakfast-appropriate dishes.
"""

import pandas as pd

def fix_breakfast_classification():
    """
    Reclassifies breakfast-appropriate main courses as snacks/breakfast items.
    """
    print("=" * 70)
    print("🍳 FIXING BREAKFAST CLASSIFICATION")
    print("=" * 70)
    
    # Read the dataset
    print("\n1️⃣  Loading indian_food.csv...")
    df = pd.read_csv('indian_food.csv')
    print(f"   Total dishes: {len(df)}")
    
    # Define breakfast-appropriate dishes currently misclassified as main course
    breakfast_mains = [
        # Breads/Rotis
        'Paratha', 'Thepla', 'Makki di roti', 'Sattu ki roti',
        'Akki roti', 'Chapati', 'Roti', 'Puri', 
        'Luchi', 'Bhatura', 'Kulcha', 'Naan',
        
        # Quick breakfast dishes
        'Aloo tikki',  # Already good, but ensure it stays
    ]
    
    print(f"\n2️⃣  Identifying dishes to reclassify...")
    print(f"   Looking for {len(breakfast_mains)} potential breakfast items...")
    
    # Find dishes that match
    breakfast_mask = (
        (df['name'].isin(breakfast_mains)) & 
        (df['course'] == 'main course')
    )
    
    dishes_to_reclassify = df[breakfast_mask]['name'].tolist()
    
    if dishes_to_reclassify:
        print(f"\n   Found {len(dishes_to_reclassify)} dishes to reclassify:")
        for dish in dishes_to_reclassify:
            print(f"      - {dish}")
        
        # Reclassify to snack
        df.loc[breakfast_mask, 'course'] = 'snack'
        print(f"\n   ✅ Reclassified {len(dishes_to_reclassify)} dishes to 'snack'")
    else:
        print("   ℹ️  No dishes found to reclassify (may already be correct)")
    
    # Also check if any snacks are currently desserts but should be snacks
    # (This is less common but possible)
    
    print("\n3️⃣  Analyzing course distribution...")
    print("\n   BEFORE:")
    before_dist = df.groupby('course').size()
    print(before_dist.to_string())
    
    # Save the fixed dataset
    output_file = 'indian_food_fixed.csv'
    df.to_csv(output_file, index=False)
    print(f"\n4️⃣  Saved fixed dataset: {output_file}")
    
    print("\n   AFTER:")
    after_dist = df.groupby('course').size()
    print(after_dist.to_string())
    
    # Analyze breakfast options now available
    print("\n5️⃣  Breakfast options analysis:")
    snacks = df[df['course'] == 'snack']
    print(f"\n   Total snacks: {len(snacks)}")
    print(f"   Vegetarian: {len(snacks[snacks['diet'] == 'vegetarian'])}")
    print(f"   Non-vegetarian: {len(snacks[snacks['diet'] == 'non vegetarian'])}")
    
    print("\n   Sample breakfast items:")
    breakfast_samples = snacks.head(15)[['name', 'diet', 'prep_time', 'cook_time', 'region']]
    print(breakfast_samples.to_string(index=False))
    
    print("\n" + "=" * 70)
    print("✅ BREAKFAST CLASSIFICATION FIX COMPLETE!")
    print("=" * 70)
    
    print("\n💡 Next steps:")
    print("   1. Update mealcraft_ai.py to use 'indian_food_fixed.csv'")
    print("   2. Run: python test_healthy.py")
    print("   3. Verify breakfast now has better variety")
    
    return df

def create_breakfast_enhanced_dataset():
    """
    Creates a version with additional metadata for breakfast suitability.
    """
    print("\n" + "=" * 70)
    print("🌟 CREATING BREAKFAST-ENHANCED DATASET")
    print("=" * 70)
    
    df = pd.read_csv('indian_food_fixed.csv')
    
    # Add metadata column
    df['is_breakfast_suitable'] = df['course'].isin(['snack', 'starter'])
    
    # Quick dishes (< 30 min total) could also be breakfast suitable
    df['is_quick_dish'] = (
        (df['prep_time'].fillna(0) + df['cook_time'].fillna(0)) < 30
    )
    
    # Classify meal types
    def get_meal_type(row):
        if row['course'] == 'snack':
            return 'breakfast'
        elif row['course'] == 'main course':
            return 'lunch_dinner'
        elif row['course'] == 'dessert':
            return 'dessert'
        elif row['course'] == 'starter':
            return 'appetizer'
        return 'other'
    
    df['meal_type'] = df.apply(get_meal_type, axis=1)
    
    # Save
    output_file = 'indian_food_enhanced.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Created enhanced dataset: {output_file}")
    print("\nNew columns added:")
    print("   - is_breakfast_suitable (boolean)")
    print("   - is_quick_dish (boolean)")
    print("   - meal_type (breakfast/lunch_dinner/dessert/appetizer)")
    
    print("\n📊 Meal type distribution:")
    print(df['meal_type'].value_counts().to_string())
    
    return df

if __name__ == "__main__":
    # Fix classification
    df_fixed = fix_breakfast_classification()
    
    # Create enhanced version
    df_enhanced = create_breakfast_enhanced_dataset()
    
    print("\n" + "=" * 70)
    print("🎉 ALL DONE!")
    print("=" * 70)
    print("\n📁 Files created:")
    print("   1. indian_food_fixed.csv - Reclassified breakfast items")
    print("   2. indian_food_enhanced.csv - With additional metadata")
    print("\n🚀 Ready to use with MealCraft-AI!")
