from keras.models import load_model
import cv2
import numpy as np
from random import choice
from time import sleep
from typing import Optional

GESTURE_ROCK = "rock"
GESTURE_PAPER = "paper"
GESTURE_SCISSORS = "scissors"
GESTURE_NONE = "none"

REV_CLASS_MAP = {
    0: GESTURE_ROCK,
    1: GESTURE_PAPER,
    2: GESTURE_SCISSORS,
    3: GESTURE_NONE
}

PLAYER_1_CAMERA = 0
PLAYER_2_CAMERA = 1

PLAYER_1_ID = "Player 1"
PLAYER_2_ID = "Player 2"


def mapper(val: int) -> str:
    return REV_CLASS_MAP[val]


def calculate_winner(move1: str, move2: str) -> str:
    if move1 == GESTURE_NONE or move2 == GESTURE_NONE:
        return GESTURE_NONE

    if move1 == move2:
        return "Tie"

    if move1 == GESTURE_ROCK:
        return PLAYER_1_ID if move2 == GESTURE_SCISSORS else PLAYER_2_ID

    if move1 == GESTURE_PAPER:
        return PLAYER_1_ID if move2 == GESTURE_ROCK else PLAYER_2_ID

    if move1 == GESTURE_SCISSORS:
        return PLAYER_1_ID if move2 == GESTURE_PAPER else PLAYER_2_ID


class PlayerFrame:
    def __init__(self, frame, player_id):
        self._frame = frame
        self._player_id = player_id

    def add_moves(self, user_move_name, opponent_move_name, winner):
        # Display computer's move image
        icon_path = f"images/{opponent_move_name}.png"
        icon = cv2.imread(icon_path)
        if icon is not None and opponent_move_name != GESTURE_NONE:
            icon = cv2.resize(icon, (300, 300))
            self._frame[100:400, 600:900] = icon
        elif opponent_move_name != GESTURE_NONE:
            print("Error: Could not load image for", opponent_move_name)

        # Display the information
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self._frame, f"Your Move: {user_move_name}", (50, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self._frame, f"Opponent's Move: {opponent_move_name}", (550, 70), font, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)

        # Display "Winner" at the bottom center
        text_size = cv2.getTextSize(f"Winner: {winner}", font, 2, 4)[0]
        text_width = text_size[0]
        text_height = text_size[1]
        text_x = (self._frame.shape[1] - text_width) // 2
        text_y = self._frame.shape[0] - 50
        cv2.putText(self._frame, f"Winner: {winner}", (text_x, text_y), font, 2, (0, 0, 255), 4, cv2.LINE_AA)

        cv2.imshow(self._player_id, self._frame)

    def get_img(self):
        # extract the region of image within the user rectangle
        roi = self._frame[100:400, 100:400]
        img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))
        return img


class PlayerCapture:
    def __init__(self, camera_number: int, player_id):
        self._camera_number = camera_number
        self._player_id = player_id
        self._cap = cv2.VideoCapture(camera_number)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

    def read(self) -> Optional[PlayerFrame]:
        player_frame = None
        ret, frame = self._cap.read()
        if not ret:
            player_number = self._camera_number + 1
            print(f"No frame captured for {self._player_id}. (Camera number {self._camera_number}).")
            sleep(20)
        else:
            frame = cv2.flip(frame, 1)

            # Rectangle for this player (left side)
            cv2.rectangle(frame, (100, 100), (400, 400), (255, 255, 255), 2)

            # Rectangle for other player (right side)
            cv2.rectangle(frame, (600, 100), (900, 400), (255, 255, 255), 2)

            player_frame = PlayerFrame(frame, self._player_id)

        return player_frame

    def release(self):
        self._cap.release()


class RockPaperScissorsModel:
    def __init__(self, path_to_keras_model: str):
        self._model = load_model(path_to_keras_model)

    def predict_gesture(self, frame: PlayerFrame) -> str:
        # predict the move made
        img = frame.get_img()
        pred = self._model.predict(np.array([img]))
        move_code = np.argmax(pred[0])
        return mapper(move_code)


def decide_computer_move(user_move_name: str) -> str:
    if user_move_name != GESTURE_NONE:
        return choice([GESTURE_ROCK, GESTURE_PAPER, GESTURE_SCISSORS])
    else:
        return GESTURE_NONE


def play_game(model: RockPaperScissorsModel, player1_cap: PlayerCapture, player2_cap: PlayerCapture):
    player1_wins = 0
    player2_wins = 0

    while True:
        player1_frame = player1_cap.read()
        if player1_frame is None:
            continue

        player2_frame = player2_cap.read()
        if player2_frame is None:
            continue

        player1_gesture = model.predict_gesture(player1_frame)
        player2_gesture = model.predict_gesture(player2_frame)
        winner = calculate_winner(player1_gesture, player2_gesture)

        # predict the winner (player1 vs player2)
        if winner != GESTURE_NONE:
            if player1_wins < 2 and player2_wins < 2:
                if winner == PLAYER_1_ID:
                    player1_wins += 1
                elif winner == PLAYER_2_ID:
                    player2_wins += 1
            else:
                winner = f"{PLAYER_1_ID} Wins!" \
                    if player1_wins == 2 else f"{PLAYER_2_ID} Wins!" \
                    if player2_wins == 2 else "Tie"
        else:
            winner = "Waiting..."

        player1_frame.display_moves(player1_gesture, player2_gesture, winner)
        player2_frame.display_moves(player2_gesture, player1_gesture, winner)

        k = cv2.waitKey(20)
        if k == ord('q'):
            return


def main():
    model = RockPaperScissorsModel("../../keras/rock-paper-scissors-model.keras")
    player1_cap = PlayerCapture(camera_number=PLAYER_1_CAMERA, player_id=PLAYER_1_ID)
    player2_cap = PlayerCapture(camera_number=PLAYER_2_CAMERA, player_id=PLAYER_2_ID)

    play_game(model, player1_cap, player2_cap)

    player1_cap.release()
    player2_cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

