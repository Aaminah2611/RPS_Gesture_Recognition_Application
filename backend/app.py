from flask import Flask

from scripts import train

# This file will contain the main Flask Application and routes

# Create a Flask application
app = Flask(__name__)

# Define Flask routes: these routes will handle HTTP requests
# from clients and execute corresponding logic

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

# Integrate with existing code: might need to refactor
@app.route('/train', methods=['POST'])
def train_model_route():
    # Call your existing code to train the model
    train()
    return 'Model trained successfully'


# Add player vs Player functionality
@app.route('/player_vs_player', methods=['POST'])
def player_vs_player():
    # Logic for player vs player functionality
    return 'Player vs Player functionality added successfully'

# update frontend - done in script.js

# Test Flask application - done in TestFlaskApp.py
