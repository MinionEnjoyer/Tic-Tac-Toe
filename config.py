"""
Configuration file for Tic-Tac-Toe Raspberry Pi Zero 2 W
GPIO pin assignments and hardware constants
"""

# GPIO Pin Assignments (BCM numbering)
# =====================================

# Button Input Pins (9 buttons for 9 grid positions)
# Buttons connect GPIO to GND when pressed (pull-up resistors enabled)
BUTTON_PINS = {
    0: 17,  # Top-Left
    1: 27,  # Top-Center
    2: 22,  # Top-Right
    3: 23,  # Mid-Left
    4: 24,  # Mid-Center
    5: 25,  # Mid-Right
    6: 5,   # Bottom-Left
    7: 6,   # Bottom-Center
    8: 13,  # Bottom-Right
}

# LED Matrix Data Pins (through SN74AHCT125N buffer)
# Each row of 3 matrices shares one data line
LED_DATA_PINS = {
    0: 12,  # Top row (matrices 0, 1, 2) - GPIO12 (PWM0)
    1: 18,  # Middle row (matrices 3, 4, 5) - GPIO18 (PWM0 alternate)
    2: 19,  # Bottom row (matrices 6, 7, 8) - GPIO19 (PWM1)
}

# Turn Indicator LED Pins
TURN_LED_PINS = {
    'X': 16,  # Red LED for Player X (GPIO16)
    'O': 20,  # Blue LED for Player O (GPIO20)
}

# LED Matrix Configuration
# ========================

# Each WS2812B matrix is 8x8 = 64 LEDs
LEDS_PER_MATRIX = 64

# 3 matrices per row
MATRICES_PER_ROW = 3

# Total LEDs per data line (row)
LEDS_PER_ROW = LEDS_PER_MATRIX * MATRICES_PER_ROW  # 192 LEDs

# LED brightness (0-255)
LED_BRIGHTNESS = 0.3  # 30% brightness to reduce power draw

# Button Configuration
# ====================

# Button debounce time in seconds
BUTTON_DEBOUNCE = 0.2

# Game Configuration
# ==================

# Colors for players (RGB format)
PLAYER_X_COLOR = (255, 0, 0)    # Red
PLAYER_O_COLOR = (0, 0, 255)    # Blue
EMPTY_COLOR = (0, 0, 0)         # Off
STARTUP_COLOR = (255, 255, 255) # White for startup text

# Animation timing
WIN_ANIMATION_DURATION = 3.0  # seconds
STARTUP_DISPLAY_DURATION = 2.5  # seconds
RESET_DELAY = 2.0  # seconds after win before reset

# Win celebration colors (rainbow)
WIN_COLORS = [
    (255, 0, 0),    # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (148, 0, 211),  # Violet
]
