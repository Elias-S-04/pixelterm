from pixelterm import PixelRenderer, draw_rectangle
import time

r = PixelRenderer(64, 32)
try:
    draw_rectangle(r, 10, 5, 50, 25, (255, 0, 0), filled=True)
    r.render()
    time.sleep(5)
finally:
    r.cleanup()
