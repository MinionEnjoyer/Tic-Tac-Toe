#!/usr/bin/env python3
"""
Tic-Tac-Toe Game - Main Entry Point
Raspberry Pi Zero 2 W with WS2812B LED Matrices
"""

import sys
import time
import signal
from game_controller import GameController
from led_manager import LEDManager
from button_handler import ButtonHandler
from turn_indicator import TurnIndicator
from config import RESET_DELAY


class TicTacToeGame:
    """Main game class that coordinates all components."""
    
    def __init__(self):
        """Initialize all game components."""
        print("=" * 50)
        print("Tic-Tac-Toe Game - Initializing...")
        print("=" * 50)
        
        # Initialize components
        self.game = GameController()
        self.leds = LEDManager()
        self.turn_indicator = TurnIndicator()
        self.buttons = ButtonHandler(callback=self.on_button_press)
        
        # Flag to track if we're waiting for input
        self.waiting_for_input = False
        
        print("Initialization complete!")
    
    def on_button_press(self, panel_num):
        """
        Callback for button press events.
        
        Args:
            panel_num: Panel number (0-8) that was pressed
        """
        # Only process if we're waiting for input and game is not over
        if not self.waiting_for_input or self.game.is_game_over():
            return
        
        print(f"\nButton pressed: Panel {panel_num}")
        
        # Try to make the move
        if self.game.make_move(panel_num):
            # Valid move - update LED display
            current_player = self.game.get_board_state()[panel_num]
            self.leds.set_panel_symbol(panel_num, current_player)
            
            # Print board state for debugging
            self.game.print_board()
            
            # Check if game is over
            if self.game.is_game_over():
                self.handle_game_over()
            else:
                # Update turn indicator for next player
                self.turn_indicator.set_player(self.game.get_current_player())
        else:
            print("Invalid move - square already occupied!")
    
    def handle_game_over(self):
        """Handle game over state (win or draw)."""
        self.waiting_for_input = False
        
        if self.game.get_winner():
            # Someone won
            winner = self.game.get_winner()
            winning_line = self.game.get_winning_line()
            
            print(f"\n{'=' * 50}")
            print(f"Player {winner} WINS!")
            print(f"{'=' * 50}\n")
            
            # Flash winner's turn indicator
            self.turn_indicator.flash_winner(winner, times=5)
            
            # Animate winning line
            self.leds.animate_win(winning_line)
        else:
            # Draw
            print(f"\n{'=' * 50}")
            print("DRAW - No winner!")
            print(f"{'=' * 50}\n")
            
            # Animate draw
            self.leds.animate_draw()
        
        # Wait before resetting
        time.sleep(RESET_DELAY)
        
        # Reset for new game
        self.reset_game()
    
    def reset_game(self):
        """Reset the game for a new round."""
        print("\nResetting for new game...\n")
        
        # Reset game state
        self.game.reset_game()
        
        # Clear all LED matrices
        self.leds.clear_all()
        
        # Set turn indicator to Player X
        self.turn_indicator.set_player('X')
        
        # Ready to accept input again
        self.waiting_for_input = True
    
    def run(self):
        """Run the main game loop."""
        try:
            # Display startup sequence
            self.leds.display_startup_sequence()
            
            # Set initial turn indicator
            self.turn_indicator.set_player('X')
            
            # Start accepting input
            self.waiting_for_input = True
            
            print("\n" + "=" * 50)
            print("Game Ready! Player X starts.")
            print("Press any button to make your move.")
            print("=" * 50 + "\n")
            
            # Main game loop - just keep running and let callbacks handle everything
            while True:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\nGame interrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up all resources."""
        print("\nCleaning up...")
        self.leds.cleanup()
        self.turn_indicator.cleanup()
        self.buttons.cleanup()
        print("Cleanup complete. Goodbye!")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\nReceived shutdown signal")
    sys.exit(0)


def main():
    """Main entry point."""
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create and run game
    game = TicTacToeGame()
    game.run()


if __name__ == "__main__":
    main()
