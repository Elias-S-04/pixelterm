from pixelterm import PixelRenderer, draw_polygon

r = PixelRenderer(32, 16)
try:
    # Draw a polygon using a list of (x, y) coordinate tuples
    # pentagon
    pentagon_points = [(10, 5), (20, 5), (15, 12), (10, 12), (10, 5)]
    draw_polygon(r, pentagon_points, (255, 0, 255), filled=True)

    r.render()
finally:
    r.cleanup()
