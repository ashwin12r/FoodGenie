/**
 * MealCraft API Client
 * JavaScript API wrapper for frontend-backend communication
 */

class MealCraftAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    /**
     * Generic API request handler
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // ===== HEALTH CHECK =====

    async healthCheck() {
        return this.request('/health');
    }

    // ===== USER MANAGEMENT =====

    async createUser(userData) {
        return this.request('/api/users/create', {
            method: 'POST',
            body: JSON.stringify(userData),
        });
    }

    async getUser(email) {
        return this.request(`/api/users/${encodeURIComponent(email)}`);
    }

    // ===== PREFERENCES =====

    async savePreferences(preferences) {
        return this.request('/api/preferences/save', {
            method: 'POST',
            body: JSON.stringify(preferences),
        });
    }

    async getPreferences(email) {
        return this.request(`/api/preferences/${encodeURIComponent(email)}`);
    }

    // ===== MEAL PLANS =====

    async generateMealPlan(email, preferences = null) {
        return this.request('/api/meal-plan/generate', {
            method: 'POST',
            body: JSON.stringify({
                email: email,
                preferences: preferences,
            }),
        });
    }

    async getMealPlan(mealPlanId) {
        return this.request(`/api/meal-plan/${mealPlanId}`);
    }

    async getUserMealPlans(email, limit = 10) {
        return this.request(`/api/meal-plan/user/${encodeURIComponent(email)}?limit=${limit}`);
    }

    // ===== GROCERY PRICES =====

    async getGroceryPrices(store = null) {
        const endpoint = store 
            ? `/api/grocery/prices?store=${encodeURIComponent(store)}`
            : '/api/grocery/prices';
        return this.request(endpoint);
    }

    async scrapeGroceryPrices(stores = ['Grace Daily', 'KPN Fresh']) {
        return this.request('/api/grocery/scrape', {
            method: 'POST',
            body: JSON.stringify(stores),
        });
    }

    async comparePrices(itemName) {
        return this.request(`/api/grocery/compare?item_name=${encodeURIComponent(itemName)}`);
    }

    // ===== OPTIONS =====

    async getAvailableOptions() {
        return this.request('/api/options');
    }
}

// Create global instance
const mealCraftAPI = new MealCraftAPI();

// Export for use in modules (optional)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MealCraftAPI, mealCraftAPI };
}
