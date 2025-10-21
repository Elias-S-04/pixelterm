# pixelterm/renderer.py (only the two methods below)
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
        """Draw buffer in-place without scrolling or wrapping, for any size."""
        # Terminal geometry
        cols, rows = shutil.get_terminal_size(fallback=(80, 24))
        cell_w = len(self.cell)  # Use the cell string length directly
        
        # Account for terminal character aspect ratio (2:1 height:width)
        # Since terminal chars are ~2x taller, adjust height calculation
        max_px_w = max(1, cols // cell_w)
        max_px_h = max(1, rows * 2 // cell_w)  # Adjust for aspect ratio
        
        # Use same sampling to maintain square pixels
        max_fit = min(max_px_w, max_px_h)
        x_step = max(1, math.ceil(self.width / max_fit))
        y_step = max(1, math.ceil(self.height / max_fit))

        if self._first_render:
            sys.stdout.write("\033[?1049h\033[?25l\033[?7l")
            self._first_render = False

        sys.stdout.write("\033[H")
        drawn_rows = 0

        for sy in range(0, self.height, y_step):
            if drawn_rows >= rows:
                break
            sys.stdout.write(f"\033[{drawn_rows+1};1H")
            row = self.buffer[sy]

            line_parts = []
            used_cols = 0
            for sx in range(0, self.width, x_step):
                r, g, b = row[sx]
                seg = f"{rgb_to_ansi(r, g, b)}{self.cell}"
                if used_cols + cell_w > cols:
                    break
                line_parts.append(seg)
                used_cols += cell_w

            sys.stdout.write(''.join(line_parts) + "\033[0m")
            drawn_rows += 1

        for extra in range(drawn_rows, self._last_rows):
            if extra >= rows:
                break
            sys.stdout.write(f"\033[{extra+1};1H\033[0K")

        self._last_rows = drawn_rows
        sys.stdout.flush()

    def cleanup(self):
        """Restore terminal state even if animation was interrupted."""
        sys.stdout.write("\033[0m\033[?7h\033[?25h\033[?1049l\n")
        sys.stdout.flush()
