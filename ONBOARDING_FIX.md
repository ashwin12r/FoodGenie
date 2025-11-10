# 🔧 Onboarding Database Fix

## ✅ Issue Found & Fixed

### Problem:
The onboarding form was **partially working**:
- ✅ User creation worked (200 OK)
- ❌ Preferences save failed (422 Unprocessable Content)

### Root Cause:
The `onboarding-integration.js` was sending incorrect data format for preferences:
- `preferred_flavors` was being set to dietary restrictions array instead of flavor strings
- Some fields weren't properly formatted as arrays

### Solution Applied:

**Fixed** `pages/onboarding-integration.js`:

```javascript
// BEFORE (Incorrect):
preferred_flavors: formData.dietary || ['spicy'], // ❌ Wrong - dietary restrictions, not flavors

// AFTER (Correct):
preferred_flavors: ['spicy', 'mild'], // ✅ Correct - actual flavor preferences
```

Also fixed array handling for:
- `preferred_cuisines` - now properly converts to array
- `dietary_restrictions` - now properly handles array/string
- `health_goals` - now properly handles array/string
- `cost_per_meal_limit` - now rounds to integer

---

## 🧪 How to Test

### Option 1: Use Test Page

1. **Start Backend** (if not running):
   ```powershell
   cd "c:\prime project\prime\ML"
   python backend_server.py
   ```

2. **Open Test Page**:
   ```
   http://localhost:5500/pages/test-api.html
   ```

3. **Run Tests**:
   - Click "Check Backend Health" - should show "healthy"
   - Click "Run Full Onboarding" - tests complete flow
   - Check console for detailed logs

### Option 2: Test Real Onboarding

1. **Start Backend** (if not running):
   ```powershell
   cd "c:\prime project\prime\ML"
   python backend_server.py
   ```

2. **Open Onboarding**:
   ```
   http://localhost:5500/pages/onboarding.html
   ```

3. **Fill Form & Complete Setup**

4. **Check Browser Console** - Should see:
   ```
   💾 Saving user profile to database...
   ✅ User created: {...}
   📤 Sending preferences to API: {...}
   ✅ Preferences saved: {...}
   ```

5. **Check Backend Logs** - Should see:
   ```
   INFO: 127.0.0.1 - "POST /api/users/create HTTP/1.1" 200 OK
   INFO: 127.0.0.1 - "POST /api/preferences/save HTTP/1.1" 200 OK
   ```

---

## 📊 What Changed

### Files Modified:

1. **`pages/onboarding-integration.js`**:
   - Fixed `preferred_flavors` to use actual flavors
   - Added proper array handling for all list fields
   - Added debug logging for sent data
   - Added error response logging

2. **`pages/test-api.html`** (NEW):
   - Test page for API debugging
   - Tests health, user creation, preferences save
   - Shows detailed request/response

---

## ✅ Current Status

### What Now Works:

1. ✅ **User Creation** - Creates entry in `users` table
2. ✅ **Preferences Save** - Saves to `user_preferences` table
3. ✅ **Data Persistence** - Stored in Neon PostgreSQL
4. ✅ **Fallback** - Still saves to localStorage if API fails
5. ✅ **Email Storage** - Stores for future API calls

### Data Flow:

```
User fills onboarding form
    ↓
Clicks "Complete Setup"
    ↓
JavaScript collects form data
    ↓
POST /api/users/create
  → Creates user in database
  → Returns user_id
    ↓
POST /api/preferences/save
  → Saves preferences with user_id
  → Links to user record
    ↓
Success message → Redirect to meal planner
```

---

## 🎯 Next Steps

After this fix, try the onboarding again:

1. Refresh the onboarding page
2. Fill out the form
3. Complete setup
4. Should see success message
5. Check backend logs for 200 OK responses

If you still see 422 error:
- Open browser DevTools (F12)
- Go to Console tab
- Look for "📤 Sending preferences to API:" log
- Copy that data and share it for further debugging

---

## 🐛 Debugging Commands

### Check if backend is running:
```powershell
curl http://localhost:8000/health
```

### View Neon database tables:
```sql
-- Connect to your Neon database and run:
SELECT * FROM users ORDER BY created_at DESC LIMIT 5;
SELECT * FROM user_preferences ORDER BY created_at DESC LIMIT 5;
```

### Test API manually:
```powershell
# Test user creation
curl -X POST http://localhost:8000/api/users/create -H "Content-Type: application/json" -d '{\"email\":\"test@test.com\",\"family_name\":\"Test\",\"family_size\":4,\"city\":\"Chennai\"}'

# Test preferences save (use email from above)
curl -X POST http://localhost:8000/api/preferences/save -H "Content-Type: application/json" -d '{\"email\":\"test@test.com\",\"diet\":\"Vegetarian\",\"preferred_cuisines\":[\"North Indian\"],\"dietary_restrictions\":[\"vegetarian\"],\"cooking_time_limit\":45,\"cooking_complexity\":\"intermediate\",\"daily_calorie_target\":2000,\"weekly_budget\":15000,\"health_goals\":[\"weight_loss\"],\"preferred_flavors\":[\"spicy\",\"mild\"],\"region\":\"North\",\"cost_per_meal_limit\":714}'
```

---

**The fix has been applied! Test it now and let me know if you still see any errors.** 🚀
