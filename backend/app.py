import base64
import os
from flask import Flask, render_template, redirect, request, jsonify, Response
import cv2
import numpy as np

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
    user = db.session.get(User, user_id)
    new_game = Game()
    new_participant = Participant()
    user.participants.append(new_participant)
    new_game.participants.append(new_participant)
    db.session.add(new_game)
    db.session.commit()
    return {'message': 'Game created successfully'}


@app.route('/video_feed', methods=['POST'])
def video_feed():
    # Get the frame sent by the client
    frame_data = request.json.get('image_data')
    frame_bytes = frame_data.split(',')[1].encode('utf-8')
    frame_array = np.frombuffer(base64.b64decode(frame_bytes), dtype=np.uint8)
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    # Process the frame (Example: Convert to grayscale)
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform any additional processing here...

    # Return the processed frame as a response
    ret, jpeg = cv2.imencode('.jpg', processed_frame)
    return Response(response=jpeg.tobytes(), status=200, mimetype='image/jpeg')


@app.route('/game/move', methods=['POST'])
def handle_move():
    return 'Move handled successfully'


if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True)
