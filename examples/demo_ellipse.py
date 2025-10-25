from pixelterm import PixelRenderer, draw_ellipse

r = PixelRenderer(64, 32)
try:
    # Outlined ellipse
    draw_ellipse(r, 10, 5, 54, 27, (255, 255, 0), filled=False)
    # Filled ellipse
    draw_ellipse(r, 20, 10, 44, 22, (0, 120, 255), filled=True)
    r.render()
finally:
    r.cleanup()
