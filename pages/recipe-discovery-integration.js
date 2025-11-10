/**
 * MealCraft Recipe Discovery Integration
 * Connects recipe discovery page to backend API
 */

// Current recipes loaded
let currentRecipes = [];
let allRecipes = []; // Store all recipes for filtering
let currentFilters = {
    query: '',
    diet: null,
    course: null,
    region: null,
    flavor: null,
    max_time: null
};

// Available filter options
let filterOptions = {
    regions: new Set(),
    courses: new Set(),
    flavors: new Set()
};

/**
 * Initialize recipe discovery page
 */
async function initializeRecipeDiscovery() {
    console.log('🔍 Initializing Recipe Discovery...');
    
    try {
        // Check API health
        const health = await mealCraftAPI.healthCheck();
        console.log('✅ Backend API connected:', health);
        
        // Load ALL recipes from dataset
        await loadAllRecipes();
        
        // Setup search functionality
        setupSearchListeners();
        
        // Populate filter dropdowns
        populateFilterOptions();
        
    } catch (error) {
        console.error('❌ Backend API not available:', error);
        console.log('ℹ️ Showing demo recipes');
        showDemoRecipes();
    }
}

/**
 * Load all recipes from the dataset
 */
async function loadAllRecipes() {
    try {
        showLoading();
        
        // Request all recipes (high limit)
        const response = await fetch(`${mealCraftAPI.baseURL}/api/recipes/search?limit=500`);
        const data = await response.json();
        
        if (data.success) {
            allRecipes = data.recipes;
            currentRecipes = allRecipes;
            
            // Extract unique filter options
            allRecipes.forEach(recipe => {
                if (recipe.region) filterOptions.regions.add(recipe.region);
                if (recipe.course) filterOptions.courses.add(recipe.course);
                if (recipe.flavor_profile) filterOptions.flavors.add(recipe.flavor_profile);
            });
            
            displayRecipes(currentRecipes);
            console.log(`✅ Loaded ${data.count} recipes from dataset`);
            
            // Update stats
            updateStats(data.count);
        }
        
        hideLoading();
        
    } catch (error) {
        console.error('❌ Error loading recipes:', error);
        hideLoading();
        showError('Failed to load recipes. Please refresh the page.');
    }
}

/**
 * Populate filter dropdown options
 */
function populateFilterOptions() {
    // Populate regions
    const regionFilter = document.getElementById('region-filter');
    if (regionFilter && filterOptions.regions.size > 0) {
        Array.from(filterOptions.regions).sort().forEach(region => {
            const option = document.createElement('option');
            option.value = region;
            option.textContent = region;
            regionFilter.appendChild(option);
        });
    }
    
    // Populate courses
    const courseFilter = document.getElementById('course-filter');
    if (courseFilter && filterOptions.courses.size > 0) {
        Array.from(filterOptions.courses).sort().forEach(course => {
            const option = document.createElement('option');
            option.value = course;
            option.textContent = course;
            courseFilter.appendChild(option);
        });
    }
    
    // Populate flavors
    const flavorFilter = document.getElementById('flavor-filter');
    if (flavorFilter && filterOptions.flavors.size > 0) {
        Array.from(filterOptions.flavors).sort().forEach(flavor => {
            const option = document.createElement('option');
            option.value = flavor;
            option.textContent = flavor;
            flavorFilter.appendChild(option);
        });
    }
    
    console.log('✅ Filter options populated');
}

/**
 * Setup search and filter listeners
 */
function setupSearchListeners() {
    // Search input
    const searchInput = document.getElementById('recipe-search');
    if (searchInput) {
        searchInput.addEventListener('keyup', debounce(async (e) => {
            currentFilters.query = e.target.value;
            await applyFilters();
        }, 500));
        
        // Also add search button click
        const searchButton = searchInput.parentElement.querySelector('button');
        if (searchButton) {
            searchButton.addEventListener('click', async () => {
                currentFilters.query = searchInput.value;
                await applyFilters();
            });
        }
    }
    
    // Diet filter
    const dietFilter = document.getElementById('diet-filter');
    if (dietFilter) {
        dietFilter.addEventListener('change', async (e) => {
            currentFilters.diet = e.target.value || null;
            await applyFilters();
        });
    }
    
    // Course filter
    const courseFilter = document.getElementById('course-filter');
    if (courseFilter) {
        courseFilter.addEventListener('change', async (e) => {
            currentFilters.course = e.target.value || null;
            await applyFilters();
        });
    }
    
    // Region filter
    const regionFilter = document.getElementById('region-filter');
    if (regionFilter) {
        regionFilter.addEventListener('change', async (e) => {
            currentFilters.region = e.target.value || null;
            await applyFilters();
        });
    }
    
    // Flavor filter
    const flavorFilter = document.getElementById('flavor-filter');
    if (flavorFilter) {
        flavorFilter.addEventListener('change', async (e) => {
            currentFilters.flavor = e.target.value || null;
            await applyFilters();
        });
    }
    
    // Time filter
    const timeFilter = document.getElementById('time-filter');
    if (timeFilter) {
        timeFilter.addEventListener('change', async (e) => {
            currentFilters.max_time = e.target.value ? parseInt(e.target.value) : null;
            await applyFilters();
        });
    }
    
    console.log('✅ Search listeners setup complete');
}

/**
 * Apply filters to loaded recipes (client-side filtering for speed)
 */
async function applyFilters() {
    showLoading();
    
    let filtered = [...allRecipes];
    
    // Apply query search
    if (currentFilters.query) {
        const query = currentFilters.query.toLowerCase();
        filtered = filtered.filter(recipe => 
            recipe.name.toLowerCase().includes(query) ||
            (recipe.ingredients && recipe.ingredients.toLowerCase().includes(query)) ||
            (recipe.region && recipe.region.toLowerCase().includes(query)) ||
            (recipe.course && recipe.course.toLowerCase().includes(query))
        );
    }
    
    // Apply diet filter
    if (currentFilters.diet) {
        filtered = filtered.filter(recipe => 
            recipe.diet && recipe.diet.toLowerCase() === currentFilters.diet.toLowerCase()
        );
    }
    
    // Apply course filter
    if (currentFilters.course) {
        filtered = filtered.filter(recipe => 
            recipe.course && recipe.course.toLowerCase() === currentFilters.course.toLowerCase()
        );
    }
    
    // Apply region filter
    if (currentFilters.region) {
        filtered = filtered.filter(recipe => 
            recipe.region && recipe.region.toLowerCase() === currentFilters.region.toLowerCase()
        );
    }
    
    // Apply flavor filter
    if (currentFilters.flavor) {
        filtered = filtered.filter(recipe => 
            recipe.flavor_profile && recipe.flavor_profile.toLowerCase() === currentFilters.flavor.toLowerCase()
        );
    }
    
    // Apply time filter
    if (currentFilters.max_time) {
        filtered = filtered.filter(recipe => {
            const time = recipe.total_time || recipe.cook_time || 0;
            return time <= currentFilters.max_time;
        });
    }
    
    currentRecipes = filtered;
    displayRecipes(currentRecipes);
    updateResultsCount(filtered.length);
    
    console.log(`🔍 Filtered: ${filtered.length} recipes`);
    
    hideLoading();
}

/**
 * Reset all filters
 */
function resetFilters() {
    currentFilters = {
        query: '',
        diet: null,
        course: null,
        region: null,
        flavor: null,
        max_time: null
    };
    
    // Reset UI
    const searchInput = document.getElementById('recipe-search');
    if (searchInput) searchInput.value = '';
    
    const selects = document.querySelectorAll('select');
    selects.forEach(select => select.selectedIndex = 0);
    
    // Show all recipes
    currentRecipes = allRecipes;
    displayRecipes(currentRecipes);
    updateResultsCount(allRecipes.length);
    
    console.log('🔄 Filters reset');
}

/**
 * Update stats display
 */
function updateStats(count) {
    // Update recipe count in hero section
    const statsElements = document.querySelectorAll('.text-2xl.font-bold');
    if (statsElements[0]) {
        statsElements[0].textContent = count + '+';
    }
}

/**
 * Load random recipes for discovery
 */
async function loadRandomRecipes(count = 12) {
    try {
        showLoading();
        
        const response = await fetch(`${mealCraftAPI.baseURL}/api/recipes/random?count=${count}`);
        const data = await response.json();
        
        if (data.success) {
            currentRecipes = data.recipes;
            displayRecipes(currentRecipes);
            console.log(`✅ Loaded ${data.count} random recipes`);
        }
        
        hideLoading();
        
    } catch (error) {
        console.error('❌ Error loading random recipes:', error);
        hideLoading();
        showError('Failed to load recipes. Please try again.');
    }
}

/**
 * Display recipes in the grid
 */
function displayRecipes(recipes) {
    const grid = document.getElementById('recipe-grid');
    if (!grid) {
        console.error('Recipe grid element not found');
        return;
    }
    
    if (recipes.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full text-center py-12">
                <svg class="w-16 h-16 mx-auto text-neutral-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                <h3 class="text-xl font-semibold text-text-primary mb-2">No recipes found</h3>
                <p class="text-text-secondary">Try adjusting your filters or search terms</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = recipes.map(recipe => createRecipeCard(recipe)).join('');
    
    // Add click listeners to recipe cards
    recipes.forEach((recipe, index) => {
        const card = grid.children[index];
        if (card) {
            card.addEventListener('click', () => viewRecipeDetails(recipe.name));
        }
    });
}

/**
 * Create recipe card HTML
 */
function createRecipeCard(recipe) {
    const dietColor = recipe.diet === 'vegetarian' ? 'bg-green-100 text-green-800' : 
                     recipe.diet === 'vegan' ? 'bg-purple-100 text-purple-800' : 
                     'bg-red-100 text-red-800';
    
    return `
        <div class="card overflow-hidden hover:shadow-lg transition-smooth cursor-pointer">
            <div class="h-48 bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center">
                <div class="text-center p-4">
                    <div class="text-4xl mb-2">🍽️</div>
                    <h3 class="font-bold text-lg text-text-primary">${recipe.name}</h3>
                </div>
            </div>
            
            <div class="p-4">
                <div class="flex items-start justify-between mb-2">
                    <h3 class="text-lg font-semibold text-text-primary line-clamp-1">${recipe.name}</h3>
                    <button onclick="saveRecipe('${recipe.name}'); event.stopPropagation();" class="text-text-secondary hover:text-accent transition-smooth">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                        </svg>
                    </button>
                </div>
                
                <div class="flex items-center gap-2 mb-3">
                    <span class="${dietColor} text-xs px-2 py-1 rounded-full font-medium">
                        ${recipe.diet}
                    </span>
                    <span class="text-xs text-text-secondary">${recipe.course || 'Main'}</span>
                </div>
                
                <p class="text-sm text-text-secondary mb-3 line-clamp-2">
                    ${recipe.ingredients || 'Traditional Indian dish with authentic flavors'}
                </p>
                
                <div class="grid grid-cols-3 gap-2 text-xs text-text-secondary border-t border-neutral-100 pt-3">
                    <div class="flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        ${recipe.total_time || recipe.cook_time || 30} min
                    </div>
                    <div class="flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                        </svg>
                        ${recipe.region || 'India'}
                    </div>
                    <div class="flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                        </svg>
                        ${recipe.flavor_profile || 'Mild'}
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * View recipe details in modal
 */
async function viewRecipeDetails(recipeName) {
    try {
        showLoading();
        
        const response = await fetch(`${mealCraftAPI.baseURL}/api/recipes/${encodeURIComponent(recipeName)}`);
        const data = await response.json();
        
        if (data.success) {
            displayRecipeModal(data.recipe);
            console.log('✅ Loaded recipe details:', recipeName);
        }
        
        hideLoading();
        
    } catch (error) {
        console.error('❌ Error loading recipe details:', error);
        hideLoading();
        showError('Failed to load recipe details. Please try again.');
    }
}

/**
 * Display recipe details in modal
 */
function displayRecipeModal(recipe) {
    // Create modal HTML
    const imageUrl = recipe.image_url || 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&q=80';
    
    const modalHTML = `
        <div id="recipe-modal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4" onclick="closeRecipeModal(event)">
            <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" onclick="event.stopPropagation()">
                <!-- Header -->
                <div class="sticky top-0 bg-white border-b border-neutral-200 p-6 flex items-center justify-between">
                    <div>
                        <div class="text-5xl mb-3">🍽️</div>
                        <h2 class="text-3xl font-bold text-text-primary mb-2">${recipe.name}</h2>
                        <p class="text-text-secondary">${recipe.region || 'Indian'} | ${recipe.course || 'Main Course'}</p>
                    </div>
                    <button onclick="closeRecipeModal()" class="text-text-secondary hover:text-text-primary rounded-full p-2">
                        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
                
                <!-- Content -->
                <div class="p-6">
                    <!-- Quick Info -->
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                        <div class="text-center p-3 bg-primary-50 rounded-lg">
                            <div class="text-2xl font-bold text-primary">${recipe.prep_time || 15} min</div>
                            <div class="text-sm text-text-secondary">Prep Time</div>
                        </div>
                        <div class="text-center p-3 bg-secondary-50 rounded-lg">
                            <div class="text-2xl font-bold text-secondary">${recipe.cook_time || 30} min</div>
                            <div class="text-sm text-text-secondary">Cook Time</div>
                        </div>
                        <div class="text-center p-3 bg-accent-50 rounded-lg">
                            <div class="text-2xl font-bold text-accent">₹${recipe.estimated_cost || 50}</div>
                            <div class="text-sm text-text-secondary">Est. Cost</div>
                        </div>
                        <div class="text-center p-3 bg-neutral-50 rounded-lg">
                            <div class="text-2xl font-bold text-text-primary">${recipe.nutrition?.calories || 350}</div>
                            <div class="text-sm text-text-secondary">Calories</div>
                        </div>
                    </div>
                    
                    <!-- Ingredients -->
                    <div class="mb-6">
                        <h3 class="text-xl font-semibold text-text-primary mb-3">Ingredients</h3>
                        <div class="bg-neutral-50 rounded-lg p-4">
                            <p class="text-text-secondary">${recipe.ingredients}</p>
                        </div>
                    </div>
                    
                    <!-- Instructions -->
                    <div class="mb-6">
                        <h3 class="text-xl font-semibold text-text-primary mb-3">Instructions</h3>
                        <div class="space-y-3">
                            ${recipe.instructions.map((instruction, index) => `
                                <div class="flex items-start">
                                    <span class="flex-shrink-0 w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-semibold text-sm mr-3">
                                        ${index + 1}
                                    </span>
                                    <p class="text-text-secondary pt-1">${instruction}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <!-- Tips & Serving (if available) -->
                    ${recipe.tips || recipe.serving ? `
                    <div class="mb-6 grid gap-4 ${recipe.tips && recipe.serving ? 'md:grid-cols-2' : ''}">
                        ${recipe.tips ? `
                        <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                            <h4 class="font-semibold text-yellow-800 mb-2">💡 Tips</h4>
                            <p class="text-sm text-yellow-700">${recipe.tips}</p>
                        </div>
                        ` : ''}
                        ${recipe.serving ? `
                        <div class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
                            <h4 class="font-semibold text-blue-800 mb-2">🍽️ Serving</h4>
                            <p class="text-sm text-blue-700">${recipe.serving}</p>
                        </div>
                        ` : ''}
                    </div>
                    ` : ''}
                    
                    <!-- Nutrition Info -->
                    ${recipe.nutrition ? `
                    <div class="mb-6">
                        <h3 class="text-xl font-semibold text-text-primary mb-3">Nutritional Information</h3>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div class="bg-primary-50 p-3 rounded-lg text-center">
                                <div class="text-lg font-bold text-primary">${recipe.nutrition.protein}g</div>
                                <div class="text-xs text-text-secondary">Protein</div>
                            </div>
                            <div class="bg-secondary-50 p-3 rounded-lg text-center">
                                <div class="text-lg font-bold text-secondary">${recipe.nutrition.carbs}g</div>
                                <div class="text-xs text-text-secondary">Carbs</div>
                            </div>
                            <div class="bg-accent-50 p-3 rounded-lg text-center">
                                <div class="text-lg font-bold text-accent">${recipe.nutrition.fat}g</div>
                                <div class="text-xs text-text-secondary">Fat</div>
                            </div>
                            <div class="bg-neutral-50 p-3 rounded-lg text-center">
                                <div class="text-lg font-bold text-text-primary">${recipe.nutrition.fiber || 5}g</div>
                                <div class="text-xs text-text-secondary">Fiber</div>
                            </div>
                        </div>
                    </div>
                    ` : ''}
                    
                    <!-- Actions -->
                    <div class="flex gap-3">
                        <button class="btn-primary flex-1" onclick="addRecipeToMealPlan('${recipe.name}')">
                            Add to Meal Plan
                        </button>
                        <button class="btn-secondary flex-1" onclick="shareRecipe('${recipe.name}')">
                            Share Recipe
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

/**
 * Close recipe modal
 */
function closeRecipeModal(event) {
    if (!event || event.target.id === 'recipe-modal') {
        const modal = document.getElementById('recipe-modal');
        if (modal) {
            modal.remove();
        }
    }
}

/**
 * Add recipe to meal plan
 */
function addRecipeToMealPlan(recipeName) {
    console.log('Adding to meal plan:', recipeName);
    // Store in localStorage for meal planner page
    const savedRecipes = JSON.parse(localStorage.getItem('saved-recipes') || '[]');
    if (!savedRecipes.includes(recipeName)) {
        savedRecipes.push(recipeName);
        localStorage.setItem('saved-recipes', JSON.stringify(savedRecipes));
    }
    showSuccess(`${recipeName} added to your favorites!`);
    closeRecipeModal();
}

/**
 * Share recipe
 */
function shareRecipe(recipeName) {
    console.log('Sharing recipe:', recipeName);
    if (navigator.share) {
        navigator.share({
            title: recipeName,
            text: `Check out this recipe: ${recipeName}`,
            url: window.location.href
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback - copy to clipboard
        const url = `${window.location.origin}/recipe_discovery.html?recipe=${encodeURIComponent(recipeName)}`;
        navigator.clipboard.writeText(url);
        showSuccess('Recipe link copied to clipboard!');
    }
}

/**
 * Update results count
 */
function updateResultsCount(count) {
    const countElement = document.getElementById('results-count');
    if (countElement) {
        countElement.textContent = `${count} recipes found`;
    }
}

/**
 * Show demo recipes (fallback)
 */
function showDemoRecipes() {
    const demoRecipes = [
        { name: 'Dal Tadka', diet: 'vegetarian', course: 'main', ingredients: 'Toor dal, onions, tomatoes, spices', total_time: 45, region: 'North', flavor_profile: 'spicy' },
        { name: 'Butter Chicken', diet: 'non-vegetarian', course: 'main', ingredients: 'Chicken, butter, cream, spices', total_time: 60, region: 'North', flavor_profile: 'mild' },
        { name: 'Masala Dosa', diet: 'vegetarian', course: 'breakfast', ingredients: 'Rice, urad dal, potatoes, spices', total_time: 30, region: 'South', flavor_profile: 'spicy' }
    ];
    displayRecipes(demoRecipes);
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Loading overlay
 */
function showLoading() {
    const loader = document.createElement('div');
    loader.id = 'recipe-loader';
    loader.className = 'fixed inset-0 bg-black bg-opacity-30 z-40 flex items-center justify-center';
    loader.innerHTML = '<div class="bg-white rounded-lg p-6"><div class="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full"></div></div>';
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.getElementById('recipe-loader');
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

// Make functions globally accessible
window.viewRecipeDetails = viewRecipeDetails;
window.closeRecipeModal = closeRecipeModal;
window.addRecipeToMealPlan = addRecipeToMealPlan;
window.shareRecipe = shareRecipe;
window.resetFilters = resetFilters;
window.setViewMode = setViewMode;
window.currentFilters = currentFilters;
window.applyFilters = applyFilters;
window.saveRecipe = function(recipeName) {
    const savedRecipes = JSON.parse(localStorage.getItem('saved-recipes') || '[]');
    if (!savedRecipes.includes(recipeName)) {
        savedRecipes.push(recipeName);
        localStorage.setItem('saved-recipes', JSON.stringify(savedRecipes));
        showSuccess(`${recipeName} saved!`);
    }
};

/**
 * Set view mode (grid or list)
 */
function setViewMode(mode) {
    const grid = document.getElementById('recipe-grid');
    if (!grid) return;
    
    if (mode === 'list') {
        grid.className = 'space-y-4';
        // TODO: Update card display for list view
    } else {
        grid.className = 'grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6';
    }
}
