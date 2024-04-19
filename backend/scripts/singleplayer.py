from keras.models import load_model
import cv2
import numpy as np
from random import choice

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
        return "Human" if move2 == "scissors" else "Computer"

    if move1 == "paper":
        return "Human" if move2 == "rock" else "Computer"

    if move1 == "scissors":
        return "Human" if move2 == "paper" else "Computer"


def display_moves(frame, human_move_name, computer_move_name, winner):
    # Display computer's move image
    icon_path = f"../images/{computer_move_name}.png"
    icon = cv2.imread(icon_path)
    if icon is not None and computer_move_name != "none":
        icon = cv2.resize(icon, (300, 300))
        frame[100:400, 600:900] = icon
    elif computer_move_name != "none":
        print("Error: Could not load image for", computer_move_name)

    # Display the information
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f"Your Move: {human_move_name}", (50, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Computer's Move: {computer_move_name}", (550, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display "Winner" at the bottom center
    text_size = cv2.getTextSize(f"Winner: {winner}", font, 2, 4)[0]
    text_width = text_size[0]
    text_height = text_size[1]
    text_x = (frame.shape[1] - text_width) // 2
    text_y = frame.shape[0] - 50
    cv2.putText(frame, f"Winner: {winner}", (text_x, text_y), font, 2, (0, 0, 255), 4, cv2.LINE_AA)


def play_game(cap, model):
    human_wins = 0
    computer_wins = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)

        # Rectangle for Human to play (left side)
        cv2.rectangle(frame, (100, 100), (400, 400), (255, 255, 255), 2)

        # Rectangle for computer to play (right side)
        cv2.rectangle(frame, (600, 100), (900, 400), (255, 255, 255), 2)

        # extract the region of image within the Human rectangle
        roi = frame[100:400, 100:400]
        img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))

        # predict the move made
        pred = model.predict(np.array([img]))
        move_code = np.argmax(pred[0])
        human_move_name = mapper(move_code)

        # predict the winner (human vs computer)
        if human_move_name != "none":
            if human_wins < 2 and computer_wins < 2:
                computer_move_name = choice(['rock', 'paper', 'scissors'])
                winner = calculate_winner(human_move_name, computer_move_name)
                if winner == "Human":
                    human_wins += 1
                elif winner == "Computer":
                    computer_wins += 1
            else:
                winner = "Human Wins!" if human_wins == 2 else "Computer Wins!" if computer_wins == 2 else "Tie"
        else:
            computer_move_name = "none"
            winner = "Waiting..."

        display_moves(frame, human_move_name, computer_move_name, winner)

        cv2.imshow("Rock Paper Scissors", frame)

        k = cv2.waitKey(20)
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    model = load_model("../../keras/rock-paper-scissors-model.keras")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    play_game(cap, model)
