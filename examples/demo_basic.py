from pixelterm import PixelRenderer
from pixelterm.shapes import draw_line
import time

r = PixelRenderer(64, 32)
# Test multiple lines to see if the algorithm works
#draw_line(r, 0, 0, 63, 31, (255, 0, 0))      # Diagonal red
#draw_line(r, 0, 31, 63, 0, (0, 255, 0))      # Other diagonal green  
draw_line(r, 0, 15, 63, 15, (0, 0, 255))     # Horizontal blue
draw_line(r, 31, 0, 31, 31, (255, 255, 0))   # Vertical yellow

r.render()
input("Press Enter to exit...")  # Keep it visible
r.cleanup()

#try:
#    for i in range(50):
#        r.clear()
#        for y in range(r.height):
#            for x in range(r.width):
#                if (x + y + i) % r.width == 0:
#                    r.set_pixel(x, y, (255, 50, 0))
#        r.render()
#        time.sleep(0.05)
#finally:
#    r.cleanup()
