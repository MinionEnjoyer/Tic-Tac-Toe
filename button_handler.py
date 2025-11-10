"""
Button Input Handler for Tic-Tac-Toe Game
Handles button press detection with debouncing
"""

import RPi.GPIO as GPIO
import time
from config import BUTTON_PINS, BUTTON_DEBOUNCE


class ButtonHandler:
    """Manages button input detection with debouncing."""
    
    def __init__(self, callback=None):
        """
        Initialize button handler.
        
        Args:
            callback: Function to call when button is pressed, receives panel_num
        """
        self.callback = callback
        self.last_press_time = {}
        
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        
        # Configure all button pins as inputs with pull-up resistors
        for panel_num, pin in BUTTON_PINS.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.last_press_time[panel_num] = 0
            
            # Add event detection for button press (falling edge = button press)
            GPIO.add_event_detect(
                pin,
                GPIO.FALLING,
                callback=self._button_callback,
                bouncetime=int(BUTTON_DEBOUNCE * 1000)  # Convert to milliseconds
            )
        
        print("Button handler initialized")
    
    def _button_callback(self, channel):
        """
        Internal callback for GPIO event detection.
        
        Args:
            channel: GPIO pin number that triggered the event
        """
        # Find which panel number this pin corresponds to
        panel_num = None
        for num, pin in BUTTON_PINS.items():
            if pin == channel:
                panel_num = num
                break
        
        if panel_num is None:
            return
        
        # Check debounce time
        current_time = time.time()
        if current_time - self.last_press_time[panel_num] < BUTTON_DEBOUNCE:
            return
        
        self.last_press_time[panel_num] = current_time
        
        # Call the user callback if set
        if self.callback:
            self.callback(panel_num)
    
    def wait_for_button(self):
        """
        Wait for any button press and return the panel number.
        Blocking call.
        
        Returns:
            Panel number (0-8) of the pressed button
        """
        pressed_panel = [None]  # Use list to allow modification in nested function
        
        def temp_callback(panel_num):
            pressed_panel[0] = panel_num
        
        # Temporarily override callback
        old_callback = self.callback
        self.callback = temp_callback
        
        # Wait for button press
        while pressed_panel[0] is None:
            time.sleep(0.01)
        
        # Restore old callback
        self.callback = old_callback
        
        return pressed_panel[0]
    
    def is_button_pressed(self, panel_num):
        """
        Check if a specific button is currently pressed.
        
        Args:
            panel_num: Panel number (0-8) to check
            
        Returns:
            True if button is pressed, False otherwise
        """
        pin = BUTTON_PINS.get(panel_num)
        if pin is None:
            return False
        
        # Button is pressed when pin reads LOW (pulled to ground)
        return GPIO.input(pin) == GPIO.LOW
    
    def cleanup(self):
        """Clean up GPIO resources."""
        print("Cleaning up button handler")
        GPIO.cleanup()
