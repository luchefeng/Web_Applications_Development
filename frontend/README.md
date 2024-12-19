# My Web Project - Frontend

This project is a web application built using Vue 3 for the frontend and Flask for the backend. It allows users to log in, input their desired calorie intake, and receive recipe recommendations. Users can also view and post recipes and articles.

## Project Structure

```
frontend
├── public
│   └── index.html
├── src
│   ├── assets
│   ├── components
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── RecipeList.vue
│   │   ├── RecipeDetail.vue
│   │   ├── ArticleList.vue
│   │   └── ArticleDetail.vue
│   ├── router
│   │   └── index.js
│   ├── store
│   │   └── index.js
│   ├── views
│   │   ├── Home.vue
│   │   ├── Profile.vue
│   │   ├── Recipes.vue
│   │   └── Articles.vue
│   ├── App.vue
│   └── main.js
├── package.json
├── babel.config.js
└── vue.config.js
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd my-web-project/frontend
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Run the application:**
   ```
   npm run serve
   ```

4. **Access the application:**
   Open your browser and navigate to `http://localhost:8080`.

## Features

- User authentication (login and registration)
- Input and manage calorie intake
- Recipe recommendations based on user preferences
- View and post recipes
- View articles related to recipes and nutrition

## Usage

- Users can log in to access personalized features.
- Users can input their calorie goals to receive tailored recipe suggestions.
- Users can browse and contribute to a collection of recipes and articles.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.