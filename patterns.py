"""
LED patterns for 8x8 matrices
Defines X, O, and letter patterns for the Tic-Tac-Toe game
"""

# Pattern format: 8x8 grid where 1 = LED on, 0 = LED off
# Each row is read left to right, top to bottom

# X Pattern (diagonal cross)
PATTERN_X = [
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
]

# O Pattern (circle)
PATTERN_O = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
]

# Letter patterns for "TIC TAC TOE" startup display
# T pattern
PATTERN_T = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
]

# I pattern
PATTERN_I = [
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
]

# C pattern
PATTERN_C = [
    [0, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 0],
]

# A pattern
PATTERN_A = [
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
]

# E pattern
PATTERN_E = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

# Map panel positions to letters for "TIC TAC TOE"
STARTUP_LETTERS = {
    0: PATTERN_T,  # Top-Left: T
    1: PATTERN_I,  # Top-Center: I
    2: PATTERN_C,  # Top-Right: C
    3: PATTERN_T,  # Mid-Left: T
    4: PATTERN_A,  # Mid-Center: A
    5: PATTERN_C,  # Mid-Right: C
    6: PATTERN_T,  # Bottom-Left: T
    7: PATTERN_O,  # Bottom-Center: O
    8: PATTERN_E,  # Bottom-Right: E
}


def get_pattern(symbol):
    """
    Get the LED pattern for a given symbol.
    
    Args:
        symbol: 'X', 'O', or panel number (0-8) for startup letters
        
    Returns:
        8x8 pattern array or None if invalid
    """
    if symbol == 'X':
        return PATTERN_X
    elif symbol == 'O':
        return PATTERN_O
    elif isinstance(symbol, int) and 0 <= symbol <= 8:
        return STARTUP_LETTERS.get(symbol)
    return None


def pattern_to_pixel_indices(pattern):
    """
    Convert an 8x8 pattern to a list of pixel indices that should be lit.
    
    Args:
        pattern: 8x8 array where 1 = LED on, 0 = LED off
        
    Returns:
        List of pixel indices (0-63) that should be illuminated
    """
    indices = []
    for row in range(8):
        for col in range(8):
            if pattern[row][col] == 1:
                # Convert 2D position to 1D index
                # Assuming row-major order (left to right, top to bottom)
                index = row * 8 + col
                indices.append(index)
    return indices


def get_all_pixels():
    """
    Get indices for all pixels in an 8x8 matrix.
    
    Returns:
        List of all pixel indices (0-63)
    """
    return list(range(64))
