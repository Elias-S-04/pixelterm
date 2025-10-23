"""
PixelTerm - Terminal-based pixel graphics library
===============================================

A Python library for creating pixel-based graphics and visualizations in the terminal.

Examples:
    Basic shapes:
        >>> from pixelterm import PixelRenderer, draw_line, draw_circle
        >>> r = PixelRenderer(32, 16)
        >>> draw_line(r, 0, 0, 31, 15, (255, 0, 0))
        >>> r.render()
        >>> r.cleanup()

    GitHub heatmap:
        >>> from pixelterm import show_github_heatmap
        >>> show_github_heatmap("username")
"""

# Core renderer
from .renderer import PixelRenderer

# Shape drawing functions
from .shapes import draw_line, draw_circle, draw_rectangle, draw_triangle, draw_oval, draw_polygon, draw_bezier_curve

# GitHub integration
from .githubmap import show_github_heatmap

# Image tools
from .image_tools import show_image, show_gif, show_video, convert_image_to_ascii

# Version
__version__ = "0.1.0"
__author__ = "Elias-S-04"

# Public API
__all__ = [
    "PixelRenderer",
    "draw_line", 
    "draw_circle", 
    "draw_rectangle", 
    "draw_triangle",
    "draw_oval",
    "draw_polygon",
    "draw_bezier_curve",
    "show_github_heatmap",
    "show_image",
    "show_gif",
    "show_video",
    "convert_image_to_ascii"
]
