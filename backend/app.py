from flask import Flask, render_template, redirect, request, jsonify
from game import Game
from queue import Queue
from database import db, configure_db, User, Game

# Create instances of mediator queue and game logic
mediator = Queue()
game = Game.Thread(mediator)

# Create a Flask application
app = Flask(__name__)

# Configure the database connection
configure_db(app)

# Define Flask routes
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', game_state=game.game_state)

@app.route('/start', methods=['POST'])
def start():
    mediator.put('n')
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    mediator.put('r')
    return redirect('/')

@app.route('/quit', methods=['POST'])
def stop():
    mediator.put('q')
    return redirect('/')

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
    new_game = Game(user_id_1=user_id)
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game created successfully'})

@app.route('/matchmaking', methods=['POST'])
def matchmaking():
    return 'Players matched successfully'

@app.route('/game/move', methods=['POST'])
def handle_move():
    return 'Move handled successfully'

@app.route('/game/winner', methods=['POST'])
def determine_winner():
    return 'Winner determined successfully'

@app.route('/player_vs_player', methods=['POST'])
def player_vs_player():
    return 'Player vs Player functionality added successfully'

if __name__ == "__main__":
    # Start the game thread
    game.start()
    # Run the Flask application
    app.run(debug=True)
