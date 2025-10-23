from pixelterm import PixelRenderer, draw_oval

r = PixelRenderer(64, 32)
try:
    # Outlined oval
    draw_oval(r, 10, 5, 54, 27, (255, 255, 0), filled=False)
    # Filled oval
    draw_oval(r, 20, 10, 44, 22, (0, 120, 255), filled=True)
    r.render()
finally:
    r.cleanup()
