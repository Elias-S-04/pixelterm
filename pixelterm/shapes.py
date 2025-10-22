# pixelterm/shapes.py
def draw_line(renderer, x1, y1, x2, y2, color):
    """Draw a simple line using Bresenham's algorithm."""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        renderer.set_pixel(x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_circle(renderer, cx, cy, radius, color, filled=False):
    """
    Draw a circle using Bresenham's circle algorithm.
    If filled=True, fills the circle by drawing horizontal lines between edges.
    """
    x = 0
    y = radius
    d = 3 - 2 * radius

    while y >= x:
        if filled:
            # Fill between symmetric points
            _draw_filled_circle_lines(renderer, cx, cy, x, y, color)
        else:
            # Outline only
            renderer.set_pixel(cx + x, cy + y, color)
            renderer.set_pixel(cx - x, cy + y, color)
            renderer.set_pixel(cx + x, cy - y, color)
            renderer.set_pixel(cx - x, cy - y, color)
            renderer.set_pixel(cx + y, cy + x, color)
            renderer.set_pixel(cx - y, cy + x, color)
            renderer.set_pixel(cx + y, cy - x, color)
            renderer.set_pixel(cx - y, cy - x, color)

        # Bresenham update
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6


def _draw_filled_circle_lines(renderer, cx, cy, x, y, color):
    """Helper: draw horizontal spans between circle edges for filling."""
    for xi in range(cx - x, cx + x + 1):
        renderer.set_pixel(xi, cy + y, color)
        renderer.set_pixel(xi, cy - y, color)
    for xi in range(cx - y, cx + y + 1):
        renderer.set_pixel(xi, cy + x, color)
        renderer.set_pixel(xi, cy - x, color)

    