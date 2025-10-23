from pixelterm import PixelRenderer, draw_line

r = PixelRenderer(32, 16)
r.set_background((0, 0, 0))  # Black background (If no background is set, default is empty space: " ").

try:
    # Draw a few lines from center
    center_x, center_y = r.width // 2, r.height // 2
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (0, 255, 255),
        (255, 0, 255),
    ]
    points = [
        (0, 0), (r.width - 1, 0),
        (0, r.height - 1), (r.width - 1, r.height - 1),
        (r.width - 1, r.height // 2), (r.width // 2, 0)
    ]

    for (x2, y2), color in zip(points, colors):
        draw_line(r, center_x, center_y, x2, y2, color)

    r.render()
finally:
    r.cleanup()
