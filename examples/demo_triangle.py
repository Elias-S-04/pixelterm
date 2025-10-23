from pixelterm import PixelRenderer, draw_triangle

r = PixelRenderer(64, 32)
try:
    draw_triangle(r, 10, 10, 30, 10, 20, 25, (0, 255, 0), filled=True)
    r.render()
finally:
    r.cleanup()
