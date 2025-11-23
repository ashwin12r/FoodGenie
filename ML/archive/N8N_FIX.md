# Quick Fix for n8n SSL Issue

## Problem
The HTTP Request node in n8n is having SSL issues even with "Ignore SSL" enabled.

## Solution: Use Code Node Instead

Replace the HTTP Request nodes (BIGBASKET, ZEPTO, SWIGGY) with **Code** nodes:

### 1. Delete BIGBASKET, ZEPTO, SWIGGY HTTP nodes

### 2. Add a single "Scrape All Stores" Code node

**Position**: Between "Loop Items" and "Calculate Average"

**Code**:
```javascript
const item = $input.item.json.item_name;
const location = $input.item.json.location;

// Bright Data proxy
const proxy = 'http://brd-customer-hl_dde66e96-zone-webscrape:18y4rj198mpn@brd.superproxy.io:33335';

// Use axios with proxy
const axios = require('axios');
const HttpsProxyAgent = require('https-proxy-agent');

const agent = new HttpsProxyAgent(proxy);

const stores = [
  { name: 'bigbasket', url: `https://www.bigbasket.com/ps/?q=${item}` },
  { name: 'zepto', url: `https://www.zeptonow.com/search?query=${item}` },
  { name: 'swiggy', url: `https://www.swiggy.com/instamart/search?query=${item}` }
];

const results = [];

for (const store of stores) {
  try {
    const response = await axios.get(store.url, {
      httpsAgent: agent,
      timeout: 30000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    results.push({
      store: store.name,
      html: response.data,
      status: response.status
    });
  } catch (error) {
    results.push({
      store: store.name,
      error: error.message,
      status: 'failed'
    });
  }
}

return [{
  json: {
    item: item,
    results: results
  }
}];
```

### 3. Update "Calculate Average" code

```javascript
const data = $input.item.json;
const item = data.item;
const results = data.results || [];

const prices = [];

// Extract prices from each store's HTML
for (const result of results) {
  if (result.html) {
    const html = String(result.html);
    
    // Price patterns
    const patterns = [
      /₹\s*(\d+(?:,\d{3})*(?:\.\d{2})?)/g,
      /Rs\s*(\d+(?:,\d{3})*(?:\.\d{2})?)/g,
      /"price":\s*(\d+(?:\.\d{2})?)/g,
      /"mrp":\s*(\d+(?:\.\d{2})?)/g
    ];
    
    for (const pattern of patterns) {
      const matches = html.matchAll(pattern);
      for (const match of matches) {
        const price = parseFloat(match[1].replace(/,/g, ''));
        if (price > 0 && price < 10000) {
          prices.push(price);
          break;
        }
      }
      if (prices.length > 0) break;
    }
  }
}

const avgPrice = prices.length > 0 
  ? prices.reduce((a, b) => a + b, 0) / prices.length 
  : null;

return [{
  json: {
    item: item,
    price: avgPrice,
    sources: prices.length,
    raw_prices: prices
  }
}];
```

## Alternative: Simpler HTTP Request Fix

If Code node doesn't work, try this in BIGBASKET node:

1. **Delete the node completely**
2. **Add it fresh**
3. **Before adding options, save the basic config first**
4. **Then add options one by one**

## Why This Happens

n8n's HTTP Request node sometimes doesn't properly handle proxy + SSL together. The Code node gives you more control.
