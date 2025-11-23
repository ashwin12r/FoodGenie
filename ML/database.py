"""
Database Connection Module for MealCraft
Uses Neon PostgreSQL for cloud database
"""

import os
from typing import Optional, Dict, List, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from datetime import datetime
import json

# Database configuration
# Set these environment variables or update with your Neon connection string
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://neondb_owner:npg_4iaFwsRzm2pv@ep-divine-pond-a49q3o6d-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
)

class DatabaseManager:
    """Manages PostgreSQL database connections and operations"""
    
    def __init__(self, connection_string: str = DATABASE_URL):
        """Initialize database connection pool"""
        self.connection_string = connection_string
        self.pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Create connection pool"""
        try:
            self.pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=self.connection_string
            )
            print("[OK] Database connection pool created successfully")
        except Exception as e:
            print(f"[ERROR] Error creating connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        return self.pool.getconn()
    
    def return_connection(self, conn):
        """Return connection to the pool"""
        self.pool.putconn(conn)
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        if self.pool:
            self.pool.closeall()
    
    # === SCHEMA INITIALIZATION ===
    
    def initialize_schema(self):
        """Create all necessary database tables"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # Users table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE,
                        user_name VARCHAR(255),
                        password_hash VARCHAR(255),
                        family_size INTEGER DEFAULT 1,
                        city VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # User preferences table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        diet VARCHAR(50),
                        preferred_cuisines JSONB,
                        dietary_restrictions JSONB,
                        cooking_time_limit INTEGER,
                        cooking_complexity VARCHAR(50),
                        daily_calorie_target INTEGER,
                        weekly_budget DECIMAL(10, 2),
                        health_goals JSONB,
                        preferred_flavors JSONB,
                        region VARCHAR(100),
                        cost_per_meal_limit DECIMAL(10, 2),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id)
                    )
                """)
                
                # Meal plans table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS meal_plans (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        plan_data JSONB NOT NULL,
                        start_date DATE,
                        end_date DATE,
                        total_cost DECIMAL(10, 2),
                        total_calories INTEGER,
                        status VARCHAR(50) DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Shopping lists table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS shopping_lists (
                        id SERIAL PRIMARY KEY,
                        meal_plan_id INTEGER REFERENCES meal_plans(id) ON DELETE CASCADE,
                        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        items JSONB NOT NULL,
                        total_cost DECIMAL(10, 2),
                        status VARCHAR(50) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        completed_at TIMESTAMP
                    )
                """)
                
                # Grocery prices table (cache from web scraping)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS grocery_prices (
                        id SERIAL PRIMARY KEY,
                        item_name VARCHAR(255) NOT NULL,
                        store_name VARCHAR(100) NOT NULL,
                        price DECIMAL(10, 2) NOT NULL,
                        unit VARCHAR(50),
                        category VARCHAR(100),
                        in_stock BOOLEAN DEFAULT true,
                        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(item_name, store_name)
                    )
                """)
                
                # Create indexes for better performance
                cur.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_meal_plans_user_id ON meal_plans(user_id)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_meal_plans_start_date ON meal_plans(start_date)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_grocery_prices_item ON grocery_prices(item_name)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_grocery_prices_store ON grocery_prices(store_name)")
                
                conn.commit()
                print("[OK] Database schema initialized successfully")
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Error initializing schema: {e}")
            raise
        finally:
            self.return_connection(conn)
    
    # === USER OPERATIONS ===
    
    def create_user(self, email: str, user_name: str, family_size: int = 1, city: str = 'Mumbai') -> Optional[int]:
        """Create a new user"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (email, user_name, family_size, city)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (email) DO UPDATE 
                    SET user_name = EXCLUDED.user_name,
                        family_size = EXCLUDED.family_size,
                        city = EXCLUDED.city,
                        updated_at = CURRENT_TIMESTAMP
                    RETURNING id
                """, (email, user_name, family_size, city))
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Error creating user: {e}")
            return None
        finally:
            self.return_connection(conn)
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                return dict(cur.fetchone()) if cur.rowcount > 0 else None
        finally:
            self.return_connection(conn)
    
    def save_user_password(self, user_id: int, password: str) -> bool:
        """Save user password (simple version - in production use bcrypt!)"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # Simple hash for demo - in production use bcrypt or passlib
                import hashlib
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                cur.execute(
                    "UPDATE users SET password_hash = %s WHERE id = %s",
                    (password_hash, user_id)
                )
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Error saving password: {e}")
            return False
        finally:
            self.return_connection(conn)
    
    def verify_user_password(self, user_id: int, password: str) -> bool:
        """Verify user password"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                import hashlib
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                cur.execute(
                    "SELECT id FROM users WHERE id = %s AND password_hash = %s",
                    (user_id, password_hash)
                )
                return cur.rowcount > 0
        finally:
            self.return_connection(conn)
    
    # === USER PREFERENCES ===
    
    def save_user_preferences(self, user_id: int, preferences: Dict) -> bool:
        """Save or update user preferences"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO user_preferences (
                        user_id, diet, preferred_cuisines, dietary_restrictions,
                        cooking_time_limit, cooking_complexity, daily_calorie_target,
                        weekly_budget, health_goals, preferred_flavors, region, cost_per_meal_limit
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE SET
                        diet = EXCLUDED.diet,
                        preferred_cuisines = EXCLUDED.preferred_cuisines,
                        dietary_restrictions = EXCLUDED.dietary_restrictions,
                        cooking_time_limit = EXCLUDED.cooking_time_limit,
                        cooking_complexity = EXCLUDED.cooking_complexity,
                        daily_calorie_target = EXCLUDED.daily_calorie_target,
                        weekly_budget = EXCLUDED.weekly_budget,
                        health_goals = EXCLUDED.health_goals,
                        preferred_flavors = EXCLUDED.preferred_flavors,
                        region = EXCLUDED.region,
                        cost_per_meal_limit = EXCLUDED.cost_per_meal_limit,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    user_id,
                    preferences.get('diet'),
                    json.dumps(preferences.get('preferred_cuisines', [])),
                    json.dumps(preferences.get('dietary_restrictions', [])),
                    preferences.get('cooking_time_limit'),
                    preferences.get('cooking_complexity'),
                    preferences.get('daily_calorie_target'),
                    preferences.get('weekly_budget'),
                    json.dumps(preferences.get('health_goals', [])),
                    json.dumps(preferences.get('preferred_flavors', [])),
                    preferences.get('region'),
                    preferences.get('cost_per_meal_limit')
                ))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Error saving preferences: {e}")
            return False
        finally:
            self.return_connection(conn)
    
    def get_user_preferences(self, user_id: int) -> Optional[Dict]:
        """Get user preferences"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))
                return dict(cur.fetchone()) if cur.rowcount > 0 else None
        finally:
            self.return_connection(conn)
    
    # === MEAL PLANS ===
    
    def save_meal_plan(self, user_id: int, plan_data: Dict, start_date: str, end_date: str) -> Optional[int]:
        """Save a generated meal plan"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                summary = plan_data.get('summary', {})
                total_cost = float(summary.get('total_cost', '0').replace('₹', '').replace(',', ''))
                total_calories = float(summary.get('daily_avg_calories', 0)) * 7  # Convert to Python float
                
                cur.execute("""
                    INSERT INTO meal_plans (user_id, plan_data, start_date, end_date, total_cost, total_calories)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (user_id, json.dumps(plan_data), start_date, end_date, total_cost, total_calories))
                meal_plan_id = cur.fetchone()[0]
                conn.commit()
                return meal_plan_id
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Error saving meal plan: {e}")
            return None
        finally:
            self.return_connection(conn)
    
    def get_meal_plan(self, meal_plan_id: int) -> Optional[Dict]:
        """Get a specific meal plan"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM meal_plans WHERE id = %s", (meal_plan_id,))
                return dict(cur.fetchone()) if cur.rowcount > 0 else None
        finally:
            self.return_connection(conn)
    
    def get_user_meal_plans(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's meal plans"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM meal_plans 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC 
                    LIMIT %s
                """, (user_id, limit))
                return [dict(row) for row in cur.fetchall()]
        finally:
            self.return_connection(conn)
    
    # === SHOPPING LISTS ===
    
    def save_shopping_list(self, meal_plan_id: int, user_id: int, items: List[Dict], total_cost: float) -> Optional[int]:
        """Save a shopping list"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO shopping_lists (meal_plan_id, user_id, items, total_cost)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (meal_plan_id, user_id, json.dumps(items), total_cost))
                shopping_list_id = cur.fetchone()[0]
                conn.commit()
                return shopping_list_id
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Error saving shopping list: {e}")
            return None
        finally:
            self.return_connection(conn)
    
    def get_user_shopping_lists(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's shopping lists"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM shopping_lists 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC 
                    LIMIT %s
                """, (user_id, limit))
                return [dict(row) for row in cur.fetchall()]
        finally:
            self.return_connection(conn)
    
    # === GROCERY PRICES ===
    
    def update_grocery_prices(self, prices: List[Dict]) -> int:
        """Update grocery prices from web scraping"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                count = 0
                for item in prices:
                    cur.execute("""
                        INSERT INTO grocery_prices (item_name, store_name, price, unit, category, in_stock)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (item_name, store_name) DO UPDATE SET
                            price = EXCLUDED.price,
                            in_stock = EXCLUDED.in_stock,
                            scraped_at = CURRENT_TIMESTAMP
                    """, (
                        item.get('name'),
                        item.get('store'),
                        item.get('price'),
                        item.get('unit', 'unit'),
                        item.get('category', 'general'),
                        item.get('in_stock', True)
                    ))
                    count += 1
                conn.commit()
                return count
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Error updating grocery prices: {e}")
            return 0
        finally:
            self.return_connection(conn)
    
    def get_grocery_prices(self, store_name: Optional[str] = None) -> List[Dict]:
        """Get grocery prices, optionally filtered by store"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if store_name:
                    cur.execute("""
                        SELECT * FROM grocery_prices 
                        WHERE store_name = %s AND in_stock = true
                        ORDER BY item_name
                    """, (store_name,))
                else:
                    cur.execute("""
                        SELECT * FROM grocery_prices 
                        WHERE in_stock = true
                        ORDER BY store_name, item_name
                    """)
                return [dict(row) for row in cur.fetchall()]
        finally:
            self.return_connection(conn)


# Singleton instance
db = DatabaseManager()


if __name__ == "__main__":
    # Test database connection and schema
    print("[INFO] Testing database connection...")
    try:
        db.initialize_schema()
        print("[OK] Database setup complete!")
    except Exception as e:
        print(f"[ERROR] Database setup failed: {e}")
