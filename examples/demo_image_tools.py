from pixelterm import show_image, show_gif, show_video

# Display a static image
#show_image("path/to/image.jpg", width=64, height=32)

# Display an animated GIF
show_gif("/home/elias/Projects/pixelterm/examples/nyan-cat.gif", width=64, height=32, loop=True)

# Display a video (requires opencv-python)
#show_video("path/to/video.mp4", width=64, height=32, fps=15, duration=10)

