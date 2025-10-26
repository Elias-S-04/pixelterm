from pixelterm import show_text, show_multiline_text, show_banner, render_text


# Basic text
print("1. Basic text:")
show_text("HELLO WORLD!", color=(255, 0, 0), scale=1)

print("\n2. Large scaled text:")
show_text("BIG TEXT", color=(0, 255, 0), scale=2)

print("\n3. Multi-line text:")
lines = ["PIXELTERM", "IS COOL", "123456"]
show_multiline_text(lines, color=(0, 255, 255), scale=1, line_spacing=2)

print("\n4. Banner with border:")
show_banner("PIXELTERM", color=(255, 255, 0), scale=2, border=True, border_color=(255, 0, 255))

print("\n5. Custom spacing:")
show_text("SPACED OUT", color=(255, 128, 0), scale=1, spacing=3)

r = render_text("RAINBOW", color=(255, 255, 255), scale=2)

r.render()
r.cleanup()