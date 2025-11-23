"""
Quick test script to verify AI Agent setup
Run this to check if everything is configured correctly
"""

import os
import sys
from dotenv import load_dotenv

print("🔍 Checking AI Agent Setup...\n")

# 1. Check .env file
load_dotenv()
print("📄 .env file loading... ", end="")
if os.path.exists(".env"):
    print("✅ Found")
else:
    print("⚠️  Not found - please create from .env.template")

# 2. Check API keys
print("\n🔑 API Keys:")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
    print(f"  ✅ ANTHROPIC_API_KEY: {anthropic_key[:10]}...{anthropic_key[-4:]}")
elif openai_key and openai_key != "your_openai_api_key_here":
    print(f"  ✅ OPENAI_API_KEY: {openai_key[:10]}...{openai_key[-4:]}")
else:
    print("  ❌ No valid API key found!")
    print("  📝 Please add your API key to .env file:")
    print("     ANTHROPIC_API_KEY=sk-ant-...")
    print("     OR")
    print("     OPENAI_API_KEY=sk-proj-...")
    print("\n  Get keys from:")
    print("     - Anthropic: https://console.anthropic.com/")
    print("     - OpenAI: https://platform.openai.com/api-keys")
    sys.exit(1)

# 3. Check browser-use
print("\n📦 Dependencies:")
try:
    import browser_use
    print("  ✅ browser-use: installed")
except ImportError:
    print("  ❌ browser-use not installed")
    print("     Run: pip install browser-use")
    sys.exit(1)

# 4. Check Playwright
try:
    from playwright.sync_api import sync_playwright
    print("  ✅ playwright: installed")
except ImportError:
    print("  ❌ playwright not installed")
    print("     Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# 5. Check AI model
print("\n🤖 AI Model:")
try:
    if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
        from langchain_anthropic import ChatAnthropic
        model = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
        print("  ✅ Claude 3.5 Sonnet (Anthropic)")
    else:
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o", temperature=0)
        print("  ✅ GPT-4o (OpenAI)")
except Exception as e:
    print(f"  ❌ Error initializing model: {e}")
    sys.exit(1)

# 6. Check Chrome
print("\n🌐 Browser:")
chrome_paths = [
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
]

chrome_found = False
for path in chrome_paths:
    if os.path.exists(path):
        print(f"  ✅ Chrome found at: {path}")
        chrome_found = True
        break

if not chrome_found:
    print("  ⚠️  Chrome not found at default locations")
    print("     Update chrome_instance_path in ai_grocery_agent.py")

# 7. Summary
print("\n" + "="*50)
print("✅ Setup Complete!")
print("="*50)
print("\n📚 Next Steps:")
print("  1. Start backend: python backend_server.py")
print("  2. Open: smart-shopping-ai.html")
print("  3. Click 'Place Order' on a meal")
print("  4. Watch AI agent automate shopping! 🤖")
print("\n📖 Read AI_AGENT_SETUP.md for detailed instructions")
