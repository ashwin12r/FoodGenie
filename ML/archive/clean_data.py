"""
Data Cleaning and Preprocessing for MealCraft-AI
Cleans the dataset and creates a health-focused version
"""

import pandas as pd
import numpy as np


def clean_dataset(input_file='indian_food.csv', output_file='indian_food_cleaned.csv'):
    """
    Clean the Indian food dataset:
    1. Replace -1 values with appropriate defaults
    2. Fill missing times with estimates
    3. Standardize categories
    4. Fix data quality issues
    """
    print("🧹 Starting data cleaning process...")
    
    # Load dataset
    df = pd.read_csv(input_file)
    print(f"📊 Original dataset: {len(df)} dishes")
    
    # 1. Replace -1 in prep_time and cook_time
    print("\n1️⃣  Fixing -1 values in time fields...")
    
    # Replace -1 prep_time based on course type
    prep_time_defaults = {
        'main course': 15,
        'snack': 10,
        'dessert': 15,
        'starter': 10
    }
    
    for course, default_time in prep_time_defaults.items():
        mask = (df['course'] == course) & ((df['prep_time'] == -1) | (df['prep_time'].isna()))
        df.loc[mask, 'prep_time'] = default_time
    
    # Replace -1 cook_time based on course type
    cook_time_defaults = {
        'main course': 30,
        'snack': 20,
        'dessert': 30,
        'starter': 20
    }
    
    for course, default_time in cook_time_defaults.items():
        mask = (df['course'] == course) & ((df['cook_time'] == -1) | (df['cook_time'].isna()))
        df.loc[mask, 'cook_time'] = default_time
    
    # 2. Replace -1 in state and region
    print("2️⃣  Fixing -1 values in state/region fields...")
    
    # For dishes with -1 region, set to 'All India' (popular across India)
    df.loc[df['state'] == '-1', 'state'] = 'All India'
    df.loc[df['region'] == '-1', 'region'] = 'All'
    
    # 3. Fix -1 in flavor_profile
    print("3️⃣  Fixing -1 values in flavor_profile...")
    df.loc[df['flavor_profile'] == '-1', 'flavor_profile'] = 'mild'
    
    # 4. Ensure all missing values are handled
    print("4️⃣  Handling remaining missing values...")
    df['prep_time'] = df['prep_time'].fillna(15)
    df['cook_time'] = df['cook_time'].fillna(30)
    df['flavor_profile'] = df['flavor_profile'].fillna('mild')
    df['region'] = df['region'].fillna('All')
    df['state'] = df['state'].fillna('All India')
    
    # 5. Add total_time column
    df['total_time'] = df['prep_time'] + df['cook_time']
    
    # Save cleaned dataset
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Cleaned dataset saved: {output_file}")
    print(f"📊 Total dishes: {len(df)}")
    print(f"   - Main course: {len(df[df['course'] == 'main course'])}")
    print(f"   - Snacks: {len(df[df['course'] == 'snack'])}")
    print(f"   - Desserts: {len(df[df['course'] == 'dessert'])}")
    print(f"   - Starters: {len(df[df['course'] == 'starter'])}")
    
    return df


def create_healthy_dataset(input_file='indian_food_cleaned.csv', 
                          output_file='indian_food_healthy.csv'):
    """
    Create a health-focused dataset:
    1. Focus on main course dishes (remove most desserts)
    2. Convert healthy snacks to breakfast options
    3. Keep only nutritious, balanced meals
    """
    print("\n" + "="*70)
    print("🥗 Creating health-focused dataset...")
    print("="*70)
    
    df = pd.read_csv(input_file)
    
    # Define healthy snacks that can be breakfast (not sweet desserts)
    healthy_breakfast_snacks = [
        'Poha', 'Upma', 'Idli', 'Dosa', 'Uttapam', 'Pesarattu',
        'Dhokla', 'Thepla', 'Paratha', 'Aloo tikki', 'Vada',
        'Kachori', 'Samosa', 'Puri Bhaji', 'Idiappam', 'Puttu',
        'Thalipeeth', 'Sabudana Khichadi', 'Poori', 'Sevai',
        'Paniyaram', 'Handvo', 'Muthiya'
    ]
    
    # 1. Keep all main course dishes
    main_courses = df[df['course'] == 'main course'].copy()
    print(f"\n1️⃣  Main course dishes: {len(main_courses)}")
    
    # 2. Keep healthy snacks for breakfast
    healthy_snacks = df[
        (df['course'] == 'snack') & 
        (df['name'].isin(healthy_breakfast_snacks))
    ].copy()
    
    # Mark these as suitable for breakfast
    healthy_snacks['suitable_for'] = 'breakfast'
    print(f"2️⃣  Healthy breakfast snacks: {len(healthy_snacks)}")
    
    # 3. Keep only starters (can be used for variety)
    starters = df[df['course'] == 'starter'].copy()
    print(f"3️⃣  Starters kept: {len(starters)}")
    
    # 4. Keep only a few healthy desserts (for occasional use)
    healthy_desserts = [
        'Kheer', 'Payasam', 'Phirni', 'Misti doi', 'Basundi',
        'Shrikhand', 'Rabri'  # Milk-based, relatively healthier
    ]
    
    desserts = df[
        (df['course'] == 'dessert') & 
        (df['name'].isin(healthy_desserts))
    ].copy()
    print(f"4️⃣  Healthy desserts kept: {len(desserts)}")
    
    # Combine all healthy dishes
    healthy_df = pd.concat([
        main_courses,
        healthy_snacks,
        starters,
        desserts
    ], ignore_index=True)
    
    # Add suitable_for column to main courses
    healthy_df.loc[healthy_df['course'] == 'main course', 'suitable_for'] = 'lunch,dinner'
    healthy_df.loc[healthy_df['course'] == 'starter', 'suitable_for'] = 'lunch,dinner'
    healthy_df.loc[healthy_df['course'] == 'dessert', 'suitable_for'] = 'occasional'
    
    # Fill NaN in suitable_for
    healthy_df['suitable_for'] = healthy_df['suitable_for'].fillna('lunch,dinner')
    
    # Save healthy dataset
    healthy_df.to_csv(output_file, index=False)
    
    print(f"\n✅ Healthy dataset saved: {output_file}")
    print(f"📊 Total healthy dishes: {len(healthy_df)}")
    print(f"\n📈 Breakdown:")
    print(f"   - Main courses: {len(healthy_df[healthy_df['course'] == 'main course'])}")
    print(f"   - Breakfast options: {len(healthy_df[healthy_df['suitable_for'] == 'breakfast'])}")
    print(f"   - Starters: {len(healthy_df[healthy_df['course'] == 'starter'])}")
    print(f"   - Healthy desserts: {len(healthy_df[healthy_df['course'] == 'dessert'])}")
    
    # Show statistics
    print(f"\n📊 Diet distribution:")
    print(healthy_df['diet'].value_counts())
    
    print(f"\n🗺️  Region distribution:")
    print(healthy_df['region'].value_counts())
    
    return healthy_df


def analyze_dataset_quality(file='indian_food_cleaned.csv'):
    """Analyze data quality after cleaning"""
    print("\n" + "="*70)
    print("🔍 DATA QUALITY ANALYSIS")
    print("="*70)
    
    df = pd.read_csv(file)
    
    print(f"\n1️⃣  Missing Values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✅ No missing values!")
    else:
        print(missing[missing > 0])
    
    print(f"\n2️⃣  -1 Values:")
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            count = (df[col] == -1).sum()
            if count > 0:
                print(f"   ⚠️  {col}: {count} instances of -1")
        elif df[col].dtype == 'object':
            count = (df[col] == '-1').sum()
            if count > 0:
                print(f"   ⚠️  {col}: {count} instances of '-1'")
    
    if ((df.select_dtypes(include=['number']) == -1).sum().sum() == 0 and
        (df.select_dtypes(include=['object']) == '-1').sum().sum() == 0):
        print("   ✅ No -1 values found!")
    
    print(f"\n3️⃣  Time Statistics:")
    print(f"   Prep time: min={df['prep_time'].min()}, max={df['prep_time'].max()}, avg={df['prep_time'].mean():.1f}")
    print(f"   Cook time: min={df['cook_time'].min()}, max={df['cook_time'].max()}, avg={df['cook_time'].mean():.1f}")
    print(f"   Total time: min={df['total_time'].min()}, max={df['total_time'].max()}, avg={df['total_time'].mean():.1f}")
    
    print(f"\n4️⃣  Course Distribution:")
    print(df['course'].value_counts())
    
    print(f"\n5️⃣  Flavor Profile Distribution:")
    print(df['flavor_profile'].value_counts())


def main():
    """Main execution"""
    print("="*70)
    print("🍽️  MEALCRAFT-AI DATA CLEANING & PREPROCESSING")
    print("="*70)
    
    # Step 1: Clean the original dataset
    cleaned_df = clean_dataset('indian_food.csv', 'indian_food_cleaned.csv')
    
    # Step 2: Analyze data quality
    analyze_dataset_quality('indian_food_cleaned.csv')
    
    # Step 3: Create health-focused dataset
    healthy_df = create_healthy_dataset('indian_food_cleaned.csv', 'indian_food_healthy.csv')
    
    # Step 4: Show sample from healthy dataset
    print("\n" + "="*70)
    print("📋 SAMPLE FROM HEALTHY DATASET")
    print("="*70)
    print("\nSample main courses:")
    print(healthy_df[healthy_df['course'] == 'main course'][['name', 'diet', 'total_time', 'region']].head(10))
    
    print("\nSample breakfast options:")
    breakfast = healthy_df[healthy_df['suitable_for'] == 'breakfast']
    if len(breakfast) > 0:
        print(breakfast[['name', 'diet', 'total_time', 'region']].head(10))
    
    print("\n" + "="*70)
    print("✅ DATA CLEANING COMPLETE!")
    print("="*70)
    print("\n📁 Files created:")
    print("   1. indian_food_cleaned.csv - Full cleaned dataset")
    print("   2. indian_food_healthy.csv - Health-focused dataset")
    print("\n💡 Next steps:")
    print("   1. Use 'indian_food_healthy.csv' in MealCraft-AI")
    print("   2. Run updated meal planning with health focus")
    print("   3. Breakfast will now use healthy snacks, not sweets!")


if __name__ == "__main__":
    main()
