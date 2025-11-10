/**
 * MealCraft Onboarding Integration
 * Saves user data to Neon PostgreSQL database via API
 * 
 * Add this script to onboarding.html:
 * <script src="api-client.js"></script>
 * <script src="onboarding-integration.js"></script>
 */

/**
 * Save user profile to database
 */
async function saveUserToDatabase(formData) {
    try {
        console.log('💾 Saving user profile to database...', formData);
        
        // 1. Create user account
        const userData = {
            email: formData.email || `user_${Date.now()}@mealcraft.com`,
            user_name: formData.userName || 'User',
            family_size: 1, // Single person
            city: formData.city || 'mumbai'
        };
        
        const userResponse = await mealCraftAPI.createUser(userData);
        console.log('✅ User created:', userResponse);
        
        // Store email for future use
        localStorage.setItem('user-email', userData.email);
        
        // 2. Save user preferences
        const preferences = {
            email: userData.email,
            diet: mapDietaryToBackend(formData.dietary),
            preferred_cuisines: Array.isArray(formData.cuisine) 
                ? formData.cuisine 
                : [formData.cuisine || 'North Indian'],
            dietary_restrictions: Array.isArray(formData.dietary) 
                ? formData.dietary 
                : (formData.dietary ? [formData.dietary] : []),
            cooking_time_limit: parseInt(formData.cookingTime) || 45,
            cooking_complexity: formData.cookingComplexity || 'intermediate',
            daily_calorie_target: 2000, // Default, can be calculated based on family size
            weekly_budget: parseFloat(formData.budget) || 15000,
            health_goals: Array.isArray(formData.healthGoal) 
                ? formData.healthGoal 
                : (formData.healthGoal ? [formData.healthGoal] : []),
            preferred_flavors: ['spicy', 'mild'], // Default flavors
            region: mapCuisineToRegion(formData.cuisine),
            cost_per_meal_limit: Math.round((parseFloat(formData.budget) || 15000) / 21) // budget / 21 meals
        };
        
        console.log('📤 Sending preferences to API:', preferences);
        
        const prefsResponse = await mealCraftAPI.savePreferences(preferences);
        console.log('✅ Preferences saved:', prefsResponse);
        
        return {
            success: true,
            email: userData.email,
            message: 'Profile saved successfully'
        };
        
    } catch (error) {
        console.error('❌ Error saving to database:', error);
        
        // Log detailed error if available
        if (error.response) {
            console.error('API Response:', await error.response.text());
        }
        
        // Fallback: Still save to localStorage even if API fails
        console.log('⚠️ Falling back to localStorage only');
        return {
            success: false,
            error: error.message,
            fallback: 'localStorage'
        };
    }
}

/**
 * Map dietary preferences to backend format
 */
function mapDietaryToBackend(dietaryArray) {
    if (!dietaryArray || dietaryArray.length === 0) {
        return 'Vegetarian'; // Default
    }
    
    const mapping = {
        'vegetarian': 'Vegetarian',
        'non-vegetarian': 'Non-Vegetarian',
        'vegan': 'Vegan',
        'jain': 'Jain',
        'eggetarian': 'Eggetarian'
    };
    
    // Return first match
    for (const diet of dietaryArray) {
        if (mapping[diet.toLowerCase()]) {
            return mapping[diet.toLowerCase()];
        }
    }
    
    return 'Vegetarian';
}

/**
 * Map cuisine to region
 */
function mapCuisineToRegion(cuisine) {
    const mapping = {
        'north-indian': 'North',
        'south-indian': 'South',
        'gujarati': 'West',
        'bengali': 'East',
        'punjabi': 'North',
        'maharashtrian': 'West',
        'tamil': 'South',
        'kerala': 'South'
    };
    
    return mapping[cuisine?.toLowerCase()] || 'All';
}

/**
 * Enhanced completeSetup function
 * This will be called instead of the original one
 */
async function completeSetupWithDatabase(formData) {
    console.log('🚀 Completing setup with database integration...');
    
    // Show loading
    showLoadingOverlay('Saving your profile...');
    
    try {
        // 1. Save to localStorage (as before)
        localStorage.setItem('mealcraft-profile', JSON.stringify(formData));
        
        // 2. Save to database (NEW!)
        const result = await saveUserToDatabase(formData);
        
        hideLoadingOverlay();
        
        if (result.success) {
            // Success - show message and redirect
            showSuccessMessage('Welcome to MealCraft! Your profile has been created successfully.');
            
            setTimeout(() => {
                window.location.href = 'mealplanner.html';
            }, 1500);
        } else {
            // API failed but localStorage worked
            showWarningMessage('Profile saved locally. Some features may be limited.');
            
            setTimeout(() => {
                window.location.href = 'mealplanner.html';
            }, 2000);
        }
        
    } catch (error) {
        hideLoadingOverlay();
        console.error('Error in setup:', error);
        
        // Still allow user to proceed with localStorage only
        showWarningMessage('Profile saved locally. You can continue, but some features may be limited.');
        
        setTimeout(() => {
            window.location.href = 'mealplanner.html';
        }, 2000);
    }
}

/**
 * UI Helper Functions
 */
function showLoadingOverlay(message) {
    const overlay = document.createElement('div');
    overlay.id = 'onboarding-loader';
    overlay.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    overlay.innerHTML = `
        <div class="bg-white rounded-lg p-8 max-w-md text-center">
            <div class="spinner mx-auto mb-4"></div>
            <p class="text-text-primary text-lg">${message}</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('onboarding-loader');
    if (overlay) {
        overlay.remove();
    }
}

function showSuccessMessage(message) {
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 bg-success text-white px-6 py-4 rounded-lg shadow-lg z-50';
    toast.innerHTML = `
        <div class="flex items-center">
            <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>
            </svg>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

function showWarningMessage(message) {
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 bg-warning text-white px-6 py-4 rounded-lg shadow-lg z-50';
    toast.innerHTML = `
        <div class="flex items-center">
            <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"/>
            </svg>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 4000);
}

/**
 * Add email field to onboarding if it doesn't exist
 */
function addEmailFieldIfNeeded() {
    // Check if email field exists
    const userNameInput = document.getElementById('user-name');
    if (!userNameInput) return;
    
    const emailInput = document.getElementById('user-email-field');
    if (emailInput) return; // Already exists
    
    // Create email field
    const emailFieldHTML = `
        <div class="mb-6">
            <label class="block text-sm font-medium text-text-primary mb-2">
                Email Address (Optional)
                <span class="text-text-secondary text-xs ml-1">- For saving your profile</span>
            </label>
            <input 
                type="email" 
                id="user-email-field" 
                class="input-field w-full" 
                placeholder="your.email@example.com"
            />
        </div>
    `;
    
    // Insert after user name
    userNameInput.parentElement.insertAdjacentHTML('afterend', emailFieldHTML);
}

/**
 * Override the original completeSetup function
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔗 Onboarding database integration loaded');
    
    // Add email field
    addEmailFieldIfNeeded();
    
    // Override the original completeSetup function
    if (typeof window.completeSetup !== 'undefined') {
        const originalCompleteSetup = window.completeSetup;
        
        window.completeSetup = async function() {
            // Get form data from the original function's scope
            const formDataFromPage = window.formData || {};
            
            // Add email if provided
            const emailInput = document.getElementById('user-email-field');
            if (emailInput && emailInput.value) {
                formDataFromPage.email = emailInput.value;
            }
            
            // Call our enhanced version
            await completeSetupWithDatabase(formDataFromPage);
        };
        
        console.log('✅ completeSetup function enhanced with database integration');
    }
});

// Export for global use
window.OnboardingAPI = {
    saveUserToDatabase,
    completeSetupWithDatabase
};
