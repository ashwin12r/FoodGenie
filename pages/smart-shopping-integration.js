/**
 * MealCraft Smart Shopping Integration
 * Connects smart shopping page to grocery price API
 * 
 * Add this script to smartshopping.html:
 * <script src="api-client.js"></script>
 * <script src="smart-shopping-integration.js"></script>
 */

// Available stores
const STORES = ['Grace Daily', 'KPN Fresh'];

/**
 * Initialize smart shopping with API
 */
async function initializeSmartShopping() {
    console.log('🛒 Initializing Smart Shopping...');
    
    try {
        // Check API health
        const health = await mealCraftAPI.healthCheck();
        console.log('✅ Backend API connected:', health);
        
        // Load grocery prices
        await loadGroceryPrices();
        
        // Load shopping list from meal plan
        await loadShoppingList();
        
    } catch (error) {
        console.error('❌ Backend API not available:', error);
        console.log('ℹ️ Using demo mode with mock data');
    }
}

/**
 * Load grocery prices from database
 */
async function loadGroceryPrices(store = null) {
    try {
        console.log('📊 Loading grocery prices...');
        showLoading('Loading grocery prices...');
        
        const response = await mealCraftAPI.getGroceryPrices(store);
        console.log('✅ Loaded prices:', response);
        
        if (response.prices && response.prices.length > 0) {
            displayGroceryPrices(response.prices);
        } else {
            console.log('No prices available. Consider scraping stores.');
            showEmptyState();
        }
        
        hideLoading();
        
    } catch (error) {
        console.error('Error loading grocery prices:', error);
        hideLoading();
        showError('Failed to load grocery prices');
    }
}

/**
 * Scrape grocery prices from stores
 */
async function scrapeGroceryPrices() {
    try {
        console.log('🕷️ Starting web scraping...');
        showLoading('Scraping grocery prices from stores... This may take a few minutes.');
        
        const response = await mealCraftAPI.scrapeGroceryPrices(STORES);
        console.log('✅ Scraping complete:', response);
        
        showSuccess(`Successfully scraped ${response.prices_updated} items!`);
        
        // Reload prices
        await loadGroceryPrices();
        
        hideLoading();
        
    } catch (error) {
        console.error('Error scraping prices:', error);
        hideLoading();
        showError('Failed to scrape grocery prices. Using cached data.');
    }
}

/**
 * Compare prices for a specific item
 */
async function compareItemPrices(itemName) {
    try {
        console.log(`🔍 Comparing prices for: ${itemName}`);
        
        const response = await mealCraftAPI.comparePrices(itemName);
        console.log('💰 Price comparison:', response);
        
        displayPriceComparison(response);
        
    } catch (error) {
        console.error('Error comparing prices:', error);
        showError(`Item "${itemName}" not found in any store`);
    }
}

/**
 * Load shopping list from current meal plan
 */
async function loadShoppingList() {
    try {
        // Check if there's a shopping list in localStorage
        const storedList = localStorage.getItem('current-shopping-list');
        
        if (storedList) {
            const shoppingList = JSON.parse(storedList);
            displayShoppingList(shoppingList);
        } else {
            console.log('No shopping list available. Generate a meal plan first.');
        }
        
    } catch (error) {
        console.error('Error loading shopping list:', error);
    }
}

/**
 * Display grocery prices on the page
 */
function displayGroceryPrices(prices) {
    console.log('📋 Displaying grocery prices...');
    
    // Group prices by store
    const pricesByStore = {};
    prices.forEach(item => {
        if (!pricesByStore[item.store_name]) {
            pricesByStore[item.store_name] = [];
        }
        pricesByStore[item.store_name].push(item);
    });
    
    // Update price tables for each store
    Object.keys(pricesByStore).forEach(storeName => {
        updateStoreTable(storeName, pricesByStore[storeName]);
    });
    
    // Update summary
    updatePriceSummary(prices);
}

/**
 * Update price table for a specific store
 */
function updateStoreTable(storeName, items) {
    // Find or create table for this store
    let table = document.querySelector(`[data-store="${storeName}"]`);
    
    if (!table) {
        // Create table if it doesn't exist
        const container = document.getElementById('price-tables') || document.querySelector('main');
        if (container) {
            const tableHTML = createStoreTable(storeName, items);
            container.insertAdjacentHTML('beforeend', tableHTML);
        }
    } else {
        // Update existing table
        const tbody = table.querySelector('tbody');
        if (tbody) {
            tbody.innerHTML = items.map(item => createTableRow(item)).join('');
        }
    }
}

/**
 * Create table HTML for a store
 */
function createStoreTable(storeName, items) {
    return `
        <div class="card mb-6" data-store="${storeName}">
            <div class="p-6">
                <h3 class="text-xl font-bold text-text-primary mb-4">
                    ${storeName}
                    <span class="text-sm font-normal text-text-secondary ml-2">
                        (${items.length} items)
                    </span>
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead>
                            <tr class="border-b border-neutral-200">
                                <th class="text-left py-2">Item</th>
                                <th class="text-left py-2">Price</th>
                                <th class="text-left py-2">Unit</th>
                                <th class="text-left py-2">Status</th>
                                <th class="text-right py-2">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${items.map(item => createTableRow(item)).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

/**
 * Create table row for an item
 */
function createTableRow(item) {
    const statusClass = item.in_stock ? 'text-success' : 'text-error';
    const statusText = item.in_stock ? 'In Stock' : 'Out of Stock';
    
    return `
        <tr class="border-b border-neutral-100">
            <td class="py-3">${item.item_name}</td>
            <td class="py-3 font-semibold text-primary">₹${item.price}</td>
            <td class="py-3 text-text-secondary">${item.unit || 'unit'}</td>
            <td class="py-3"><span class="${statusClass}">${statusText}</span></td>
            <td class="py-3 text-right">
                <button 
                    onclick="compareItemPrices('${item.item_name}')"
                    class="text-primary hover:text-primary-700 text-sm"
                >
                    Compare
                </button>
            </td>
        </tr>
    `;
}

/**
 * Display shopping list from meal plan
 */
function displayShoppingList(shoppingList) {
    console.log('📝 Displaying shopping list:', shoppingList);
    
    const listContainer = document.getElementById('shopping-list-container');
    if (!listContainer) return;
    
    let html = '<div class="card p-6"><h3 class="text-xl font-bold mb-4">Your Shopping List</h3><ul class="space-y-2">';
    
    shoppingList.forEach(item => {
        html += `
            <li class="flex justify-between items-center py-2 border-b">
                <span>${item.name || item.item}</span>
                <span class="text-text-secondary">${item.quantity || item.amount}</span>
            </li>
        `;
    });
    
    html += '</ul></div>';
    listContainer.innerHTML = html;
}

/**
 * Display price comparison modal
 */
function displayPriceComparison(comparison) {
    const modal = createPriceComparisonModal(comparison);
    document.body.insertAdjacentHTML('beforeend', modal);
}

/**
 * Create price comparison modal HTML
 */
function createPriceComparisonModal(comparison) {
    const stores = comparison.stores || [];
    const bestPrice = comparison.best_price;
    
    return `
        <div id="price-comparison-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onclick="closeComparisonModal()">
            <div class="bg-white rounded-lg p-8 max-w-2xl w-full mx-4" onclick="event.stopPropagation()">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-2xl font-bold text-text-primary">
                        Price Comparison: ${comparison.item}
                    </h3>
                    <button onclick="closeComparisonModal()" class="text-text-secondary hover:text-text-primary">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
                
                ${bestPrice ? `
                    <div class="bg-success-50 border border-success-200 rounded-lg p-4 mb-6">
                        <div class="flex items-center">
                            <svg class="w-6 h-6 text-success mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>
                            </svg>
                            <div>
                                <p class="font-semibold text-success">Best Price: ₹${bestPrice.price}</p>
                                <p class="text-sm text-success-700">at ${bestPrice.store_name}</p>
                            </div>
                        </div>
                    </div>
                ` : ''}
                
                <div class="space-y-3">
                    ${stores.map((store, index) => `
                        <div class="flex justify-between items-center p-4 border rounded-lg ${index === 0 ? 'border-success-300 bg-success-50' : 'border-neutral-200'}">
                            <div>
                                <p class="font-semibold">${store.store_name}</p>
                                <p class="text-sm text-text-secondary">${store.in_stock ? 'In Stock' : 'Out of Stock'}</p>
                            </div>
                            <div class="text-right">
                                <p class="text-2xl font-bold text-primary">₹${store.price}</p>
                                <p class="text-sm text-text-secondary">${store.unit}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <div class="mt-6 flex justify-end">
                    <button onclick="closeComparisonModal()" class="btn-primary">
                        Close
                    </button>
                </div>
            </div>
        </div>
    `;
}

/**
 * Close comparison modal
 */
function closeComparisonModal() {
    const modal = document.getElementById('price-comparison-modal');
    if (modal) {
        modal.remove();
    }
}

/**
 * Update price summary
 */
function updatePriceSummary(prices) {
    const summary = {
        totalItems: prices.length,
        stores: [...new Set(prices.map(p => p.store_name))].length,
        inStock: prices.filter(p => p.in_stock).length
    };
    
    // Update summary elements if they exist
    const itemCountElement = document.getElementById('total-items');
    if (itemCountElement) {
        itemCountElement.textContent = summary.totalItems;
    }
    
    const storeCountElement = document.getElementById('total-stores');
    if (storeCountElement) {
        storeCountElement.textContent = summary.stores;
    }
}

/**
 * Show empty state
 */
function showEmptyState() {
    const container = document.getElementById('price-tables') || document.querySelector('main');
    if (container) {
        container.innerHTML = `
            <div class="text-center py-12">
                <p class="text-text-secondary mb-4">No grocery prices available yet.</p>
                <button onclick="scrapeGroceryPrices()" class="btn-primary">
                    Scrape Stores Now
                </button>
            </div>
        `;
    }
}

/**
 * UI Helper Functions
 */
function showLoading(message = 'Loading...') {
    const loader = document.createElement('div');
    loader.id = 'api-loader';
    loader.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    loader.innerHTML = `
        <div class="bg-white rounded-lg p-8 max-w-md">
            <div class="spinner mb-4"></div>
            <p class="text-text-primary text-center">${message}</p>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.getElementById('api-loader');
    if (loader) {
        loader.remove();
    }
}

function showSuccess(message) {
    alert(message); // Replace with better toast notification
}

function showError(message) {
    alert(message); // Replace with better toast notification
}

/**
 * Add event listeners
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize on page load
    initializeSmartShopping();
    
    // Add scrape button listener
    const scrapeButton = document.getElementById('scrape-prices-btn');
    if (scrapeButton) {
        scrapeButton.addEventListener('click', scrapeGroceryPrices);
    }
    
    // Add store filter listeners
    const storeFilters = document.querySelectorAll('[data-store-filter]');
    storeFilters.forEach(filter => {
        filter.addEventListener('click', () => {
            const store = filter.dataset.storeFilter;
            loadGroceryPrices(store === 'all' ? null : store);
        });
    });
});

// Export functions for global use
window.SmartShoppingAPI = {
    loadGroceryPrices,
    scrapeGroceryPrices,
    compareItemPrices,
    loadShoppingList
};
