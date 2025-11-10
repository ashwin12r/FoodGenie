/**
 * MealCraft AI Shopping Assistant
 * Conversational interface for smart grocery shopping
 */

// State management
let currentState = {
    selectedMeals: [],
    ingredientsList: [],
    selectedStore: null,
    totalCost: 0,
    conversation: []
};

// Store data
const availableStores = [
    {
        id: 'bigbasket',
        name: 'BigBasket',
        logo: '🛒',
        deliveryTime: '2-3 hours',
        minOrder: 100,
        discount: '10% off',
        color: 'green'
    },
    {
        id: 'zepto',
        name: 'Zepto',
        logo: '⚡',
        deliveryTime: '10 mins',
        minOrder: 0,
        discount: '₹100 off',
        color: 'purple'
    },
    {
        id: 'blinkit',
        name: 'Blinkit',
        logo: '🏃',
        deliveryTime: '15 mins',
        minOrder: 0,
        discount: 'Free delivery',
        color: 'yellow'
    },
    {
        id: 'swiggy-instamart',
        name: 'Swiggy Instamart',
        logo: '🍊',
        deliveryTime: '15-20 mins',
        minOrder: 0,
        discount: '₹75 off',
        color: 'orange'
    },
    {
        id: 'amazon-fresh',
        name: 'Amazon Fresh',
        logo: '📦',
        deliveryTime: '2 hours',
        minOrder: 0,
        discount: 'No cost EMI',
        color: 'blue'
    },
    {
        id: 'jiomart',
        name: 'JioMart',
        logo: '🔵',
        deliveryTime: 'Next day',
        minOrder: 0,
        discount: '5% cashback',
        color: 'indigo'
    }
];

/**
 * Initialize AI Shopping Assistant
 */
async function initializeAIShopping() {
    console.log('🤖 Initializing AI Shopping Assistant...');
    
    try {
        // Load today's meal plan
        await loadTodaysMealPlan();
        
        // Setup event listeners
        setupEventListeners();
        
        console.log('✅ AI Shopping Assistant ready');
    } catch (error) {
        console.error('❌ Error initializing:', error);
        addAIMessage("Sorry, I'm having trouble connecting. Please refresh the page.");
    }
}

/**
 * Load today's meal plan from localStorage or API
 */
async function loadTodaysMealPlan() {
    const mealPlanList = document.getElementById('meal-plan-list');
    
    // Try to get from localStorage first
    const savedMealPlan = localStorage.getItem('current-meal-plan');
    
    if (savedMealPlan) {
        const mealPlan = JSON.parse(savedMealPlan);
        const today = new Date().toISOString().split('T')[0];
        
        // Find today's meals
        const todaysMeals = mealPlan.meals || [];
        
        if (todaysMeals.length > 0) {
            displayMealPlan(todaysMeals);
        } else {
            // Show demo meals
            displayDemoMeals();
        }
    } else {
        // Show demo meals
        displayDemoMeals();
    }
}

/**
 * Display meal plan cards
 */
function displayMealPlan(meals) {
    const mealPlanList = document.getElementById('meal-plan-list');
    
    mealPlanList.innerHTML = meals.map((meal, index) => `
        <div class="meal-card card card-hover cursor-pointer p-4" onclick="selectMeal('${meal.name}', ${index})">
            <div class="flex items-center justify-between mb-2">
                <h3 class="font-semibold text-text-primary">${meal.name}</h3>
                <span class="text-2xl">${getMealEmoji(meal.type)}</span>
            </div>
            <p class="text-xs text-text-secondary mb-2">${meal.type || 'Main Course'}</p>
            <div class="flex items-center justify-between text-xs">
                <span class="text-text-secondary">${meal.ingredients?.split(',').length || 8} ingredients</span>
                <span class="text-primary font-medium">Click to add →</span>
            </div>
        </div>
    `).join('');
}

/**
 * Display demo meals
 */
function displayDemoMeals() {
    const demoMeals = [
        { name: 'Dal Tadka', type: 'Lunch', ingredients: 'Toor dal, onions, tomatoes, cumin, mustard seeds, curry leaves, ghee, green chilies' },
        { name: 'Aloo Paratha', type: 'Breakfast', ingredients: 'Wheat flour, potatoes, cumin powder, coriander, ghee, yogurt' },
        { name: 'Palak Paneer', type: 'Dinner', ingredients: 'Spinach, paneer, onions, tomatoes, garlic, ginger, cream, spices' }
    ];
    
    displayMealPlan(demoMeals);
}

/**
 * Get emoji for meal type
 */
function getMealEmoji(type) {
    const emojiMap = {
        'breakfast': '🌅',
        'lunch': '🌞',
        'dinner': '🌙',
        'snack': '☕'
    };
    return emojiMap[type?.toLowerCase()] || '🍽️';
}

/**
 * Select a meal and start conversation
 */
async function selectMeal(mealName, index) {
    console.log('Selected meal:', mealName);
    
    // Add to selected meals
    if (!currentState.selectedMeals.includes(mealName)) {
        currentState.selectedMeals.push(mealName);
    }
    
    // Fetch meal details
    try {
        const response = await fetch(`${mealCraftAPI.baseURL}/api/recipes/${encodeURIComponent(mealName)}`);
        const data = await response.json();
        
        if (data.success && data.recipe) {
            const ingredients = data.recipe.ingredients.split(',').map(i => i.trim());
            
            // Add user message
            addUserMessage(`I want to cook ${mealName}`);
            
            // AI thinks
            await showTypingIndicator();
            
            // AI response with ingredients
            setTimeout(() => {
                hideTypingIndicator();
                addAIMessage(`Great choice! ${mealName} requires these ingredients:`);
                
                setTimeout(() => {
                    displayIngredientsList(ingredients, mealName);
                    
                    setTimeout(() => {
                        addAIMessage(`I've prepared your shopping list with ${ingredients.length} items.`, true);
                        setTimeout(() => {
                            askToProceed(ingredients, data.recipe);
                        }, 500);
                    }, 800);
                }, 500);
            }, 1500);
        }
    } catch (error) {
        console.error('Error fetching recipe:', error);
        addAIMessage("I couldn't find the exact recipe details, but I can help you with a general ingredient list.");
    }
}

/**
 * Display ingredients as a card in chat
 */
function displayIngredientsList(ingredients, mealName) {
    const chatContainer = document.getElementById('chat-container');
    
    const ingredientsHTML = `
        <div class="message mb-4">
            <div class="flex items-start">
                <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">
                    🤖
                </div>
                <div class="ml-3 flex-1">
                    <div class="bg-gradient-to-br from-primary-50 to-secondary-50 rounded-lg rounded-tl-none shadow-md p-4 border border-primary-200">
                        <div class="flex items-center justify-between mb-3">
                            <h4 class="font-bold text-text-primary">📋 Shopping List: ${mealName}</h4>
                            <span class="text-xs bg-white px-2 py-1 rounded-full text-text-secondary">${ingredients.length} items</span>
                        </div>
                        <div class="bg-white rounded-lg p-3 max-h-48 overflow-y-auto">
                            <ul class="space-y-2">
                                ${ingredients.map((ing, idx) => `
                                    <li class="flex items-center text-sm">
                                        <span class="w-6 h-6 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-xs mr-2">✓</span>
                                        <span class="text-text-primary">${ing}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                    <p class="text-xs text-text-secondary mt-1 ml-2">Just now</p>
                </div>
            </div>
        </div>
    `;
    
    chatContainer.insertAdjacentHTML('beforeend', ingredientsHTML);
    scrollToBottom();
    
    currentState.ingredientsList = ingredients;
}

/**
 * Ask user if they want to proceed with purchase
 */
function askToProceed(ingredients, recipe) {
    const estimatedCost = ingredients.length * 35; // Rough estimate
    currentState.totalCost = estimatedCost;
    
    const chatContainer = document.getElementById('chat-container');
    
    const questionHTML = `
        <div class="message mb-4">
            <div class="flex items-start">
                <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">
                    🤖
                </div>
                <div class="ml-3 flex-1">
                    <div class="bg-white rounded-lg rounded-tl-none shadow-sm p-4">
                        <p class="text-text-primary font-medium mb-3">💰 Estimated cost: ₹${estimatedCost}</p>
                        <p class="text-text-primary mb-4">Should I proceed to buy these ingredients from an online store?</p>
                        <div class="flex space-x-3">
                            <button class="btn-primary px-6" onclick="proceedToStoreSelection()">
                                ✓ Yes, let's buy
                            </button>
                            <button class="btn-secondary px-6" onclick="declinePurchase()">
                                ✗ Not now
                            </button>
                        </div>
                    </div>
                    <p class="text-xs text-text-secondary mt-1 ml-2">Just now</p>
                </div>
            </div>
        </div>
    `;
    
    chatContainer.insertAdjacentHTML('beforeend', questionHTML);
    scrollToBottom();
}

/**
 * Proceed to store selection
 */
async function proceedToStoreSelection() {
    addUserMessage("Yes, let's buy these ingredients");
    
    await showTypingIndicator();
    
    setTimeout(() => {
        hideTypingIndicator();
        addAIMessage("Perfect! Let me show you the best stores available for quick delivery.");
        
        setTimeout(() => {
            showStoreOptions();
        }, 800);
    }, 1200);
}

/**
 * Decline purchase
 */
async function declinePurchase() {
    addUserMessage("Not right now, maybe later");
    
    await showTypingIndicator();
    
    setTimeout(() => {
        hideTypingIndicator();
        addAIMessage("No problem! Your shopping list is saved. I'll be here when you're ready to order. 😊");
        
        // Save to localStorage
        localStorage.setItem('saved-shopping-list', JSON.stringify({
            ingredients: currentState.ingredientsList,
            meals: currentState.selectedMeals,
            timestamp: new Date().toISOString()
        }));
    }, 1000);
}

/**
 * Show store selection options
 */
function showStoreOptions() {
    const storeSelection = document.getElementById('store-selection');
    const storeOptions = document.getElementById('store-options');
    
    storeOptions.innerHTML = availableStores.map(store => `
        <div class="store-card card p-4 text-center" onclick="selectStore('${store.id}')">
            <div class="text-4xl mb-2">${store.logo}</div>
            <h4 class="font-bold text-text-primary mb-1">${store.name}</h4>
            <p class="text-xs text-text-secondary mb-2">⏱️ ${store.deliveryTime}</p>
            <p class="text-xs font-medium text-green-600">${store.discount}</p>
            <button class="btn-primary w-full mt-3 text-sm">Select</button>
        </div>
    `).join('');
    
    storeSelection.classList.remove('hidden');
    
    // Scroll to store selection
    storeSelection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    addAIMessage("👆 Choose your preferred store from the options above. I've compared prices and delivery times for you!");
}

/**
 * Select a store
 */
async function selectStore(storeId) {
    const store = availableStores.find(s => s.id === storeId);
    currentState.selectedStore = store;
    
    // Visual feedback
    document.querySelectorAll('.store-card').forEach(card => {
        card.classList.remove('selected');
    });
    event.target.closest('.store-card').classList.add('selected');
    
    addUserMessage(`I choose ${store.name}`);
    
    await showTypingIndicator();
    
    setTimeout(() => {
        hideTypingIndicator();
        addAIMessage(`Excellent choice! ${store.name} offers ${store.deliveryTime} delivery. 🚚`);
        
        setTimeout(() => {
            confirmOrder(store);
        }, 1000);
    }, 1500);
}

/**
 * Confirm order
 */
function confirmOrder(store) {
    const chatContainer = document.getElementById('chat-container');
    
    const confirmHTML = `
        <div class="message mb-4">
            <div class="flex items-start">
                <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">
                    🤖
                </div>
                <div class="ml-3 flex-1">
                    <div class="bg-gradient-to-br from-green-50 to-blue-50 rounded-lg rounded-tl-none shadow-md p-4 border border-green-200">
                        <h4 class="font-bold text-text-primary mb-3">📦 Order Summary</h4>
                        <div class="bg-white rounded-lg p-3 mb-3 space-y-2 text-sm">
                            <div class="flex justify-between">
                                <span class="text-text-secondary">Store:</span>
                                <span class="font-medium">${store.logo} ${store.name}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-text-secondary">Items:</span>
                                <span class="font-medium">${currentState.ingredientsList.length} ingredients</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-text-secondary">Delivery:</span>
                                <span class="font-medium">${store.deliveryTime}</span>
                            </div>
                            <div class="flex justify-between border-t pt-2 mt-2">
                                <span class="text-text-secondary">Total:</span>
                                <span class="font-bold text-lg text-primary">₹${currentState.totalCost}</span>
                            </div>
                        </div>
                        <p class="text-sm text-text-primary mb-3">Ready to place this order?</p>
                        <div class="flex space-x-3">
                            <button class="btn-primary flex-1" onclick="placeOrder()">
                                🛒 Place Order
                            </button>
                            <button class="btn-secondary" onclick="cancelOrder()">
                                ✗ Cancel
                            </button>
                        </div>
                    </div>
                    <p class="text-xs text-text-secondary mt-1 ml-2">Just now</p>
                </div>
            </div>
        </div>
    `;
    
    chatContainer.insertAdjacentHTML('beforeend', confirmHTML);
    scrollToBottom();
}

/**
 * Place order
 */
async function placeOrder() {
    addUserMessage("Yes, place the order");
    
    await showTypingIndicator();
    
    try {
        // Call backend to automate browser
        addAIMessage("🤖 Opening browser and automating your order...");
        
        const response = await fetch('http://localhost:8000/api/automate-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                store_name: currentState.selectedStore.name,
                ingredients: currentState.ingredientsList,
                meal_name: currentState.selectedMeals[0] || "Your meal"
            })
        });
        
        const result = await response.json();
        
        hideTypingIndicator();
        
        if (result.success) {
            addAIMessage(`✅ Browser automation started! Chrome is now opening ${currentState.selectedStore.name} and adding items to your cart.`);
            
            setTimeout(() => {
                const automationResult = result.automation_result;
                const itemsAdded = automationResult.items_added || [];
                const itemsNotFound = automationResult.items_not_found || [];
                
                let statusMessage = `📦 <strong>Automation Status:</strong><br>`;
                if (itemsAdded.length > 0) {
                    statusMessage += `✅ Added ${itemsAdded.length} items: ${itemsAdded.join(', ')}<br>`;
                }
                if (itemsNotFound.length > 0) {
                    statusMessage += `⚠️ ${itemsNotFound.length} items need manual search: ${itemsNotFound.join(', ')}<br>`;
                }
                statusMessage += `<br>Please review the cart in the opened browser and proceed to checkout! 🛒`;
                
                addAIMessage(statusMessage);
            }, 2000);
            
        } else {
            addAIMessage("❌ Browser automation encountered an issue. Opening the store website for manual shopping...");
            
            // Fallback: just open the store URL
            setTimeout(() => {
                const storeUrls = {
                    'BigBasket': 'https://www.bigbasket.com',
                    'Zepto': 'https://www.zeptonow.com',
                    'Blinkit': 'https://www.blinkit.com',
                    'Swiggy Instamart': 'https://www.swiggy.com/instamart',
                    'Amazon Fresh': 'https://www.amazon.in/alm/storefront?almBrandId=QW1hem9uIEZyZXNo',
                    'JioMart': 'https://www.jiomart.com'
                };
                
                const storeUrl = storeUrls[currentState.selectedStore.name] || storeUrls['BigBasket'];
                window.open(storeUrl, '_blank');
                
                addAIMessage(`I've opened ${currentState.selectedStore.name} in a new tab. Please manually search and add these items: ${currentState.ingredientsList.join(', ')}`);
            }, 1000);
        }
        
    } catch (error) {
        hideTypingIndicator();
        console.error('Automation error:', error);
        addAIMessage("⚠️ Couldn't connect to automation service. Opening store website instead...");
        
        // Fallback: open store URL
        const storeUrls = {
            'BigBasket': 'https://www.bigbasket.com',
            'Zepto': 'https://www.zeptonow.com',
            'Blinkit': 'https://www.blinkit.com',
            'Swiggy Instamart': 'https://www.swiggy.com/instamart',
            'Amazon Fresh': 'https://www.amazon.in/alm/storefront?almBrandId=QW1hem9uIEZyZXNo',
            'JioMart': 'https://www.jiomart.com'
        };
        
        const storeUrl = storeUrls[currentState.selectedStore.name] || storeUrls['BigBasket'];
        window.open(storeUrl, '_blank');
        
        addAIMessage(`Store opened! Here's your shopping list: ${currentState.ingredientsList.join(', ')}`);
    }
}

/**
 * Cancel order
 */
function cancelOrder() {
    addUserMessage("Cancel the order");
    addAIMessage("No problem! Your shopping list is still saved if you want to order later.");
}

/**
 * Add AI message to chat
 */
function addAIMessage(message, isCard = false) {
    const chatContainer = document.getElementById('chat-container');
    
    const messageHTML = `
        <div class="message mb-4">
            <div class="flex items-start">
                <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">
                    🤖
                </div>
                <div class="ml-3 flex-1">
                    <div class="bg-white rounded-lg rounded-tl-none shadow-sm p-4">
                        <p class="text-text-primary">${message}</p>
                    </div>
                    <p class="text-xs text-text-secondary mt-1 ml-2">Just now</p>
                </div>
            </div>
        </div>
    `;
    
    chatContainer.insertAdjacentHTML('beforeend', messageHTML);
    scrollToBottom();
}

/**
 * Add user message to chat
 */
function addUserMessage(message) {
    const chatContainer = document.getElementById('chat-container');
    
    const messageHTML = `
        <div class="message mb-4">
            <div class="flex items-start justify-end">
                <div class="mr-3 flex-1 text-right">
                    <div class="bg-primary text-white rounded-lg rounded-tr-none shadow-sm p-4 inline-block">
                        <p>${message}</p>
                    </div>
                    <p class="text-xs text-text-secondary mt-1 mr-2">Just now</p>
                </div>
                <div class="w-8 h-8 bg-secondary rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">
                    👤
                </div>
            </div>
        </div>
    `;
    
    chatContainer.insertAdjacentHTML('beforeend', messageHTML);
    scrollToBottom();
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const chatContainer = document.getElementById('chat-container');
    
    const typingHTML = `
        <div class="message mb-4" id="typing-indicator">
            <div class="flex items-start">
                <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">
                    🤖
                </div>
                <div class="ml-3">
                    <div class="bg-white rounded-lg rounded-tl-none shadow-sm">
                        <div class="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    chatContainer.insertAdjacentHTML('beforeend', typingHTML);
    scrollToBottom();
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    const messageInput = document.getElementById('user-message-input');
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendUserMessage();
        }
    });
}

/**
 * Send user message
 */
function sendUserMessage() {
    const input = document.getElementById('user-message-input');
    const message = input.value.trim();
    
    if (message) {
        addUserMessage(message);
        input.value = '';
        
        // Simple response
        setTimeout(() => {
            addAIMessage("I'm here to help! Please select a meal from the left panel to start shopping.");
        }, 1000);
    }
}

// Make functions globally accessible
window.initializeAIShopping = initializeAIShopping;
window.selectMeal = selectMeal;
window.selectStore = selectStore;
window.proceedToStoreSelection = proceedToStoreSelection;
window.declinePurchase = declinePurchase;
window.placeOrder = placeOrder;
window.cancelOrder = cancelOrder;
window.sendUserMessage = sendUserMessage;
