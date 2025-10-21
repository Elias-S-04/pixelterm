from pixelterm import PixelRenderer
import time

r = PixelRenderer(50, 50)

try:
    for i in range(50):
        r.clear()
        for y in range(r.height):
            for x in range(r.width):
                if (x + y + i) % 8 == 0:
                    r.set_pixel(x, y, (255, 50, 0))
        r.render()
        time.sleep(0.05)
finally:
    r.cleanup()
