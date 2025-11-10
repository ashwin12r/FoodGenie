# FoodGenie 🍽️# HTML



> Your Smart Kitchen Companion - AI-Powered Meal Planning & Grocery AutomationA modern HTML project utilizing Tailwind CSS for building responsive web applications with minimal setup.



FoodGenie is an intelligent meal planning application that combines AI-powered recipe recommendations with automated grocery shopping. Built with Python FastAPI backend and vanilla JavaScript frontend.## 🚀 Features



## ✨ Features- **HTML5** - Modern HTML structure with best practices

- **Tailwind CSS** - Utility-first CSS framework for rapid UI development

### 🔐 **Authentication System**- **Custom Components** - Pre-built component classes for buttons and containers

- User registration and login  - **NPM Scripts** - Easy-to-use commands for development and building

- Secure password hashing- **Responsive Design** - Mobile-first approach for all screen sizes

- Personalized user dashboard

- Activity tracking## 📋 Prerequisites



### 🎯 **Smart Meal Planning**- Node.js (v12.x or higher)

- AI-powered meal recommendations- npm or yarn

- Dietary preference customization

- Budget-based meal planning## 🛠️ Installation

- Weekly meal schedules

- Nutritional information tracking1. Install dependencies:

```bash

### 🛒 **AI Shopping Automation**npm install

- Automated BigBasket ordering via Playwright# or

- Real-time ingredient extractionyarn install

- Smart shopping list generation```

- Price tracking and optimization

2. Start the development server:

### 👤 **User Dashboard**```bash

- View meal plan historynpm run dev

- Track shopping lists# or

- Monitor spendingyarn dev

- Manage preferences```



### 🍳 **Recipe Discovery**## 📁 Project Structure

- Browse 255+ Indian cuisine recipes

- Filter by diet type (Vegetarian, Non-Vegetarian, Vegan)```

- Search by ingredientshtml_app/

- Detailed cooking instructions├── css/

│   ├── tailwind.css   # Tailwind source file with custom utilities

## 🚀 Quick Start│   └── main.css       # Compiled CSS (generated)

├── pages/             # HTML pages

### Prerequisites├── index.html         # Main entry point

├── package.json       # Project dependencies and scripts

- **Node.js** (v12.x or higher)└── tailwind.config.js # Tailwind CSS configuration

- **Python 3.12.6** (Important: NOT 3.13+ due to Playwright compatibility)```

- **PostgreSQL** (Neon Database)

- **Google Chrome** (for automation)## 🎨 Styling



### InstallationThis project uses Tailwind CSS for styling. Custom utility classes include:



1. **Clone the repository**

```bash## 🧩 Customization

git clone https://github.com/ashwin12r/FoodGenie.git

cd FoodGenieTo customize the Tailwind configuration, edit the `tailwind.config.js` file:

```



2. **Frontend Setup**## 📦 Build for Production

```bash

npm installBuild the CSS for production:

npm run build:css

``````bash

npm run build:css

3. **Backend Setup**# or

```bashyarn build:css

cd ML```



# Create virtual environment with Python 3.12## 📱 Responsive Design

python -m venv ../.venv

The app is built with responsive design using Tailwind CSS breakpoints:

# Activate virtual environment

..\.venv\Scripts\activate  # Windows- `sm`: 640px and up

source ../.venv/bin/activate  # Linux/Mac- `md`: 768px and up

- `lg`: 1024px and up

# Install dependencies- `xl`: 1280px and up

pip install -r requirements.txt- `2xl`: 1536px and up



# Install Playwright browsers

playwright install chromium
```

4. **Database Setup**

Create a `.env` file in the `ML` directory:
```env
DATABASE_URL=your_neon_database_url
GOOGLE_API_KEY=your_google_api_key
```

5. **Initialize Database**
```bash
cd ML
python -c "from database import db; db.initialize_schema()"
```

6. **Start Backend Server**
```bash
cd ML
python -m uvicorn backend_server:app --host 0.0.0.0 --port 8000 --reload
```

7. **Open Frontend**
- Open `index.html` in your browser
- Or use Live Server in VS Code

## 📖 Usage Guide

### 1. **Sign Up / Login**
- Navigate to `pages/auth.html`
- Create a new account or login
- Enter your details (name, email, family size, city)

### 2. **Setup Preferences**
- Complete the onboarding flow (`pages/onboarding.html`)
- Set dietary preferences (Vegetarian, Vegan, etc.)
- Choose cuisine preferences
- Set budget and health goals
- Configure cooking time and complexity

### 3. **Generate Meal Plan**
- Go to Meal Planner (`pages/mealplanner.html`)
- Your AI-powered weekly meal plan will be generated
- View nutritional information and costs
- Customize meals as needed

### 4. **Smart Shopping**
- Navigate to Smart Shopping (`pages/smartshopping.html`)
- Click "AI Auto-Order from Meal Plan"
- Select dishes from your meal plan
- AI extracts ingredients automatically
- Click "Order on BigBasket" for automated ordering

### 5. **Browse Recipes**
- Explore Recipe Discovery (`pages/recipe_discovery.html`)
- Search and filter recipes
- View ingredients and instructions
- Add to meal plan

## 🏗️ Architecture

### Frontend Structure
```
├── pages/
│   ├── auth.html              # Login/Signup
│   ├── dashboard.html         # User dashboard
│   ├── onboarding.html        # Preference setup
│   ├── mealplanner.html       # Meal planning
│   ├── smartshopping.html     # Shopping & automation
│   └── recipe_discovery.html  # Recipe browsing
├── css/
│   ├── main.css              # Compiled Tailwind
│   └── tailwind.css          # Source styles
└── public/
    └── manifest.json         # PWA config
```

### Backend Structure
```
ML/
├── backend_server.py         # FastAPI server
├── database.py              # Neon PostgreSQL
├── ai_grocery_agent.py      # Playwright automation
├── mealcraft_ai.py          # AI meal planning
└── indian_food_cleaned.csv  # Recipe database
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Login user
- `GET /api/user/dashboard/{email}` - Get user stats

### User Management
- `POST /api/users/create` - Create user profile
- `GET /api/users/{email}` - Get user details
- `POST /api/preferences/save` - Save dietary preferences
- `GET /api/preferences/{email}` - Get user preferences

### Meal Planning
- `POST /api/meal-plan/generate` - Generate AI meal plan
- `GET /api/meal-plans/user/{email}` - Get user's meal plans

### Shopping
- `POST /api/automate-order` - Automated BigBasket ordering
- `POST /api/grocery/scrape` - Update grocery prices

### Recipes
- `GET /api/recipes` - List all recipes
- `GET /api/recipes/filter` - Filter by diet/cuisine
- `GET /api/recipes/{dish_name}` - Get recipe details

## 🗄️ Database Schema

### Users Table
- `id`, `email`, `user_name`, `password_hash`
- `family_size`, `city`, `created_at`, `updated_at`

### User Preferences Table
- `user_id`, `diet`, `preferred_cuisines`, `dietary_restrictions`
- `cooking_time_limit`, `weekly_budget`, `health_goals`

### Meal Plans Table
- `user_id`, `plan_data`, `start_date`, `end_date`
- `total_cost`, `total_calories`, `status`

### Shopping Lists Table
- `meal_plan_id`, `user_id`, `items`, `total_cost`, `status`

## 🎨 Tech Stack

- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Backend**: Python 3.12, FastAPI, Uvicorn
- **Database**: PostgreSQL (Neon Cloud)
- **AI/ML**: Custom recommendation engine
- **Automation**: Playwright (Synchronous API)
- **Browser**: Google Chrome (for automation)

## 🔧 Configuration

### Tailwind CSS
Edit `tailwind.config.js` to customize:
- Colors
- Typography
- Breakpoints
- Custom utilities

### Backend Settings
Edit `backend_server.py` for:
- CORS origins
- API rate limits
- Database connection
- ML model parameters

## 🐛 Troubleshooting

### Python 3.13 Compatibility Issue
If you see `NotImplementedError` with Playwright:
```bash
# Uninstall Python 3.13
# Install Python 3.12.6 from python.org
# Recreate virtual environment
python3.12 -m venv .venv
```

### Backend Not Starting
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process_id> /F
```

### Database Connection Error
- Verify DATABASE_URL in `.env`
- Check Neon dashboard for connection string
- Ensure SSL mode is set correctly

### Automation Not Working
- Verify Chrome is installed at default path
- Check Playwright installation: `playwright install chromium`
- Ensure backend server is running

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Ashwin**
- GitHub: [@ashwin12r](https://github.com/ashwin12r)

## 🙏 Acknowledgments

- Recipe data sourced from Indian cuisine database
- UI inspired by modern food delivery apps
- AI recommendations powered by collaborative filtering

---

**Note**: This project requires a Neon PostgreSQL database. Sign up at [neon.tech](https://neon.tech) for a free account.

For detailed documentation, visit the [Wiki](https://github.com/ashwin12r/FoodGenie/wiki).
