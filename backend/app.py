from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.models import User, Game

# This file will contain the main Flask Application and routes

# Create a Flask application
app = Flask(__name__)

# Configure the database connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:3rQ1eq0z1TLN@localhost:3306/game_db'

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'Welcome to the game application!'


# Define Flask routes: these routes will handle HTTP requests
# from clients and execute corresponding logic

# Interact with the database (e.g., perform database operations within your Flask routes)
# Route to create a new user record
@app.route('/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        # Parse JSON data from the request body
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()  # Commit changes to the database


# handle POST requests. When a POST request is received
# the user ID is extracted from the request JSON data
# Then, a new Game record is created with the provided user ID,
# added to the database session, and committed to persist the changes.
# With this route implemented, you can now make a POST request to /create_game endpoint
# with the necessary data to create a new game record associated with a user.
@app.route('/create_game', methods=['POST'])
def create_game():
    # Assuming you receive user ID from the request
    user_id = request.json.get('user_id')

    # Create a new game record
    new_game = Game(user_id=user_id)
    db.session.add(new_game)
    db.session.commit()

    return 'Game created successfully'


@app.route('/matchmaking', methods=['POST'])
def matchmaking():
    # Logic for matching players together
    return 'Players matched successfully'


@app.route('/game/move', methods=['POST'])
def handle_move():
    # Logic for handling game moves
    return 'Move handled successfully'


@app.route('/game/winner', methods=['POST'])
def determine_winner():
    # Logic for determining the winner
    return 'Winner determined successfully'


# Main section to run the Flask application
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)


# # Integrate with existing code: might need to refactor
# @app.route('/train', methods=['POST'])
# def train_model_route():
#     # Call your existing code to train the model
#     train()
#     return 'Model trained successfully'


# Add player vs Player functionality
@app.route('/player_vs_player', methods=['POST'])
def player_vs_player():
    # Logic for player vs player functionality
    return 'Player vs Player functionality added successfully'

# update frontend - done in script.js

# Test Flask application - done in TestFlaskApp.py
