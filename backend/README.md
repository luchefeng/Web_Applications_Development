# My Web Project - Backend

## Overview
This project is a web application that allows users to log in, input their desired calorie intake, and receive recipe recommendations. Users can also view and post recipes and articles. The backend is built using Flask and interacts with a MySQL database.

## Setup Instructions

### Prerequisites
- Python 3.x
- MySQL Server
- Virtual Environment (recommended)

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-web-project/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a MySQL database named `flaskdb`.
   - Update the database connection details in `config.py` if necessary.

5. Set environment variables:
   - Set the `SECRET_KEY` environment variable for session management.

### Running the Application
To run the Flask application, execute:
```
flask run
```
The application will be available at `http://localhost:5000`.

## API Endpoints

### User Authentication
- **POST /login**: Log in a user.
- **POST /register**: Register a new user.

### Recipe Management
- **GET /recipes**: Retrieve a list of recipes based on user preferences.
- **POST /recipes**: Post a new recipe.

### Article Management
- **GET /articles**: Retrieve a list of articles.
- **GET /articles/<id>**: Retrieve a specific article.

## Usage Examples
- To log in, send a POST request to `/login` with the username and password.
- To register, send a POST request to `/register` with the required user information.
- To get recipe recommendations, send a GET request to `/recipes` after logging in.

## License
This project is licensed under the MIT License.