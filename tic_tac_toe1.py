import math
import random

# Step 1: Game Logic
class TicTacToe:
    def _init_(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

# Step 2: AI Opponent (Minimax Algorithm)
class TicTacToeAI:
    def _init_(self, letter):
        self.letter = letter

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())  # Random first move
        else:
            return self.minimax(game, self.letter)['position']

    def minimax(self, state, player):
        max_player = self.letter  # AI
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # Maximize
        else:
            best = {'position': None, 'score': math.inf}  # Minimize

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # Simulate game

            # Undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:  # Maximize
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:  # Minimize
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

# Step 3: Advisor System
class TicTacToeAdvisor:
    def _init_(self, letter):
        self.letter = letter

    def suggest_move(self, game):
        if len(game.available_moves()) == 9:
            return "Try starting in the center for the best chance to win!"
        else:
            best_move = self.minimax(game, self.letter)['position']
            return f"I suggest placing your {self.letter} in position {best_move}."

    def minimax(self, state, player):
        # Same as AI's minimax function
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

# Step 4: Playful Personality
class PlayfulPersonality:
    def _init_(self, name):
        self.name = name

    def taunt(self):
        return f"{self.name}: You're going down! 😈"

    def encourage(self):
        return f"{self.name}: You're doing great! Keep it up! 🎉"

    def celebrate(self):
        return f"{self.name}: I win! Better luck next time! 🏆"

    def console(self):
        return f"{self.name}: Don't worry, it's just a game! 😊"

# Step 5: Main Game Loop
def play(game, ai, advisor, personality):
    game.print_board()
    letter = 'X'  # Human starts
    while game.empty_squares():
        if letter == 'O':
            move = ai.get_move(game)
            game.make_move(move, letter)
            print(f"AI places an 'O' in position {move}")
        else:
            move = int(input("Your turn! Enter a position (0-8): "))
            game.make_move(move, letter)
            print(advisor.suggest_move(game))

        game.print_board()
        if game.current_winner:
            if letter == 'O':
                print(personality.celebrate())
            else:
                print(personality.console())
            break
        letter = 'O' if letter == 'X' else 'X'

# Initialize
game = TicTacToe()
ai = TicTacToeAI('O')
advisor = TicTacToeAdvisor('X')
personality = PlayfulPersonality("AI Opponent")

# Start Game
print("Welcome to Tic-Tac-Toe!")
print("Positions are numbered from 0 to 8, left to right, top to bottom.")
play(game, ai, advisor, personality)