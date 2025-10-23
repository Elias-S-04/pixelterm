from pixelterm import PixelRenderer, draw_rectangle

r = PixelRenderer(32, 16)
try:
    draw_rectangle(r, 10, 5, 22, 11, (255, 0, 0), filled=True)
    r.render()
finally:
    r.cleanup()
