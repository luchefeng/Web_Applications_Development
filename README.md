# My Web Project

This project is a web application that allows users to log in, input their desired calorie intake, and receive recipe recommendations. Users can also view and post recipes and articles.

## Project Structure

```
my-web-project
├── backend
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   ├── config.py
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── assets
│   │   ├── components
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── RecipeList.vue
│   │   │   ├── RecipeDetail.vue
│   │   │   ├── ArticleList.vue
│   │   │   └── ArticleDetail.vue
│   │   ├── router
│   │   │   └── index.js
│   │   ├── store
│   │   │   └── index.js
│   │   ├── views
│   │   │   ├── Home.vue
│   │   │   ├── Profile.vue
│   │   │   ├── Recipes.vue
│   │   │   └── Articles.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── babel.config.js
│   ├── vue.config.js
│   └── README.md
└── README.md
```

## Backend

The backend is built using Flask and provides the following functionalities:

- User authentication (login and registration)
- Recipe management (posting and retrieving recipes)
- Article management (posting and retrieving articles)

### Setup Instructions

1. Navigate to the `backend` directory.
2. Install the required Python packages using:
   ```
   pip install -r requirements.txt
   ```
3. Set up the database and run the application:
   ```
   python app.py
   ```

## Frontend

The frontend is built using Vue 3 and provides a user-friendly interface for interacting with the backend.

### Setup Instructions

1. Navigate to the `frontend` directory.
2. Install the required Node.js packages using:
   ```
   npm install
   ```
3. Run the Vue application:
   ```
   npm run serve
   ```

## Usage

- Users can log in or register to access personalized features.
- Users can input their calorie intake and receive tailored recipe recommendations.
- Users can view and post recipes and articles related to nutrition.

## License

This project is licensed under the MIT License.