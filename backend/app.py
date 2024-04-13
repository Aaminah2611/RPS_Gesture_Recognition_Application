import os

from flask import Flask, render_template, redirect, request, jsonify

from backend.game.Game import GameThread
from backend.game import Game
from queue import Queue
from backend.database import db, configure_db, User, Game, Participant

# Create instances of mediator queue and game logic
mediator = Queue()
game = GameThread(mediator)

# Create a Flask application
app = Flask(__name__)

app.template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))

# Configure the database connection
configure_db(app)

# Start the game thread
game.start()


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
        data = request.form.get()
        username = data.get('username')
        password = data.get('password')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}


@app.route('/create_game', methods=['POST'])
def create_game():
    user_id = request.form.get('user_id')
    user = db.session.query(User).get(user_id)
    new_game = Game()
    new_participant = Participant()
    user.participants.append(new_participant)
    new_game.participants.append(new_participant)
    db.session.add(new_game)
    db.session.add(new_participant)
    db.session.commit()
    return {'message': 'Game created successfully'}


# @app.route('/matchmaking', methods=['POST'])
# def matchmaking():
#     return 'Players matched successfully'


@app.route('/game/move', methods=['POST'])
def handle_move():
    return 'Move handled successfully'


# @app.route('/game/winner', methods=['POST'])
# def determine_winner():
#     return 'Winner determined successfully'

#
# @app.route('/player_vs_player', methods=['POST'])
# def player_vs_player():
#   return 'Player vs Player functionality added successfully'


if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True)
