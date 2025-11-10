# 🤖 AI Shopping Assistant - Browser Automation Guide

## Overview
The AI Shopping Assistant now features **intelligent browser automation** that opens Chrome and automatically adds ingredients to your cart, just like in the demo video!

## How It Works

### 1️⃣ Select Your Meal
- Click on any meal from your meal planner in the left panel
- The AI agent will show the ingredient list

### 2️⃣ Confirm Purchase
- AI asks: *"Would you like to proceed with purchasing these ingredients?"*
- Type "yes" or click the confirmation button

### 3️⃣ Choose Your Store
Select from 6 integrated stores:
- **BigBasket** - 2-3 hours delivery
- **Zepto** - 10 minutes delivery ⚡
- **Blinkit** - 15 minutes delivery
- **Swiggy Instamart** - 15-20 minutes delivery
- **Amazon Fresh** - 2 hours delivery
- **JioMart** - Next day delivery

### 4️⃣ AI Automation Magic ✨
When you click "Place Order":
1. **Chrome browser opens automatically**
2. **Navigates to your selected store** (e.g., BigBasket.com)
3. **Searches for each ingredient** one by one
4. **Adds items to cart** automatically
5. **Takes you to cart** for review and checkout

## Supported Stores (Full Automation)

### ✅ BigBasket
- Full automation support
- Auto-search and add to cart
- Location handling
- Cart redirect

### ✅ Zepto  
- Full automation support
- Quick search
- Fast add to cart
- 10-minute delivery

### 🟡 Other Stores (Manual)
For Blinkit, Swiggy, Amazon Fresh, and JioMart:
- Opens the store website
- Provides ingredient list for manual shopping
- AI guides you through the process

## Technical Implementation

### Backend (Python + Selenium)
```python
# browser_automation.py
- GroceryAutomation class
- Chrome WebDriver management
- Store-specific automation logic
- Item search and add-to-cart
```

### Frontend (JavaScript)
```javascript
// smart-shopping-ai.js
- Calls /api/automate-order endpoint
- Passes store name and ingredients
- Shows automation progress
- Fallback to manual if automation fails
```

### API Endpoint
```
POST /api/automate-order
{
  "store_name": "BigBasket",
  "ingredients": ["onions", "tomatoes", "rice"],
  "meal_name": "Dal Tadka"
}
```

## Requirements

### Python Packages
```bash
pip install selenium webdriver-manager
```

### Chrome Browser
- Chrome must be installed on your system
- WebDriver Manager will auto-download ChromeDriver
- Works with latest Chrome versions

## Troubleshooting

### Issue: Browser doesn't open
**Solution**: Make sure Chrome is installed and Selenium packages are installed
```bash
pip install selenium webdriver-manager
```

### Issue: Can't find items
**Reason**: Store website structure changed or items out of stock
**Solution**: The AI will list items not found - add them manually

### Issue: Automation fails
**Fallback**: System automatically opens store website for manual shopping

## Future Enhancements

### 🔮 Planned Features
1. **Multi-store price comparison** - Find the best deals automatically
2. **Voice commands** - "Hey MealCraft, order my groceries from Zepto"
3. **Payment integration** - Complete checkout automatically (with user permission)
4. **Scheduled orders** - Auto-order groceries every week
5. **Smart substitutions** - If item unavailable, suggest alternatives
6. **Order tracking** - Real-time delivery status updates

### 🎯 Advanced Automation
- **Headless mode** - Run automation in background
- **Faster execution** - Optimize search and add-to-cart
- **Better error handling** - Handle popups, login screens
- **Multi-tab support** - Compare prices across stores simultaneously

## Privacy & Security

### What We Do
✅ Open browser locally on your machine
✅ Navigate to store websites you choose
✅ Search for ingredients you approved
✅ Add items to cart (no purchase without your approval)

### What We DON'T Do
❌ Store your payment information
❌ Make purchases without your confirmation
❌ Share your data with third parties
❌ Access your personal information

## Demo Video Reference

Watch the inspiration: https://youtu.be/G5djZjdxVvo?si=XL_xm2IsNGQY7v-W

At 2:19 - See how AI agent opens Google Flights and searches automatically
**Our Implementation** - Same concept but for grocery shopping! 🛒

## Usage Tips

### For Best Results
1. **Review the cart** before checkout - Automation isn't perfect
2. **Check quantities** - AI adds default quantity (usually 1)
3. **Verify prices** - Prices may vary from estimates
4. **Have login ready** - Some stores require account login
5. **Keep browser open** - Don't close during automation

### Quick Start
```
1. Plan meals → Meal Planner page
2. Open Smart Shopping → AI Assistant
3. Click meal → See ingredients
4. Confirm → Choose store (BigBasket recommended)
5. Place Order → Watch the magic! ✨
```

## Support

Need help? The AI agent will guide you through the process:
- Ask questions in the chat
- AI provides step-by-step instructions
- Fallback options if automation fails

---

**Built with ❤️ using:**
- FastAPI (Backend)
- Selenium WebDriver (Browser Automation)
- Tailwind CSS (UI)
- Chrome DevTools (Web Scraping)

**Version**: 1.0.0
**Last Updated**: November 10, 2025
