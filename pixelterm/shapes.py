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

    
def draw_rectangle(renderer, x1, y1, x2, y2, color, filled=False):
    """Draw a rectangle from (x1, y1) to (x2, y2)."""
    if filled:
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                renderer.set_pixel(x, y, color)
    else:
        for x in range(x1, x2 + 1):
            renderer.set_pixel(x, y1, color)
            renderer.set_pixel(x, y2, color)
        for y in range(y1, y2 + 1):
            renderer.set_pixel(x1, y, color)
            renderer.set_pixel(x2, y, color)

def draw_triangle(renderer, x1, y1, x2, y2, x3, y3, color, filled=False):
    """Draw a triangle given by three points."""
    if filled:
        # Simple filled triangle using horizontal lines (not optimized)
        points = sorted([(x1, y1), (x2, y2), (x3, y3)], key=lambda p: p[1])
        (x1, y1), (x2, y2), (x3, y3) = points

        def edge_interpolate(y, x0, y0, x1, y1):
            if y1 == y0:
                return x0
            return x0 + (x1 - x0) * (y - y0) // (y1 - y0)

        for y in range(y1, y3 + 1):
            if y < y2:
                xa = edge_interpolate(y, x1, y1, x2, y2)
                xb = edge_interpolate(y, x1, y1, x3, y3)
            else:
                xa = edge_interpolate(y, x2, y2, x3, y3)
                xb = edge_interpolate(y, x1, y1, x3, y3)
            if xa > xb:
                xa, xb = xb, xa
            for x in range(xa, xb + 1):
                renderer.set_pixel(x, y, color)
    else:
        draw_line(renderer, x1, y1, x2, y2, color)
        draw_line(renderer, x2, y2, x3, y3, color)
        draw_line(renderer, x3, y3, x1, y1, color)


def draw_oval(renderer, x1, y1, x2, y2, color, filled=False):
    """
    Draw an oval (ellipse) using the Midpoint Ellipse Algorithm.

    Parameters:
        renderer: PixelRenderer instance
        x1, y1 : top-left corner of bounding box
        x2, y2 : bottom-right corner of bounding box
        color  : (r, g, b)
        filled : bool, fill the oval if True
    """
    # Calculate radii and center
    rx = abs(x2 - x1) // 2
    ry = abs(y2 - y1) // 2
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    # Region 1
    x = 0
    y = ry
    rx2 = rx * rx
    ry2 = ry * ry
    tworx2 = 2 * rx2
    twory2 = 2 * ry2
    px = 0
    py = tworx2 * y

    # Decision parameter for region 1
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    while px < py:
        if filled:
            _draw_horizontal_line(renderer, cx - x, cx + x, cy + y, color)
            _draw_horizontal_line(renderer, cx - x, cx + x, cy - y, color)
        else:
            renderer.set_pixel(cx + x, cy + y, color)
            renderer.set_pixel(cx - x, cy + y, color)
            renderer.set_pixel(cx + x, cy - y, color)
            renderer.set_pixel(cx - x, cy - y, color)

        x += 1
        px += twory2
        if p1 < 0:
            p1 += ry2 + px
        else:
            y -= 1
            py -= tworx2
            p1 += ry2 + px - py

    # Region 2
    p2 = (ry2) * ((x + 0.5) ** 2) + (rx2) * ((y - 1) ** 2) - (rx2 * ry2)
    while y >= 0:
        if filled:
            _draw_horizontal_line(renderer, cx - x, cx + x, cy + y, color)
            _draw_horizontal_line(renderer, cx - x, cx + x, cy - y, color)
        else:
            renderer.set_pixel(cx + x, cy + y, color)
            renderer.set_pixel(cx - x, cy + y, color)
            renderer.set_pixel(cx + x, cy - y, color)
            renderer.set_pixel(cx - x, cy - y, color)

        y -= 1
        py -= tworx2
        if p2 > 0:
            p2 += rx2 - py
        else:
            x += 1
            px += twory2
            p2 += rx2 - py + px


def _draw_horizontal_line(renderer, x_start, x_end, y, color):
    """Helper to draw a horizontal line (used for filling shapes)."""
    for x in range(x_start, x_end + 1):
        renderer.set_pixel(x, y, color)
