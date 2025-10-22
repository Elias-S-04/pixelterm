# pixelterm/renderer.py
import sys, shutil, math
from .colors import rgb_to_ansi

class PixelRenderer:
    def __init__(self, width=64, height=32, cell="██"):
        self.width = width
        self.height = height
        self.buffer = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
        self._first_render = True
        self._last_rows = 0
        self.cell = cell   # pixel size determined by string length

    def clear(self, color=(0, 0, 0)):
        """Fill the screen with one color."""
        for y in range(self.height):
            for x in range(self.width):
                self.buffer[y][x] = color

    def set_pixel(self, x, y, color):
        """Set a single pixel color."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = color

    def render(self):
        """Render exactly width × height pixels, independent of terminal size."""
        if self._first_render:
            sys.stdout.write("\033[?1049h\033[?25l\033[?7l")  # alt screen + hide cursor + disable wrap
            self._first_render = False
    
        sys.stdout.write("\033[H")  # move cursor to top-left
        frame_lines = []
    
        # Build the entire frame in memory first (avoids flicker)
        for y in range(self.height):
            row = self.buffer[y]
            line = ''.join(f"{rgb_to_ansi(r,g,b)}{self.cell}" for (r,g,b) in row)
            frame_lines.append(line + "\033[0m")
    
        frame = "\n".join(frame_lines)
        sys.stdout.write(frame)
        sys.stdout.flush()

    def cleanup(self):
        """Restore terminal state even if animation was interrupted."""
        sys.stdout.write("\033[0m\033[?7h\033[?25h\033[?1049l\n")
        sys.stdout.flush()
