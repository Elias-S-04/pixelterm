from pixelterm import PixelRenderer, draw_oval
import time

r = PixelRenderer(64, 32)
try:
    # Outlined oval
    draw_oval(r, 10, 5, 54, 27, (255, 255, 0), filled=False)
    # Filled oval
    draw_oval(r, 20, 10, 44, 22, (0, 120, 255), filled=True)
    r.render()
    time.sleep(5)
finally:
    r.cleanup()
