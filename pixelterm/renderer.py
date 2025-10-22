"""Core pixel rendering functionality."""

import sys
from .colors import rgb_to_ansi


class PixelRenderer:
    """
    A terminal-based pixel renderer for creating graphics.
    
    Args:
        width (int): Width in pixels (default: 64)
        height (int): Height in pixels (default: 32)
        cell (str): Character(s) to use for each pixel (default: "██")
        use_alt_screen (bool): Use alternate screen buffer for animations (default: False)
    """
    
    def __init__(self, width=64, height=32, cell="██", use_alt_screen=False):
        self.width = width
        self.height = height
        self.buffer = [["UNSET" for _ in range(width)] for _ in range(height)]
        self._first_render = True
        self.cell = cell
        self.background_color = (0, 0, 0)
        self._background_enabled = False
        self.use_alt_screen = use_alt_screen
        self._in_alt_screen = False
        self._frame_count = 0

    def set_background(self, color):
        """Set background color and clear buffer to that color."""
        self.background_color = color
        self._background_enabled = True
        self.clear()

    def clear(self):
        """Clear all pixels to background or unset state."""
        fill_value = None if self._background_enabled else "UNSET"
        for y in range(self.height):
            for x in range(self.width):
                self.buffer[y][x] = fill_value

    def set_pixel(self, x, y, color):
        """Set a single pixel color."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = color

    def _render_frame_to_string(self):
        """Render current frame to a string."""
        frame_lines = []
        for y in range(self.height):
            row = self.buffer[y]
            line_parts = []
            for pixel in row:
                if pixel == "UNSET":
                    line_parts.append(" " * len(self.cell))
                elif pixel is None and self._background_enabled:
                    r, g, b = self.background_color
                    line_parts.append(f"{rgb_to_ansi(r,g,b)}{self.cell}")
                elif pixel is None:
                    line_parts.append(" " * len(self.cell))
                else:
                    r, g, b = pixel
                    line_parts.append(f"{rgb_to_ansi(r,g,b)}{self.cell}")
            frame_lines.append(''.join(line_parts) + "\033[0m ")
        return "\n".join(frame_lines)

    def render(self):
        """Render the pixel buffer to terminal."""
        if self._first_render:
            if self.use_alt_screen:
                sys.stdout.write("\033[?1049h\033[?25l\033[?7l")
                self._in_alt_screen = True
            else:
                sys.stdout.write("\033[?25l")
            self._first_render = False
        
        if self._in_alt_screen:
            sys.stdout.write("\033[H")
        elif self._frame_count > 0:
            sys.stdout.write(f"\033[{self.height}A")
        
        frame = self._render_frame_to_string()
        sys.stdout.write(frame)
        
        if not self._in_alt_screen:
            sys.stdout.write("\n")
        
        sys.stdout.flush()
        self._frame_count += 1

    def cleanup(self, preserve_final_frame=True):
        """Restore terminal state."""
        if self._in_alt_screen and preserve_final_frame:
            sys.stdout.write("\033[?1049l")
            self._in_alt_screen = False
            sys.stdout.write("\033[?25l")
            final_frame = self._render_frame_to_string()
            sys.stdout.write(final_frame)
            sys.stdout.write("\n\033[?25h")
        elif self._in_alt_screen:
            sys.stdout.write("\033[0m\033[?7h\033[?25h\033[?1049l")
        else:
            sys.stdout.write("\033[?25h")
        
        sys.stdout.flush()
