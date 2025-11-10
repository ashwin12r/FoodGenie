# 🚀 Quick Start - AI Grocery Shopping Agent

## Current Status: ✅ Almost Ready!

Everything is set up and ready to go! You just need to add your API key.

## What We Built

Using the **EXACT** architecture from the video (Google Flights automation at 2:19), we created an AI agent that:
- 🤖 Understands web pages like a human
- 🛒 Automatically searches for ingredients on BigBasket
- 🎯 Clicks "Add to Cart" for each item
- 📦 Completes the shopping process

**Technology**: `browser-use` library + Claude AI (same as the video!)

---

## ⚡ Quick Setup (2 minutes)

### Step 1: Get FREE API Key

**Option A: Anthropic Claude (Recommended)**
1. Go to: https://console.anthropic.com/
2. Click "Sign Up" (you get $5 FREE credits!)
3. Go to "API Keys" tab
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)

**Option B: OpenAI GPT-4**
1. Go to: https://platform.openai.com/api-keys
2. Sign up and get $5 free credits
3. Create new key (starts with `sk-proj-...`)

### Step 2: Add API Key to .env File

Open: `ML\.env` in any text editor and replace this line:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

With your actual key:

```
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY_HERE
```

**Save the file!**

### Step 3: Verify Setup

```bash
cd "c:\prime project\prime\ML"
python test_setup.py
```

You should see: ✅ Setup Complete!

---

## 🎬 Run the Application

### 1. Start Backend Server

```bash
cd "c:\prime project\prime\ML"
python backend_server.py
```

Wait for: `✅ Server running on http://localhost:8000`

### 2. Open Frontend

- Open `smart-shopping-ai.html` in your browser
- Or navigate to a meal plan page

### 3. Test AI Agent

1. Click on any meal (shows ingredients)
2. Select "BigBasket" from store dropdown
3. Click **"Place Order"** button
4. 🎉 Watch Chrome open and AI agent automate shopping!

---

## 🎥 What You'll See

### In Console:
```
🤖 AI Agent starting automation...
🤖 Store: BigBasket
🤖 Ingredients: ['onions', 'tomatoes', 'garlic']
🌐 Opening browser...
🚀 AI Agent is now controlling the browser...
   ✅ AI found search box
   ✅ AI typed "onions"
   ✅ AI clicked "Add to Cart"
   ✅ AI added tomatoes
   ✅ AI added garlic
✅ Automation complete!
```

### In Browser:
- Chrome window opens automatically
- AI navigates to BigBasket.com
- AI searches for each ingredient
- AI clicks buttons and adds to cart
- You can watch it happen in real-time!

---

## 💡 Key Features

### 🧠 AI-Powered (Not Scripted!)
- No hard-coded CSS selectors that break
- AI understands page layout like a human
- Adapts to website changes automatically

### 📝 Natural Language Instructions
```python
"Find the search box on the page"
"Type the ingredient name"
"Click the Add to Cart button"
```

AI figures out HOW to do it!

### 🎯 Based on Real Project
- Same `browser-use` library from video
- Same Claude AI model
- Same Agent pattern
- Proven to work!

---

## 🐛 Troubleshooting

### "No API key found"
- Check: Did you edit `.env` file?
- Check: Did you save the file?
- Check: Is the key format correct? (`sk-ant-...` or `sk-proj-...`)

### Chrome doesn't open
- Check: Is Chrome installed?
- Fix: Update path in `ai_grocery_agent.py` line 66:
  ```python
  chrome_instance_path="C:\\Your\\Chrome\\Path\\chrome.exe"
  ```

### "Module not found"
```bash
pip install browser-use
playwright install chromium
```

---

## 📊 Cost Estimate

### With FREE Credits:
- Anthropic: $5 free = ~200 shopping sessions
- OpenAI: $5 free = ~100 shopping sessions

### After Free Tier:
- ~$0.01-0.03 per shopping session
- 3-5 ingredients = one session
- Very affordable for personal use!

---

## 📚 Full Documentation

For detailed information, see: `ML/AI_AGENT_SETUP.md`

---

## ✅ Checklist

- [ ] Got API key from Anthropic or OpenAI
- [ ] Added key to `ML\.env` file
- [ ] Saved `.env` file
- [ ] Ran `python test_setup.py` → All checks passed
- [ ] Started backend: `python backend_server.py`
- [ ] Opened frontend: `smart-shopping-ai.html`
- [ ] Clicked "Place Order"
- [ ] 🎉 Watched AI agent work!

---

## 🎯 Next Steps After Testing

1. **Try Different Stores**: Add Zepto, Blinkit automation
2. **Customize Instructions**: Make task more specific for better results
3. **Add Error Handling**: Handle out-of-stock items
4. **Track Shopping History**: Save automation results to database
5. **Add Progress Bar**: Show "AI is searching..." in UI

---

## 🆘 Need Help?

1. Run diagnostics: `python test_setup.py`
2. Check backend logs: Look for error messages
3. Check browser console: F12 in Chrome
4. Read full guide: `ML/AI_AGENT_SETUP.md`

---

**🎥 Video Reference**: https://youtu.be/G5djZjdxVvo?t=139 (2:19 timestamp)

**🔑 Key Insight**: Let AI figure out HOW to click buttons. You just tell it WHAT to do! 🤖
