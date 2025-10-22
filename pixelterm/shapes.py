"""Shape drawing functions for PixelRenderer."""

def draw_line(renderer, x1, y1, x2, y2, color):
    # Draw a simple line using Bresenham's algorithm.
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
    # Draw a circle using Bresenham's circle algorithm.
    # If filled=True, fills the circle by drawing horizontal lines between edges.
    x = 0
    y = radius
    d = 3 - 2 * radius

    while y >= x:
        if filled:
            # Fill between symmetric points
            for xi in range(cx - x, cx + x + 1):
                renderer.set_pixel(xi, cy + y, color)
                renderer.set_pixel(xi, cy - y, color)
            for xi in range(cx - y, cx + y + 1):
                renderer.set_pixel(xi, cy + x, color)
                renderer.set_pixel(xi, cy - x, color)
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

        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6

    
def draw_rectangle(renderer, x1, y1, x2, y2, color, filled=False):
    # Draw a rectangle from (x1, y1) to (x2, y2).
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
    # Draw a triangle given by three points.
    if filled:
        # Simple filled triangle using horizontal lines
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
    # Draw an oval (ellipse) using the Midpoint Ellipse Algorithm.

    # Calculate radii and center
    rx = abs(x2 - x1) // 2
    ry = abs(y2 - y1) // 2
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    if rx == 0 or ry == 0:
        return

    x = 0
    y = ry
    rx2 = rx * rx
    ry2 = ry * ry
    tworx2 = 2 * rx2
    twory2 = 2 * ry2
    px = 0
    py = tworx2 * y

    # Region 1
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
    # Helper to draw a horizontal line (used for filling shapes).
    for x in range(x_start, x_end + 1):
        renderer.set_pixel(x, y, color)


def draw_polygon(renderer, points, color, filled=False):
    # Draw a polygon given a list of points.

    if len(points) < 3:
        return
    
    if filled:
        # Scanline fill algorithm
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        
        for y in range(min_y, max_y + 1):
            intersections = []
            
            # Find intersections with polygon edges
            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]
                
                if p1[1] != p2[1]:  # Not horizontal
                    if min(p1[1], p2[1]) <= y <= max(p1[1], p2[1]):
                        x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) // (p2[1] - p1[1])
                        intersections.append(x)
            
            # Sort and fill between pairs
            intersections.sort()
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    for x in range(intersections[i], intersections[i + 1] + 1):
                        renderer.set_pixel(x, y, color)
    else:
        # Draw outline
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            draw_line(renderer, p1[0], p1[1], p2[0], p2[1], color)


def draw_bezier_curve(renderer, p0, p1, p2, p3, color, steps=100):
    # Draw a cubic Bezier curve.
    
    for i in range(steps + 1):
        t = i / steps
        
        # Cubic Bezier formula
        x = int((1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0])
        y = int((1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1])
        
        renderer.set_pixel(x, y, color)