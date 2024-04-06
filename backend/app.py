import os
import cv2
from flask import Flask, render_template, redirect, request, jsonify
from queue import Queue
from flask_sqlalchemy import SQLAlchemy
from keras.models import load_model

from backend import game
from backend.game.Game import GameThread
from backend.game.ai_logic import AiLogic
from backend.game.player_logic import PlayerLogic
from models.models import User, Game
import mysql.connector

# Create a Flask application
app = Flask(__name__)

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
app.template_folder = template_dir

# Configure the database connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3rQ1eq0z1TLN@localhost:3306/game_db'

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Establishing a connection to the MySQL database
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='3rQ1eq0z1TLN',
        database='game_db'
    )

    if connection.is_connected():
        print('Connected to MySQL database')

    # Function to make a move for player vs AI
    @app.route('/make_move_ai', methods=['POST'])
    def make_move_ai():
        move = request.json['move']

        # Perform move for player vs AI
        # Example: Update AI's move in the database and determine winner
        # Replace placeholders with actual MySQL queries
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='3rQ1eq0z1TLN',
                database='game_db'
            )
            cursor = connection.cursor()

            # Update AI's move in the database
            cursor.execute("UPDATE ai_table SET move = %s WHERE id = 1", (move,))
            connection.commit()

            # Get AI's move
            cursor.execute("SELECT move FROM ai_table WHERE id = 1")
            ai_move = cursor.fetchone()[0]

            # Determine winner using AI logic
            winner = ai_logic.calculate_winner(move, ai_move)

            # Reset AI's move
            cursor.execute("UPDATE ai_table SET move = NULL WHERE id = 1")
            connection.commit()

            return jsonify({'ai_move': ai_move, 'winner': winner})

        except mysql.connector.Error as e:
            return jsonify({'error': str(e)})

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # Function to make a move for player vs player
    @app.route('/make_move_player', methods=['POST'])
    def make_move_player():
        player = request.json['player']
        move = request.json['move']

        # Perform move for player vs player
        # Example: Update player's move in the database and determine winner
        # Replace placeholders with actual MySQL queries
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='3rQ1eq0z1TLN',
                database='game_db'
            )
            cursor = connection.cursor()

            # Update player's move in the database
            cursor.execute("UPDATE player_table SET move = %s WHERE id = %s", (move, player))
            connection.commit()

            # Check if both players have made their moves
            cursor.execute("SELECT move FROM player_table WHERE id = 1")
            player1_move = cursor.fetchone()[0]
            cursor.execute("SELECT move FROM player_table WHERE id = 2")
            player2_move = cursor.fetchone()[0]

            winner = None
            if player1_move is not None and player2_move is not None:
                # Determine winner using player logic
                winner = player_logic.calculate_winner(player1_move, player2_move)

                # Reset player moves
                cursor.execute("UPDATE player_table SET move = NULL WHERE id IN (1, 2)")
                connection.commit()

            return jsonify({'player1_move': player1_move, 'player2_move': player2_move, 'winner': winner})

        except mysql.connector.Error as e:
            return jsonify({'error': str(e)})

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

except mysql.connector.Error as e:
    print(f'Error connecting to MySQL database: {e}')

finally:
    # Closing the database connection
    if 'connection' in locals():
        connection.close()
        print('MySQL database connection closed')

# Create instances of mediator queue and game logic for AI
ai_mediator = Queue()
ai_logic = AiLogic(ai_mediator)

# Create instances of mediator queue and game logic for player
player_mediator = Queue()
player_logic = PlayerLogic(player_mediator)

# Define model and capture device outside of routes
model = load_model("../models/rock-paper-scissors-model.keras")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

# Define Flask routes for playing against AI
@app.route('/play_ai', methods=['GET'])
def play_ai():
    return render_template('player_v_ai.html', mode='ai')


@app.route('/play_ai', methods=['POST'])
def play_ai_post():
    mode = request.form.get('mode')
    if mode == 'ai':
        global model, cap
        model = load_model("../models/rock-paper-scissors-model.keras")
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
        # Initialize and start the game thread
        game_thread = GameThread(ai_mediator)
        game_thread.start()
        return redirect('/')
    else:
        return redirect('/')


# Define Flask routes for playing against another player
@app.route('/play_player', methods=['GET'])
def play_player():
    # Start the game thread when the route is accessed
    player_logic.start_game()
    return render_template('player_v_player.html')


# Define other Flask routes...


@app.route('/handle_move', methods=['POST'])
def handle_move():
    player1_move = request.form['player1_move']
    player2_move = request.form['player2_move']

    # Update the moves in the PlayerLogic instance
    player_mediator.put(player1_move)
    player_mediator.put(player2_move)

    # No need to determine winner here, as it will be handled by the PlayerLogic instance

    return redirect('/play_player')


# Define Flask routes
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', game_state=game.game_state)


# Define Flask routes
@app.route('/start', methods=['POST'])
def start():
    mode = request.form.get('mode')
    if mode == 'ai':
        ai_mediator.put('n')
    elif mode == 'player':
        player_mediator.put('n')
    return redirect('/')


@app.route('/reset', methods=['POST'])
def reset():
    mode = request.form.get('mode')
    if mode == 'ai':
        ai_mediator.put('r')
    elif mode == 'player':
        player_mediator.put('r')
    return redirect('/')


@app.route('/quit', methods=['POST'])
def stop():
    mode = request.form.get('mode')
    if mode == 'ai':
        ai_mediator.put('q')
    elif mode == 'player':
        player_mediator.put('q')
    return redirect('/')


# Define existing Flask routes
@app.route('/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})


@app.route('/create_game', methods=['POST'])
def create_game():
    user_id = request.json.get('user_id')
    new_game = Game(user_id=user_id)
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game created successfully'})


if __name__ == "__main__":
    app.run(debug=True)
