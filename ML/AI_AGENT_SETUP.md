# 🤖 AI Agent Setup Guide - Grocery Shopping Automation

## Overview
This implementation uses **browser-use** library with AI (Claude/GPT-4) to automate grocery shopping - the EXACT architecture from the YouTube video (Google Flights automation).

## How It Works

### Architecture (Same as Video)
```
User clicks "Place Order"
    ↓
FastAPI Backend (/api/automate-order)
    ↓
AI Agent (browser-use.Agent)
    ↓
Claude AI Model (understands web page)
    ↓
Playwright (controls Chrome browser)
    ↓
BigBasket website (automated shopping)
```

### Key Difference from Traditional Automation
- ❌ **Traditional**: Hard-coded CSS selectors: `.search-box`, `#add-to-cart`
- ✅ **AI Agent**: Natural language: "Find the search box", "Click Add to Cart"
- 💡 **Benefit**: AI figures out how to interact with the page automatically!

## Setup Steps

### 1. Install Dependencies (Already Done ✅)
```bash
pip install browser-use
pip install langchain-anthropic langchain-openai
pip install playwright
playwright install chromium
```

### 2. Get API Key (REQUIRED)

#### Option A: Anthropic Claude (Recommended - Used in Video)
1. Go to: https://console.anthropic.com/
2. Sign up / Log in
3. Click "Get API Keys"
4. Create new key
5. Copy the key: `sk-ant-api03-...`

**Free Credits**: You get $5 free credits to test!

#### Option B: OpenAI GPT-4 (Fallback)
1. Go to: https://platform.openai.com/api-keys
2. Sign up / Log in
3. Create new secret key
4. Copy the key: `sk-proj-...`

**Cost**: ~$0.01-0.05 per automation session

### 3. Configure API Key

#### Create `.env` file in `ML/` directory:
```bash
# Copy the template
cp .env.template .env

# Edit .env and add your key:
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# OR for OpenAI:
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

**Important**: Never commit `.env` file to git!

### 4. Test the Setup

#### Check if API key is loaded:
```bash
cd ML
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded:', bool(os.getenv('ANTHROPIC_API_KEY')))"
```

#### Test AI Agent:
```python
import asyncio
from ai_grocery_agent import automate_grocery_shopping_ai

# Test with sample ingredients
result = asyncio.run(automate_grocery_shopping_ai(
    store_name="BigBasket",
    ingredients=["onions", "tomatoes"]
))
print(result)
```

### 5. Run the Application

#### Start backend server:
```bash
cd ML
python backend_server.py
```

#### Open frontend:
- Open `smart-shopping-ai.html` in browser
- Click on a meal plan
- Select "BigBasket"
- Click "Place Order"
- Watch AI agent take control! 🤖

## What Happens During Automation

### Console Output:
```
🤖 AI Agent starting automation...
🤖 Store: BigBasket
🤖 Ingredients: ['onions', 'tomatoes', 'garlic']
🌐 Opening browser...
🚀 AI Agent is now controlling the browser...
   → AI: "I see a search box at the top"
   → AI: "Typing 'onions' into search box"
   → AI: "I found 'Add to Cart' button"
   → AI: "Clicked the button"
✅ Automation complete!
{
  "items_added": ["onions", "tomatoes", "garlic"],
  "items_not_found": [],
  "total_items": 3
}
```

### Browser Window:
- Chrome opens automatically
- AI navigates to BigBasket.com
- AI searches for each ingredient
- AI clicks "Add to Cart"
- AI proceeds to checkout (if instructed)

## How AI Makes Decisions

### The Natural Language Task:
```python
def grocery_shopping_task(ingredients, store_name):
    return f"""
    You are shopping on {store_name} for these items: {', '.join(ingredients)}
    
    For each ingredient:
    1. Find the search box on the page (it might be in the header, navigation bar, or main content area)
    2. Type the ingredient name into the search box
    3. Press Enter or click the search button
    4. Wait for search results to load
    5. Look for the product in the results
    6. Find the 'Add to Cart' or 'Add' button
    7. Click the button to add the item
    8. Wait for confirmation (cart icon update, notification, etc.)
    
    Return JSON:
    {{
      "items_added": ["list", "of", "added"],
      "items_not_found": ["list", "if", "any"]
    }}
    """
```

**The AI reads this like a human would!**

## Customization

### For Different Stores:
```python
# In ai_grocery_agent.py
async def automate_zepto_shopping(ingredients: List[str]):
    initial_actions = [{"open_tab": {"url": "https://www.zeptonow.com"}}]
    
    agent = Agent(
        task=grocery_shopping_task(ingredients, "Zepto"),
        llm=model,
        initial_actions=initial_actions,
        browser=browser,
    )
    # ... rest is same
```

### For Better Instructions:
Edit `grocery_shopping_task()` to give more specific guidance:
```python
# Add store-specific hints:
if store_name == "BigBasket":
    task += "\nNote: Search box is usually in the top-right corner"
    task += "\nNote: Add to Cart button is red"
```

## Troubleshooting

### ❌ "No API key found!"
- **Cause**: `.env` file missing or empty
- **Fix**: Create `.env` file with your API key

### ❌ "Could not find Chrome"
- **Cause**: Chrome path incorrect
- **Fix**: Update `chrome_instance_path` in `ai_grocery_agent.py`:
  ```python
  BrowserConfig(
      chrome_instance_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
  )
  ```

### ❌ AI gets stuck on page
- **Cause**: Page structure changed, AI confused
- **Fix**: Make task instructions more specific
- **Example**: "The search box has placeholder text 'Search for products'"

### ❌ "playwright not installed"
- **Cause**: Browser binaries missing
- **Fix**: `playwright install chromium`

### ❌ High API costs
- **Monitor**: Check usage at Anthropic/OpenAI dashboard
- **Optimize**: Make task instructions clearer (fewer attempts)
- **Limit**: Add timeout in BrowserConfig

## Cost Estimation

### Per Automation Session:
- **Claude 3.5 Sonnet**: ~$0.01-0.03 per session
- **GPT-4o**: ~$0.02-0.05 per session

### Factors:
- Number of ingredients (more = more AI calls)
- Page complexity (complex pages need more reasoning)
- Success rate (failed attempts cost more)

### Free Tier:
- Anthropic: $5 free credits = ~200 sessions
- OpenAI: $5 free credits = ~100 sessions

## Advanced Features

### Add Progress Streaming:
```python
# Show AI thinking in real-time
agent = Agent(
    task=task,
    llm=model,
    browser=browser,
    controller=Controller(streaming=True)  # Enable streaming
)

async for event in agent.stream():
    print(f"AI: {event.message}")
```

### Add Screenshots:
```python
# Save screenshots during automation
BrowserConfig(
    headless=False,
    save_recording_path="./recordings/"
)
```

### Chain Multiple Stores:
```python
# Try BigBasket first, fallback to Zepto
result = await automate_bigbasket_shopping(ingredients)
if result["items_not_found"]:
    result2 = await automate_zepto_shopping(result["items_not_found"])
```

## Comparison to Video Implementation

### Their Project (Google Flights):
```python
# backend/flights/google_flight_scraper.py
async def scrape_flights(url, preferences):
    agent = Agent(
        task=flight_scrape_task(preferences, url),
        llm=ChatAnthropic(model="claude-3-5-sonnet-20241022"),
        initial_actions=[{"open_tab": {"url": url}}],
        browser=browser
    )
    return await agent.run()
```

### Our Implementation (Grocery Shopping):
```python
# ML/ai_grocery_agent.py
async def automate_bigbasket_shopping(ingredients):
    agent = Agent(
        task=grocery_shopping_task(ingredients, "BigBasket"),
        llm=ChatAnthropic(model="claude-3-5-sonnet-20241022"),
        initial_actions=[{"open_tab": {"url": "https://www.bigbasket.com"}}],
        browser=browser
    )
    return await agent.run()
```

**Same pattern, different domain! 🎯**

## Security Notes

### API Key Safety:
- ✅ Store in `.env` file
- ✅ Add `.env` to `.gitignore`
- ❌ Never hardcode in source code
- ❌ Never commit to GitHub

### Browser Security:
- AI agent can access any website
- Only run on trusted sites
- Monitor automation sessions
- Use separate Chrome profile (optional)

## Next Steps

1. ✅ Get API key (Anthropic or OpenAI)
2. ✅ Create `.env` file with key
3. ✅ Test with `python -c "from ai_grocery_agent import ..."`
4. ✅ Start backend: `python backend_server.py`
5. ✅ Test frontend: Click "Place Order"
6. 🎉 Watch AI agent automate shopping!

## Resources

- **browser-use docs**: https://github.com/browser-use/browser-use
- **Anthropic API**: https://docs.anthropic.com/
- **OpenAI API**: https://platform.openai.com/docs
- **Playwright**: https://playwright.dev/python/

---

**🎥 Video Reference**: https://youtu.be/G5djZjdxVvo (2:19 - AI agent automation demo)

**💡 Key Insight**: Let AI figure out HOW to interact with the page, you just tell it WHAT to do!
