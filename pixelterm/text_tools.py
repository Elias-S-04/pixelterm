"""
pixelterm.text_tools
--------------------
Render text in the terminal using pixelterm with bitmap fonts.
"""

import os
from .renderer import PixelRenderer

# Compact 4x5 bitmap font (each character is 4 pixels wide, 5 pixels tall)
FONT_4x5 = {
    # A-Z
    'A': ["0110", "1001", "1111", "1001", "1001"],
    'B': ["1110", "1001", "1110", "1001", "1110"],
    'C': ["0111", "1000", "1000", "1000", "0111"],
    'D': ["1110", "1001", "1001", "1001", "1110"],
    'E': ["1111", "1000", "1110", "1000", "1111"],
    'F': ["1111", "1000", "1110", "1000", "1000"],
    'G': ["0111", "1000", "1011", "1001", "0111"],
    'H': ["1001", "1001", "1111", "1001", "1001"],
    'I': ["0111", "0010", "0010", "0010", "0111"],
    'J': ["0001", "0001", "0001", "1001", "0110"],
    'K': ["1001", "1010", "1100", "1010", "1001"],
    'L': ["1000", "1000", "1000", "1000", "1111"],
    'M': ["1001", "1111", "1111", "1001", "1001"],
    'N': ["1001", "1101", "1011", "1001", "1001"],
    'O': ["0110", "1001", "1001", "1001", "0110"],
    'P': ["1110", "1001", "1110", "1000", "1000"],
    'Q': ["0110", "1001", "1001", "1010", "0101"],
    'R': ["1110", "1001", "1110", "1010", "1001"],
    'S': ["0111", "1000", "0110", "0001", "1110"],
    'T': ["0111", "0010", "0010", "0010", "0010"],
    'U': ["1001", "1001", "1001", "1001", "0110"],
    'V': ["1001", "1001", "1001", "0110", "0100"],
    'W': ["1001", "1001", "1111", "1111", "1001"],
    'X': ["1001", "0110", "0100", "0110", "1001"],
    'Y': ["1001", "1001", "0110", "0010", "0100"],
    'Z': ["1111", "0001", "0010", "0100", "1111"],
    
    # 0-9
    '0': ["0110", "1001", "1001", "1001", "0110"],
    '1': ["0010", "0110", "0010", "0010", "0111"],
    '2': ["0110", "1001", "0010", "0100", "1111"],
    '3': ["1110", "0001", "0110", "0001", "1110"],
    '4': ["0001", "0011", "0101", "1111", "0001"],
    '5': ["1111", "1000", "1110", "0001", "1110"],
    '6': ["0110", "1000", "1110", "1001", "0110"],
    '7': ["1111", "0001", "0010", "0100", "0100"],
    '8': ["0110", "1001", "0110", "1001", "0110"],
    '9': ["0110", "1001", "0111", "0001", "0110"],
    
    # Symbols
    ' ': ["0000", "0000", "0000", "0000", "0000"],
    '.': ["0000", "0000", "0000", "0000", "1000"],
    '$': ["0110", "1010", "0110", "0000", "1111"],
    '%': ["0000", "1001", "0010", "0100", "1001"],
    '+': ["0000", "0100", "1110", "0100", "0000"],
    '-': ["0000", "0000", "1110", "0000", "0000"],
    ':': ["0000", "1000", "0000", "1000", "0000"],
    '!': ["0100", "0100", "0100", "0000", "0100"],
    '?': ["0110", "1001", "0010", "0000", "0100"],
    ',': ["0000", "0000", "0000", "0100", "1000"],
    ';': ["0000", "0100", "0000", "0100", "1000"],
    '/': ["0001", "0010", "0100", "1000", "0000"],
    '\\': ["1000", "0100", "0010", "0001", "0000"],
    '|': ["0100", "0100", "0100", "0100", "0100"],
    '(': ["0010", "0100", "0100", "0100", "0010"],
    ')': ["0100", "0010", "0010", "0010", "0100"],
    '[': ["0110", "0100", "0100", "0100", "0110"],
    ']': ["0110", "0010", "0010", "0010", "0110"],
    '<': ["0010", "0100", "1000", "0100", "0010"],
    '>': ["1000", "0100", "0010", "0100", "1000"],
    '=': ["0000", "1111", "0000", "1111", "0000"],
    '*': ["0000", "0100", "1110", "0100", "0000"],
    '#': ["0101", "1111", "0101", "1111", "0101"],
    '@': ["0110", "1011", "1011", "1000", "0111"],
    '&': ["0110", "1010", "0100", "1010", "0101"],
    '"': ["1010", "1010", "0000", "0000", "0000"],
    "'": ["0100", "0100", "0000", "0000", "0000"]
}

# Keep the old 5x7 font as backup (keeping existing format)
FONT_5x7 = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10011", "10001", "10001", "01110"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10101", "10101", "10011", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'X': ["10001", "01010", "00100", "00100", "00100", "01010", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    '3': ["11111", "00010", "00100", "00110", "00001", "10001", "01110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    '!': ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    '?': ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    '.': ["00000", "00000", "00000", "00000", "00000", "00000", "00100"],
    ',': ["00000", "00000", "00000", "00000", "00000", "00100", "01000"],
    ':': ["00000", "00000", "00100", "00000", "00000", "00100", "00000"],
    ';': ["00000", "00000", "00100", "00000", "00000", "00100", "01000"],
    '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    '=': ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    '/': ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    '\\': ["10000", "01000", "01000", "00100", "00010", "00010", "00001"],
    '|': ["00100", "00100", "00100", "00100", "00100", "00100", "00100"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '[': ["01110", "01000", "01000", "01000", "01000", "01000", "01110"],
    ']': ["01110", "00010", "00010", "00010", "00010", "00010", "01110"],
    '<': ["00010", "00100", "01000", "10000", "01000", "00100", "00010"],
    '>': ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
    '@': ["01110", "10001", "10101", "10111", "10100", "10000", "01111"],
    '#': ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
    '$': ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    '%': ["11000", "11001", "00010", "00100", "01000", "10011", "00011"],
    '&': ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    '*': ["00000", "00100", "10101", "01110", "10101", "00100", "00000"],
    '"': ["01010", "01010", "01010", "00000", "00000", "00000", "00000"],
    "'": ["00100", "00100", "00100", "00000", "00000", "00000", "00000"]
}


def _render_char(renderer, char, x, y, color, scale=1, font='4x5'):
    """Render a single character at position (x, y)."""
    char_upper = char.upper()
    
    # Select font
    if font == '5x7':
        font_data = FONT_5x7
        char_width = 5
    else:  # Default to 4x5
        font_data = FONT_4x5
        char_width = 4
    
    if char_upper not in font_data:
        char_upper = '?'  # Default to question mark for unknown chars
        if char_upper not in font_data:
            return  # Skip if question mark also not available
    
    char_bitmap = font_data[char_upper]
    
    for row_idx, row in enumerate(char_bitmap):
        for col_idx, pixel in enumerate(row):
            if pixel == '1':
                # Draw scaled pixel
                for sy in range(scale):
                    for sx in range(scale):
                        pixel_x = x + col_idx * scale + sx
                        pixel_y = y + row_idx * scale + sy
                        renderer.set_pixel(pixel_x, pixel_y, color)


def render_text(text, color=(255, 255, 255), scale=1, spacing=1, width=None, height=None, cell="██", font='4x5'):
    """
    Render text and return a PixelRenderer instance.
    
    Args:
        text (str): Text to render
        color (tuple): RGB color tuple (default: white)
        scale (int): Scale factor for text size (default: 1)
        spacing (int): Space between characters (default: 1)
        width (int): Renderer width (auto-calculated if None)
        height (int): Renderer height (auto-calculated if None)
        cell (str): Character to use for pixels (default: "██")
        font (str): Font to use ('4x5' or '5x7', default: '4x5')
    
    Returns:
        PixelRenderer: Configured renderer with text rendered
    """
    # Calculate dimensions based on font
    if font == '5x7':
        char_width = 5 * scale
        char_height = 7 * scale
    else:  # Default to 4x5
        char_width = 4 * scale
        char_height = 5 * scale
    
    if width is None:
        width = len(text) * (char_width + spacing) - spacing
        width = max(width, 1)  # Minimum width of 1
    
    if height is None:
        height = char_height
    
    # Create renderer
    renderer = PixelRenderer(width, height, cell)
    
    # Render each character
    x_pos = 0
    for char in text:
        if x_pos + char_width <= width:
            _render_char(renderer, char, x_pos, 0, color, scale, font)
        x_pos += char_width + spacing
    
    return renderer


def show_text(text, color=(255, 255, 255), scale=1, spacing=1, width=None, height=None, cell="██", font='4x5'):
    """
    Display text in the terminal.
    
    Args:
        text (str): Text to display
        color (tuple): RGB color tuple (default: white)
        scale (int): Scale factor for text size (default: 1)
        spacing (int): Space between characters (default: 1)
        width (int): Renderer width (auto-calculated if None)
        height (int): Renderer height (auto-calculated if None)
        cell (str): Character to use for pixels (default: "██")
        font (str): Font to use ('4x5' or '5x7', default: '4x5')
    """
    renderer = render_text(text, color, scale, spacing, width, height, cell, font)
    
    renderer.render()
    renderer.cleanup()


def show_multiline_text(lines, color=(255, 255, 255), scale=1, spacing=1, line_spacing=1, width=None, height=None, cell="██", font='4x5'):
    """
    Display multiple lines of text in the terminal.
    
    Args:
        lines (list): List of text lines to display
        color (tuple): RGB color tuple (default: white)
        scale (int): Scale factor for text size (default: 1)
        spacing (int): Space between characters (default: 1)
        line_spacing (int): Space between lines (default: 1)
        width (int): Renderer width (auto-calculated if None)
        height (int): Renderer height (auto-calculated if None)
        cell (str): Character to use for pixels (default: "██")
        font (str): Font to use ('4x5' or '5x7', default: '4x5')
    """
    # Calculate dimensions based on font
    if font == '5x7':
        char_width = 5 * scale
        char_height = 7 * scale
    else:  # Default to 4x5
        char_width = 4 * scale
        char_height = 5 * scale
    
    if width is None:
        max_line_length = max(len(line) for line in lines) if lines else 0
        width = max_line_length * (char_width + spacing) - spacing
        width = max(width, 1)
    
    if height is None:
        height = len(lines) * (char_height + line_spacing) - line_spacing
        height = max(height, char_height)
    
    # Create renderer
    renderer = PixelRenderer(width, height, cell)
    
    # Render each line
    y_pos = 0
    for line in lines:
        x_pos = 0
        for char in line:
            if x_pos + char_width <= width and y_pos + char_height <= height:
                _render_char(renderer, char, x_pos, y_pos, color, scale, font)
            x_pos += char_width + spacing
        y_pos += char_height + line_spacing
    
    renderer.render()
    renderer.cleanup()


def create_text_banner(text, color=(255, 255, 255), scale=2, border=True, border_color=(128, 128, 128), cell="██", font='4x5'):
    """
    Create a text banner with optional border.
    
    Args:
        text (str): Text for the banner
        color (tuple): Text color (default: white)
        scale (int): Text scale (default: 2)
        border (bool): Add border (default: True)
        border_color (tuple): Border color (default: gray)
        cell (str): Character to use for pixels (default: "██")
        font (str): Font to use ('4x5' or '5x7', default: '4x5')
    
    Returns:
        PixelRenderer: Configured renderer with banner
    """
    # Calculate text dimensions based on font
    if font == '5x7':
        char_width = 5 * scale
        char_height = 7 * scale
    else:  # Default to 4x5
        char_width = 4 * scale
        char_height = 5 * scale
    
    text_width = len(text) * (char_width + 1) - 1
    
    # Add border padding
    padding = 2 if border else 0
    banner_width = text_width + (padding * 2)
    banner_height = char_height + (padding * 2)
    
    # Create renderer
    renderer = PixelRenderer(banner_width, banner_height, cell)
    
    # Draw border
    if border:
        # Top and bottom borders
        for x in range(banner_width):
            renderer.set_pixel(x, 0, border_color)
            renderer.set_pixel(x, banner_height - 1, border_color)
        
        # Left and right borders
        for y in range(banner_height):
            renderer.set_pixel(0, y, border_color)
            renderer.set_pixel(banner_width - 1, y, border_color)
    
    # Render text
    x_pos = padding
    for char in text:
        if x_pos + char_width <= banner_width - padding:
            _render_char(renderer, char, x_pos, padding, color, scale, font)
        x_pos += char_width + 1
    
    return renderer


def show_banner(text, color=(255, 255, 255), scale=2, border=True, border_color=(128, 128, 128), cell="██", font='4x5'):
    """
    Display a text banner in the terminal.
    
    Args:
        text (str): Text for the banner
        color (tuple): Text color (default: white)
        scale (int): Text scale (default: 2)
        border (bool): Add border (default: True)
        border_color (tuple): Border color (default: gray)
        cell (str): Character to use for pixels (default: "██")
        font (str): Font to use ('4x5' or '5x7', default: '4x5')
    """
    renderer = create_text_banner(text, color, scale, border, border_color, cell, font)
    
    renderer.render()
    renderer.cleanup()