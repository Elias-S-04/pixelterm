from pixelterm import show_image, show_gif, show_video, convert_image_to_ascii

# Display a static image
#show_image("path/to/image.jpg", width=64, height=32)

# Display an animated GIF
show_gif("/home/elias/Projects/pixelterm/examples/nyan-cat.gif", width=64, height=32, loop=True)

# Display a video (requires opencv-python)
#show_video("path/to/video.mp4", width=64, height=32, fps=15, duration=10)

# Convert to ASCII art
#ascii_art = convert_image_to_ascii("path/to/image.jpg", width=80, height=40)
#print(ascii_art)  