"""
LED Matrix Manager for Tic-Tac-Toe Game
Controls 9 WS2812B 8x8 LED matrices using NeoPixel library
"""

import board
import neopixel
import time
from config import (
    LED_DATA_PINS, LEDS_PER_ROW, LEDS_PER_MATRIX,
    PLAYER_X_COLOR, PLAYER_O_COLOR, EMPTY_COLOR,
    STARTUP_COLOR, WIN_COLORS, LED_BRIGHTNESS
)
from patterns import get_pattern, pattern_to_pixel_indices, get_all_pixels


class LEDManager:
    """Manages all LED matrix operations for the Tic-Tac-Toe game."""
    
    def __init__(self):
        """Initialize NeoPixel strips for all three rows of matrices."""
        # Map GPIO pin numbers to board pin objects
        pin_map = {
            12: board.D12,
            18: board.D18,
            19: board.D19,
        }
        
        # Create NeoPixel strips for each row
        self.strips = {}
        for row_num, gpio_pin in LED_DATA_PINS.items():
            self.strips[row_num] = neopixel.NeoPixel(
                pin_map[gpio_pin],
                LEDS_PER_ROW,
                brightness=LED_BRIGHTNESS,
                auto_write=False,
                pixel_order=neopixel.GRB
            )
        
        # Clear all LEDs on initialization
        self.clear_all()
    
    def _get_strip_and_offset(self, panel_num):
        """
        Get the NeoPixel strip and LED offset for a given panel number.
        
        Args:
            panel_num: Panel number (0-8)
            
        Returns:
            Tuple of (strip, offset) where offset is the starting LED index
        """
        row = panel_num // 3  # 0, 1, or 2
        col = panel_num % 3   # 0, 1, or 2
        strip = self.strips[row]
        offset = col * LEDS_PER_MATRIX
        return strip, offset
    
    def set_panel_pattern(self, panel_num, pattern, color):
        """
        Display a pattern on a specific panel.
        
        Args:
            panel_num: Panel number (0-8)
            pattern: 8x8 array where 1 = LED on, 0 = LED off
            color: RGB tuple (r, g, b)
        """
        if pattern is None:
            return
        
        strip, offset = self._get_strip_and_offset(panel_num)
        pixel_indices = pattern_to_pixel_indices(pattern)
        
        # Clear the panel first
        for i in range(LEDS_PER_MATRIX):
            strip[offset + i] = EMPTY_COLOR
        
        # Set the pattern pixels
        for pixel_idx in pixel_indices:
            strip[offset + pixel_idx] = color
        
        strip.show()
    
    def set_panel_symbol(self, panel_num, symbol):
        """
        Display X or O symbol on a panel.
        
        Args:
            panel_num: Panel number (0-8)
            symbol: 'X' or 'O'
        """
        pattern = get_pattern(symbol)
        color = PLAYER_X_COLOR if symbol == 'X' else PLAYER_O_COLOR
        self.set_panel_pattern(panel_num, pattern, color)
    
    def clear_panel(self, panel_num):
        """
        Clear all LEDs on a specific panel.
        
        Args:
            panel_num: Panel number (0-8)
        """
        strip, offset = self._get_strip_and_offset(panel_num)
        for i in range(LEDS_PER_MATRIX):
            strip[offset + i] = EMPTY_COLOR
        strip.show()
    
    def clear_all(self):
        """Clear all LEDs on all panels."""
        for strip in self.strips.values():
            strip.fill(EMPTY_COLOR)
            strip.show()
    
    def display_startup_sequence(self):
        """Display 'TIC TAC TOE' text across all panels."""
        print("Displaying startup sequence: TIC TAC TOE")
        
        # Display each letter on its corresponding panel
        for panel_num in range(9):
            pattern = get_pattern(panel_num)
            self.set_panel_pattern(panel_num, pattern, STARTUP_COLOR)
            time.sleep(0.1)  # Small delay between each panel
        
        # Hold the display
        time.sleep(2.5)
        
        # Fade out effect
        for brightness in range(10, 0, -1):
            for row_strip in self.strips.values():
                row_strip.brightness = LED_BRIGHTNESS * (brightness / 10)
                row_strip.show()
            time.sleep(0.1)
        
        # Reset brightness and clear
        for row_strip in self.strips.values():
            row_strip.brightness = LED_BRIGHTNESS
        self.clear_all()
        print("Startup sequence complete")
    
    def animate_win(self, winning_line):
        """
        Display a celebration animation for the winning line.
        
        Args:
            winning_line: List of 3 panel numbers that form the winning line
        """
        print(f"Animating win for panels: {winning_line}")
        
        # Rainbow chase effect on winning panels
        for cycle in range(3):  # 3 complete rainbow cycles
            for color_idx, color in enumerate(WIN_COLORS):
                for panel_num in winning_line:
                    strip, offset = self._get_strip_and_offset(panel_num)
                    # Fill entire panel with current rainbow color
                    for i in range(LEDS_PER_MATRIX):
                        strip[offset + i] = color
                    strip.show()
                time.sleep(0.15)
        
        # Flash effect
        for _ in range(4):
            # All winning panels bright white
            for panel_num in winning_line:
                strip, offset = self._get_strip_and_offset(panel_num)
                for i in range(LEDS_PER_MATRIX):
                    strip[offset + i] = (255, 255, 255)
                strip.show()
            time.sleep(0.2)
            
            # Turn off
            for panel_num in winning_line:
                self.clear_panel(panel_num)
            time.sleep(0.2)
    
    def animate_draw(self):
        """Display an animation for a draw/tie game."""
        print("Animating draw")
        
        # Pulse all panels with purple color
        for _ in range(3):
            # Fade in
            for brightness in range(0, 11):
                for panel_num in range(9):
                    strip, offset = self._get_strip_and_offset(panel_num)
                    color = tuple(int(c * brightness / 10) for c in (128, 0, 128))
                    for i in range(LEDS_PER_MATRIX):
                        strip[offset + i] = color
                    strip.show()
                time.sleep(0.05)
            
            # Fade out
            for brightness in range(10, -1, -1):
                for panel_num in range(9):
                    strip, offset = self._get_strip_and_offset(panel_num)
                    color = tuple(int(c * brightness / 10) for c in (128, 0, 128))
                    for i in range(LEDS_PER_MATRIX):
                        strip[offset + i] = color
                    strip.show()
                time.sleep(0.05)
    
    def cleanup(self):
        """Clean up resources and turn off all LEDs."""
        print("Cleaning up LED manager")
        self.clear_all()
        for strip in self.strips.values():
            strip.deinit()
