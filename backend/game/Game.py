import os
import signal
from threading import Thread
from queue import Queue
import dataclasses
from typing import Optional
from time import sleep
from keras.models import load_model
import cv2
import numpy as np
from random import choice


# Holds the game state. Flask will get this and use it to display things on the UI
@dataclasses.dataclass
class GameState:
    stage: Optional[str] = None
    game_running: bool = False
    user_wins: int = 0
    computer_wins: int = 0
    user_move_name: Optional[str] = None
    computer_move_name: Optional[str] = None
    winner: Optional[str] = None


# Separate background thread to run the game independently of Flask.
class GameThread(Thread):
    _game_state: GameState

    @property
    def game_state(self) -> GameState:
        return self._game_state

    def __init__(self, mediator: Queue):
        super().__init__()
        self.mediator = mediator
        self._game_state = GameState(game_running=False)
        self.model = load_model("../keras/rock-paper-scissors-model.keras")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

    # Called when the Thread is started
    def run(self):
        # Game loop to run until 'q' is sent
        self.game_loop()

        # OS kill signal to shut down the Flask app
        os.kill(os.getpid(), signal.SIGINT)

    def game_loop(self):
        while True:
            next_command = self.mediator.get()

            if next_command == 'n':
                if not self._game_state.game_running:
                    self.new_game()
            if next_command == 'r':
                self._game_state = GameState()
            elif next_command == 'q':
                # break the loop
                break

            if self._game_state.game_running:
                self.play_game()

    def new_game(self):
        self._game_state = GameState(game_running=True)
        self._game_state.stage = 'player1 turn'

    def play_game(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)

        # Rectangle for user to play (left side)
        cv2.rectangle(frame, (100, 100), (400, 400), (255, 255, 255), 2)

        # Rectangle for computer to play (right side)
        cv2.rectangle(frame, (600, 100), (900, 400), (255, 255, 255), 2)

        # extract the region of image within the user rectangle
        roi = frame[100:400, 100:400]
        img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))

        # predict the move made
        pred = self.model.predict(np.array([img]))
        move_code = np.argmax(pred[0])
        self._game_state.user_move_name = mapper(move_code)

        # predict the winner (human vs computer)
        if self._game_state.user_move_name != "none":
            if self._game_state.user_wins < 2 and self._game_state.computer_wins < 2:
                self._game_state.computer_move_name = choice(['rock', 'paper', 'scissors'])
                self._game_state.winner = calculate_winner(self._game_state.user_move_name,
                                                           self._game_state.computer_move_name)
                if self._game_state.winner == "User":
                    self._game_state.user_wins += 1
                elif self._game_state.winner == "Computer":
                    self._game_state.computer_wins += 1
            else:
                self._game_state.winner = "User Wins!" if self._game_state.user_wins == 2 else "Computer Wins!" if self._game_state.computer_wins == 2 else "Tie"
        else:
            self._game_state.computer_move_name = "none"
            self._game_state.winner = "Waiting..."

        display_moves(frame, self._game_state.user_move_name, self._game_state.computer_move_name,
                      self._game_state.winner)

    def stop_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()


REV_CLASS_MAP = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none"
}


def mapper(val):
    return REV_CLASS_MAP[val]


def calculate_winner(move1, move2):
    if move1 == move2:
        return "Tie"

    if move1 == "rock":
        return "User" if move2 == "scissors" else "Computer"

    if move1 == "paper":
        return "User" if move2 == "rock" else "Computer"

    if move1 == "scissors":
        return "User" if move2 == "paper" else "Computer"


def display_moves(frame, user_move_name, computer_move_name, winner):
    # Display computer's move image
    icon_path = f"images/{computer_move_name}.png"
    icon = cv2.imread(icon_path)
    if icon is not None and computer_move_name != "none":
        icon = cv2.resize(icon, (300, 300))
        frame[100:400, 600:900] = icon
    elif computer_move_name != "none":
        print("Error: Could not load image for", computer_move_name)

    # Display the information
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f"Your Move: {user_move_name}", (50, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Computer's Move: {computer_move_name}", (550, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display "Winner" at the bottom center
    text_size = cv2.getTextSize(f"Winner: {winner}", font, 2, 4)[0]
    text_width = text_size[0]
    text_height = text_size[1]
    text_x = (frame.shape[1] - text_width) // 2
    text_y = frame.shape[0] - 50
    cv2.putText(frame, f"Winner: {winner}", (text_x, text_y), font, 2, (0, 0, 255), 4, cv2.LINE_AA)
