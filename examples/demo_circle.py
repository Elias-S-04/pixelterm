from pixelterm import PixelRenderer, draw_circle

r = PixelRenderer(60, 30)
try:
    for rad in range(5, 15, 3):
        draw_circle(r, r.width // 2, r.height // 2, rad, (150, 200 - rad*5, 255), filled=False)
    r.render()
finally:
    r.cleanup()
