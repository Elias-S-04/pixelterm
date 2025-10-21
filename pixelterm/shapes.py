# pixelterm/shapes.py
import math

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

def draw_circle(renderer, cx, cy, radius, color):
    """Draw a simple circle using the Midpoint circle algorithm."""
    x = radius
    y = 0
    err = 0

    while x >= y:
        renderer.set_pixel(cx + x, cy + y, color)
        renderer.set_pixel(cx + y, cy + x, color)
        renderer.set_pixel(cx - y, cy + x, color)
        renderer.set_pixel(cx - x, cy + y, color)
        renderer.set_pixel(cx - x, cy - y, color)
        renderer.set_pixel(cx - y, cy - x, color)
        renderer.set_pixel(cx + y, cy - x, color)
        renderer.set_pixel(cx + x, cy - y, color)

        y += 1
        if err <= 0:
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1