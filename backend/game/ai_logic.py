# ai_logic.py
from random import choice

class AiLogic:
    @staticmethod
    def play_ai_move():
        return choice(['rock', 'paper', 'scissors'])

    @staticmethod
    def calculate_winner(move1, move2):
        if move1 == move2:
            return "Tie"

        if move1 == "rock":
            return "Player 1" if move2 == "scissors" else "Player 2"

        if move1 == "paper":
            return "Player 1" if move2 == "rock" else "Player 2"

        if move1 == "scissors":
            return "Player 1" if move2 == "paper" else "Player 2"
