from pixelterm.renderer import PixelRenderer
import time, math

r = PixelRenderer(64, 32)
try:
    for i in range(100):
        for y in range(r.height):
            for x in range(r.width):
                r.set_pixel(x, y, (
                    int((math.sin(x/6 + i/10)+1)*127),
                    int((math.cos(y/6 + i/10)+1)*127),
                    100
                ))
        r.render()
        time.sleep(0.03)
finally:
    r.cleanup()
