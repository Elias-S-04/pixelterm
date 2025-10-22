from pixelterm import PixelRenderer, draw_triangle
import time

r = PixelRenderer(64, 32)
try:
    draw_triangle(r, 10, 10, 30, 10, 20, 25, (0, 255, 0), filled=True)
    r.render()
    time.sleep(5)
finally:
    r.cleanup()
