"""
Turn Indicator LED Controller
Controls red and blue LEDs to show which player's turn it is
"""

import RPi.GPIO as GPIO
from config import TURN_LED_PINS


class TurnIndicator:
    """Manages the turn indicator LEDs (red for X, blue for O)."""
    
    def __init__(self):
        """Initialize turn indicator LEDs."""
        # GPIO should already be set up by ButtonHandler
        # But we set mode again in case this is used standalone
        GPIO.setmode(GPIO.BCM)
        
        # Configure LED pins as outputs
        for player, pin in TURN_LED_PINS.items():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)  # Start with LEDs off
        
        print("Turn indicator initialized")
    
    def set_player(self, player):
        """
        Set the turn indicator to show the current player.
        
        Args:
            player: 'X' or 'O'
        """
        if player == 'X':
            # Turn on red LED, turn off blue LED
            GPIO.output(TURN_LED_PINS['X'], GPIO.HIGH)
            GPIO.output(TURN_LED_PINS['O'], GPIO.LOW)
            print("Turn indicator: Player X (Red)")
        elif player == 'O':
            # Turn on blue LED, turn off red LED
            GPIO.output(TURN_LED_PINS['X'], GPIO.LOW)
            GPIO.output(TURN_LED_PINS['O'], GPIO.HIGH)
            print("Turn indicator: Player O (Blue)")
    
    def flash_winner(self, player, times=5):
        """
        Flash the winning player's LED.
        
        Args:
            player: 'X' or 'O'
            times: Number of times to flash
        """
        import time
        
        pin = TURN_LED_PINS.get(player)
        if pin is None:
            return
        
        print(f"Flashing winner: Player {player}")
        for _ in range(times):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.2)
    
    def turn_off_all(self):
        """Turn off both indicator LEDs."""
        for pin in TURN_LED_PINS.values():
            GPIO.output(pin, GPIO.LOW)
        print("Turn indicators off")
    
    def cleanup(self):
        """Clean up by turning off all LEDs."""
        print("Cleaning up turn indicator")
        self.turn_off_all()
