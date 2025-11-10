/**
 * MealCraft Meal Planner Integration
 * Connects meal planner page to backend API
 * 
 * Add this script to mealplanner.html:
 * <script src="api-client.js"></script>
 * <script src="meal-planner-integration.js"></script>
 */

// User email from localStorage (set during onboarding)
let userEmail = localStorage.getItem('user-email') || 'guest@mealcraft.com';

// Store meal plans by week (key: week start date, value: meal plan data)
let weeklyMealPlans = {};

/**
 * Initialize meal planner with API
 */
async function initializeMealPlanner() {
    console.log('🚀 Initializing MealCraft Meal Planner...');
    
    try {
        // Check API health
        const health = await mealCraftAPI.healthCheck();
        console.log('✅ Backend API connected:', health);
        
        // Load weekly meal plans from localStorage
        loadWeeklyMealPlansFromStorage();
        
        // Display current week's meal plan if available
        displayCurrentWeekMealPlan();
        
        // Load user's existing meal plans
        await loadUserMealPlans();
        
    } catch (error) {
        console.error('❌ Backend API not available:', error);
        console.log('ℹ️ Using demo mode with mock data');
    }
}

/**
 * Load user's meal plans from database
 */
async function loadUserMealPlans() {
    try {
        const response = await mealCraftAPI.getUserMealPlans(userEmail, 5);
        console.log('📋 Loaded meal plans:', response);
        
        if (response.meal_plans && response.meal_plans.length > 0) {
            // Display the most recent meal plan
            const latestPlan = response.meal_plans[0];
            displayMealPlan(latestPlan.plan_data);
        } else {
            console.log('No existing meal plans found');
        }
    } catch (error) {
        console.error('Error loading meal plans:', error);
    }
}

/**
 * Generate new meal plan using AI
 */
async function generateNewMealPlan() {
    console.log('🤖 Generating AI-powered meal plan...');
    
    // Show loading state
    showLoading('Generating your personalized meal plan...');
    
    try {
        // Get user preferences from localStorage or use defaults
        const preferences = getUserPreferences();
        
        // Call API to generate meal plan
        const response = await mealCraftAPI.generateMealPlan(userEmail, {
            email: userEmail,
            ...preferences
        });
        
        console.log('✅ Meal plan generated:', response);
        
        // Display the meal plan
        if (response.meal_plan) {
            displayMealPlan(response.meal_plan);
            
            // Save meal plan for current week
            const weekKey = getCurrentWeekKey();
            weeklyMealPlans[weekKey] = response.meal_plan;
            saveWeeklyMealPlansToStorage();
            console.log(`💾 Saved meal plan for week ${weekKey}`);
            
            // Save meal plan ID for later use
            localStorage.setItem('current-meal-plan-id', response.meal_plan_id);
            
            // Show success message
            showSuccess('Meal plan generated successfully!');
        }
        
        hideLoading();
        
    } catch (error) {
        console.error('❌ Error generating meal plan:', error);
        showError('Failed to generate meal plan. Please try again.');
        hideLoading();
    }
}

/**
 * Get user preferences from localStorage
 */
function getUserPreferences() {
    console.log('📋 Getting user preferences from form...');
    
    // Get dietary preferences
    const dietaryPrefs = Array.from(document.querySelectorAll('.dietary-pref:checked'))
        .map(cb => cb.value);
    const primaryDiet = dietaryPrefs.length > 0 ? dietaryPrefs[0].toLowerCase() : 'vegetarian';
    
    // Get cuisine preferences
    const cuisinePrefs = Array.from(document.querySelectorAll('.cuisine-pref:checked'))
        .map(cb => cb.value);
    
    // Get flavor preferences
    const flavorPrefs = Array.from(document.querySelectorAll('.flavor-pref:checked'))
        .map(cb => cb.value);
    
    // Get health goal
    const healthGoalElement = document.querySelector('.health-goal:checked');
    const healthGoal = healthGoalElement ? healthGoalElement.value : 'balanced';
    
    // Get cooking time
    const cookingTime = parseInt(document.getElementById('cooking-time-input')?.value || '30');
    
    // Get calorie target
    const calorieTarget = parseInt(document.getElementById('calorie-target-input')?.value || '2000');
    
    // Get budget
    const weeklyBudget = parseFloat(document.getElementById('budget-input')?.value || '1240');
    
    // Get cost per meal
    const costPerMeal = parseFloat(document.getElementById('cost-per-meal-input')?.value || '65');
    
    const preferences = {
        diet: primaryDiet,
        preferred_cuisines: cuisinePrefs.length > 0 ? cuisinePrefs : ['North Indian'],
        daily_calorie_target: calorieTarget,
        weekly_budget: weeklyBudget,
        cooking_time_limit: cookingTime,
        cost_per_meal_limit: costPerMeal,
        preferred_flavors: flavorPrefs.length > 0 ? flavorPrefs : ['spicy'],
        region: 'All',
        goals: [healthGoal]
    };
    
    console.log('✅ User preferences:', preferences);
    return preferences;
}

/**
 * Display meal plan on the page
 */
function displayMealPlan(mealPlan) {
    console.log('📊 Displaying meal plan:', mealPlan);
    
    // Extract weekly plan data
    const weeklyPlan = mealPlan.weekly_plan || [];
    const summary = mealPlan.summary || {};
    
    // Update summary statistics
    updateSummaryStats(summary);
    
    // Update meal cards for each day
    updateMealCards(weeklyPlan);
    
    // Update shopping list
    if (mealPlan.shopping_list) {
        updateShoppingList(mealPlan.shopping_list);
    }
}

/**
 * Update summary statistics
 */
function updateSummaryStats(summary) {
    console.log('📈 Updating summary stats:', summary);
    
    // Update weekly budget display
    const budgetElement = document.getElementById('weekly-budget-display');
    if (budgetElement && summary.total_cost) {
        budgetElement.textContent = summary.total_cost;
    }
    
    // Update nutrition goals display (calorie accuracy)
    const nutritionElement = document.getElementById('nutrition-goals-display');
    if (nutritionElement && summary.calorie_balance_accuracy) {
        nutritionElement.textContent = summary.calorie_balance_accuracy;
    }
    
    console.log('✅ Summary stats updated');
}

/**
 * Update meal cards for the week
 */
function updateMealCards(weeklyPlan) {
    console.log('🔄 Updating meal cards with plan:', weeklyPlan);
    
    // weeklyPlan is an array of day objects
    weeklyPlan.forEach((dayPlan) => {
        const dayName = dayPlan.day.toLowerCase(); // "Monday" -> "monday"
        const meals = dayPlan.meals; // {breakfast: {...}, lunch: {...}, dinner: {...}}
        
        if (meals) {
            // Update each meal type
            if (meals.breakfast) updateMealSlot(dayName, 'breakfast', meals.breakfast);
            if (meals.lunch) updateMealSlot(dayName, 'lunch', meals.lunch);
            if (meals.dinner) updateMealSlot(dayName, 'dinner', meals.dinner);
        }
    });
}

/**
 * Update individual meal slot
 */
function updateMealSlot(day, mealType, mealData) {
    console.log(`📍 Updating ${day} ${mealType}:`, mealData);
    
    // Find all meal slots for this day and meal type using onclick attribute
    const allMealSlots = document.querySelectorAll('.meal-slot');
    let targetSlot = null;
    
    for (const slot of allMealSlots) {
        const onclick = slot.getAttribute('onclick');
        if (onclick && onclick.includes(`'${day}'`) && onclick.includes(`'${mealType}'`)) {
            targetSlot = slot;
            break;
        }
    }
    
    if (targetSlot && mealData) {
        // Replace the "+ Add Meal" placeholder with actual meal data
        targetSlot.innerHTML = `
            <div class="text-xs font-medium text-neutral-500 mb-1">${mealType.charAt(0).toUpperCase() + mealType.slice(1)}</div>
            <div class="text-sm font-semibold text-text-primary mb-1">${mealData.dish}</div>
            <div class="flex items-center justify-between text-xs">
                <span class="text-primary font-semibold">${mealData.cost}</span>
                <span class="text-text-secondary">${mealData.time}</span>
            </div>
            <div class="text-xs text-text-secondary mt-1">${mealData.calories}</div>
        `;
        
        // Change styling from dashed border to solid
        targetSlot.classList.remove('border-dashed', 'border-neutral-200');
        targetSlot.classList.add('border-solid', 'border-primary-200', 'bg-primary-50');
        
        console.log(`✅ Updated ${day} ${mealType} successfully`);
    } else {
        console.warn(`⚠️ Could not find slot for ${day} ${mealType}`);
    }
}

/**
 * Update shopping list
 */
function updateShoppingList(shoppingList) {
    console.log('🛒 Updating shopping list:', shoppingList);
    // Shopping list can be displayed in smart shopping page
    localStorage.setItem('current-shopping-list', JSON.stringify(shoppingList));
}

/**
 * UI Helper Functions
 */
function showLoading(message = 'Loading...') {
    // Add loading indicator to page
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
 * Get current week key (Monday's date as string)
 */
function getCurrentWeekKey() {
    // Get the current week offset from mealplanner.html
    const weekOffset = window.currentWeekOffset || 0;
    const monday = getMondayOfWeek(weekOffset);
    return monday.toISOString().split('T')[0]; // Format: YYYY-MM-DD
}

/**
 * Load weekly meal plans from localStorage
 */
function loadWeeklyMealPlansFromStorage() {
    const stored = localStorage.getItem('weekly-meal-plans');
    if (stored) {
        try {
            weeklyMealPlans = JSON.parse(stored);
            console.log('📅 Loaded weekly meal plans from storage:', Object.keys(weeklyMealPlans));
        } catch (error) {
            console.error('Error parsing stored meal plans:', error);
            weeklyMealPlans = {};
        }
    }
}

/**
 * Save weekly meal plans to localStorage
 */
function saveWeeklyMealPlansToStorage() {
    try {
        localStorage.setItem('weekly-meal-plans', JSON.stringify(weeklyMealPlans));
        console.log('💾 Saved weekly meal plans to storage');
    } catch (error) {
        console.error('Error saving meal plans:', error);
    }
}

/**
 * Display current week's meal plan if available
 */
function displayCurrentWeekMealPlan() {
    const weekKey = getCurrentWeekKey();
    const mealPlan = weeklyMealPlans[weekKey];
    
    if (mealPlan) {
        console.log(`📅 Displaying meal plan for week ${weekKey}`);
        displayMealPlan(mealPlan);
    } else {
        console.log(`📅 No meal plan found for week ${weekKey}, clearing calendar`);
        clearCalendar();
    }
}

// Make function globally accessible
window.displayCurrentWeekMealPlan = displayCurrentWeekMealPlan;

/**
 * Clear all meals from calendar
 */
function clearCalendar() {
    const allMealSlots = document.querySelectorAll('.meal-slot');
    allMealSlots.forEach(slot => {
        // Reset to empty state
        slot.innerHTML = `
            <div class="text-xs font-medium text-neutral-500 mb-1">${slot.querySelector('.text-xs')?.textContent || 'Meal'}</div>
            <div class="text-sm text-neutral-400">+ Add Meal</div>
        `;
        // Reset styling
        slot.className = slot.className.replace(/border-solid|border-primary-200|bg-primary-50/g, '');
        if (!slot.className.includes('border-dashed')) {
            slot.classList.add('border-dashed');
        }
        if (!slot.className.includes('border-neutral-200')) {
            slot.classList.add('border-neutral-200');
        }
    });
    
    // Clear summary stats
    document.getElementById('weekly-budget-display').textContent = '₹0';
    document.getElementById('nutrition-goals-display').textContent = '0%';
}

/**
 * Add event listeners
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize on page load
    initializeMealPlanner();
    
    // Add generate button listener if it exists
    const generateButton = document.querySelector('[onclick*="generate"]') || 
                          document.querySelector('button[type="submit"]');
    
    if (generateButton) {
        generateButton.addEventListener('click', (e) => {
            e.preventDefault();
            generateNewMealPlan();
        });
    }
    
    // Add refresh button
    const refreshButton = document.getElementById('refresh-meal-plan');
    if (refreshButton) {
        refreshButton.addEventListener('click', generateNewMealPlan);
    }
});

// Export functions for global use
window.MealPlannerAPI = {
    generateNewMealPlan,
    loadUserMealPlans,
    displayMealPlan
};
