# pixelterm/colors.py
def rgb_to_ansi(r, g, b):
    # Convert an RGB tuple to an ANSI escape color string.
    return f"\033[38;2;{r};{g};{b}m"

COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
}
