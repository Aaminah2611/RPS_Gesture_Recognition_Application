# player_logic.py
from queue import Queue

class PlayerLogic:
    def __init__(self, mediator: Queue):
        self.mediator = mediator
        self.game_state = {
            'game_running': False,
            'player1_move': None,
            'player2_move': None,
            'winner': None
        }

    def start_game(self):
        self.game_state['game_running'] = True
        self.game_state['winner'] = None

    def stop_game(self):
        self.game_state['game_running'] = False

    def play_game(self):
        while self.game_state['game_running']:
            # Player 1 move
            player1_move = self.mediator.get()

            # Player 2 move
            player2_move = self.mediator.get()

            # Update game state
            self.game_state['player1_move'] = player1_move
            self.game_state['player2_move'] = player2_move

            # Calculate winner
            self.game_state['winner'] = PlayerLogic.calculate_winner(player1_move, player2_move)

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
