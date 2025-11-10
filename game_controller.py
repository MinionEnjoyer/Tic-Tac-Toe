"""
Game Controller for Tic-Tac-Toe
Implements game logic, win detection, and state management
"""

import time
from config import RESET_DELAY


class GameController:
    """Manages the Tic-Tac-Toe game logic and state."""
    
    # Winning line combinations (panel indices)
    WINNING_LINES = [
        # Rows
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        # Columns
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        # Diagonals
        [0, 4, 8],
        [2, 4, 6],
    ]
    
    def __init__(self):
        """Initialize the game controller."""
        self.board = [None] * 9  # None = empty, 'X' or 'O' for filled
        self.current_player = 'X'  # X always starts
        self.game_over = False
        self.winner = None
        self.winning_line = None
        print("Game controller initialized")
    
    def reset_game(self):
        """Reset the game to initial state."""
        print("Resetting game")
        self.board = [None] * 9
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_line = None
    
    def is_valid_move(self, panel_num):
        """
        Check if a move is valid.
        
        Args:
            panel_num: Panel number (0-8)
            
        Returns:
            True if the move is valid, False otherwise
        """
        if panel_num < 0 or panel_num > 8:
            return False
        
        if self.game_over:
            return False
        
        # Square must be empty
        return self.board[panel_num] is None
    
    def make_move(self, panel_num):
        """
        Make a move on the board.
        
        Args:
            panel_num: Panel number (0-8)
            
        Returns:
            True if move was successful, False otherwise
        """
        if not self.is_valid_move(panel_num):
            print(f"Invalid move: panel {panel_num}")
            return False
        
        # Place the symbol
        self.board[panel_num] = self.current_player
        print(f"Player {self.current_player} placed at panel {panel_num}")
        
        # Check for win or draw
        if self._check_win():
            self.game_over = True
            self.winner = self.current_player
            print(f"Player {self.current_player} wins!")
            return True
        
        if self._check_draw():
            self.game_over = True
            self.winner = None
            print("Game is a draw!")
            return True
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        print(f"Turn: Player {self.current_player}")
        
        return True
    
    def _check_win(self):
        """
        Check if the current player has won.
        
        Returns:
            True if current player won, False otherwise
        """
        for line in self.WINNING_LINES:
            if all(self.board[i] == self.current_player for i in line):
                self.winning_line = line
                return True
        return False
    
    def _check_draw(self):
        """
        Check if the game is a draw (all squares filled, no winner).
        
        Returns:
            True if game is a draw, False otherwise
        """
        return all(square is not None for square in self.board)
    
    def get_board_state(self):
        """
        Get the current board state.
        
        Returns:
            List of 9 elements, each is None, 'X', or 'O'
        """
        return self.board.copy()
    
    def get_current_player(self):
        """
        Get the current player.
        
        Returns:
            'X' or 'O'
        """
        return self.current_player
    
    def is_game_over(self):
        """
        Check if the game is over.
        
        Returns:
            True if game is over, False otherwise
        """
        return self.game_over
    
    def get_winner(self):
        """
        Get the winner of the game.
        
        Returns:
            'X', 'O', or None (for draw/game not over)
        """
        return self.winner
    
    def get_winning_line(self):
        """
        Get the winning line (if there is one).
        
        Returns:
            List of 3 panel indices, or None if no winner
        """
        return self.winning_line
    
    def is_draw(self):
        """
        Check if the game ended in a draw.
        
        Returns:
            True if draw, False otherwise
        """
        return self.game_over and self.winner is None
    
    def print_board(self):
        """Print the current board state to console (for debugging)."""
        print("\nCurrent Board:")
        for row in range(3):
            line = []
            for col in range(3):
                idx = row * 3 + col
                symbol = self.board[idx] if self.board[idx] else ' '
                line.append(symbol)
            print(f" {line[0]} | {line[1]} | {line[2]} ")
            if row < 2:
                print("-----------")
        print()
