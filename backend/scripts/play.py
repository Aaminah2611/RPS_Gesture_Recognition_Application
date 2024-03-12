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
        if move2 == "scissors":
            return "User"
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return "User"
        if move2 == "scissors":
            return "Computer"

    if move1 == "scissors":
        if move2 == "paper":
            return "User"
        if move2 == "rock":
            return "Computer"


model = load_model("../models/rock-paper-scissors-model.keras")

cap = cv2.VideoCapture(0)

# Set the resolution to 640x480 (you can adjust this to your desired resolution)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

user_wins = 0
computer_wins = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

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
    pred = model.predict(np.array([img]))
    move_code = np.argmax(pred[0])
    user_move_name = mapper(move_code)

    # predict the winner (human vs computer)
    if user_move_name != "none":
        if user_wins < 2 and computer_wins < 2:
            computer_move_name = choice(['rock', 'paper', 'scissors'])
            winner = calculate_winner(user_move_name, computer_move_name)
            if winner == "User":
                user_wins += 1
            elif winner == "Computer":
                computer_wins += 1
        else:
            if user_wins == 2:
                winner = "User Wins!"
            elif computer_wins == 2:
                winner = "Computer Wins!"
            else:
                winner = "Tie"

    else:
        computer_move_name = "none"
        winner = "Waiting..."

    # Display computer's move image
    icon_path = "images/{}.png".format(computer_move_name)
    icon = cv2.imread(icon_path)
    if icon is not None and computer_move_name != "none":
        icon = cv2.resize(icon, (300, 300))
        frame[100:400, 600:900] = icon
    elif computer_move_name != "none":
        print("Error: Could not load image for", computer_move_name)

    # display the information
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Move: " + user_move_name,
                (50, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Computer's Move: " + computer_move_name,
                (550, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display "Winner" at the bottom center
    text_size = cv2.getTextSize("Winner: " + winner, font, 2, 4)[0]
    text_width = text_size[0]
    text_height = text_size[1]
    text_x = (frame.shape[1] - text_width) // 2
    text_y = frame.shape[0] - 50
    cv2.putText(frame, "Winner: " + winner,
                (text_x, text_y), font, 2, (0, 0, 255), 4, cv2.LINE_AA)

    cv2.imshow("Rock Paper Scissors", frame)

    k = cv2.waitKey(20)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
