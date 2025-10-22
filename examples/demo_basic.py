from pixelterm import PixelRenderer
from pixelterm.shapes import draw_line
import time

r = PixelRenderer(64, 32)

try:
    for i in range(50):
        r.clear()
        for y in range(r.height):
            for x in range(r.width):
                if (x + y + i) % r.width == 0:
                    r.set_pixel(x, y, (255, 50, 0))
        r.render()
        time.sleep(0.05)
finally:
    r.cleanup()
