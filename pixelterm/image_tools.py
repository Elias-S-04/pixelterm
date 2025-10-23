"""
pixelterm.image_tools
---------------------
Load and display images, GIFs, and videos in the terminal using pixelterm.
"""

import os
import time
from PIL import Image, ImageSequence
from .renderer import PixelRenderer


def _resize_image(image, target_width, target_height):
    # Resize image to fit target dimensions while maintaining aspect ratio.
    img_width, img_height = image.size
    
    # Calculate aspect ratios
    img_ratio = img_width / img_height
    target_ratio = target_width / target_height
    
    # Determine new dimensions based on aspect ratio
    if img_ratio > target_ratio:
        # Image is wider than target ratio
        new_width = target_width
        new_height = int(target_width / img_ratio)
    else:
        # Image is taller than target ratio
        new_height = target_height
        new_width = int(target_height * img_ratio)
    
    # Center the image in the target dimensions
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2
    
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized, x_offset, y_offset


def _image_to_pixels(image, renderer, x_offset=0, y_offset=0):
    # Convert PIL Image to pixel data for renderer.
    renderer.clear()
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    width, height = image.size
    
    for y in range(height):
        for x in range(width):
            if (x_offset + x < renderer.width and 
                y_offset + y < renderer.height):
                r, g, b = image.getpixel((x, y))
                renderer.set_pixel(x_offset + x, y_offset + y, (r, g, b))


def show_image(image_path, width=64, height=32, cell="██"):
    """
    Display a static image in the terminal.
    
    Args:
        image_path (str): Path to the image file
        width (int): Terminal width in characters (default: 64)
        height (int): Terminal height in characters (default: 32)
        cell (str): Character(s) to use for each pixel (default: "██")
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return
    
    try:
        # Load and resize image
        image = Image.open(image_path)
        resized_image, x_offset, y_offset = _resize_image(image, width, height)
        
        # Create renderer and display
        r = PixelRenderer(width, height, cell)
        _image_to_pixels(resized_image, r, x_offset, y_offset)
        
        r.render()
        r.cleanup()
        
        print(f"Image: {os.path.basename(image_path)} ({image.size[0]}x{image.size[1]})")
        
    except Exception as e:
        print(f"Error loading image: {e}")


def show_gif(gif_path, width=64, height=32, cell="██", frame_delay=None, loop=True):
    """
    Display an animated GIF in the terminal.
    
    Args:
        gif_path (str): Path to the GIF file
        width (int): Terminal width in characters (default: 64)
        height (int): Terminal height in characters (default: 32)
        cell (str): Character(s) to use for each pixel (default: "██")
        frame_delay (float): Override frame delay in seconds (default: use GIF timing)
        loop (bool): Whether to loop the animation (default: True)
    """
    if not os.path.exists(gif_path):
        print(f"Error: GIF file '{gif_path}' not found.")
        return
    
    try:
        # Load GIF
        gif = Image.open(gif_path)
        
        if not gif.is_animated:
            print("Warning: File is not an animated GIF. Use show_image() instead.")
            show_image(gif_path, width, height, cell)
            return
        
        # Extract frames and timing
        frames = []
        durations = []
        
        for frame in ImageSequence.Iterator(gif):
            frame_copy = frame.copy()
            resized_frame, x_offset, y_offset = _resize_image(frame_copy, width, height)
            frames.append((resized_frame, x_offset, y_offset))
            
            # Get frame duration (in milliseconds, convert to seconds)
            duration = frame.info.get('duration', 100) / 1000.0
            if frame_delay is not None:
                duration = frame_delay
            durations.append(duration)
        
        print(f"Playing GIF: {os.path.basename(gif_path)} ({len(frames)} frames)")
        print("Press Ctrl+C to stop...")
        
        # Create renderer with alt screen for smooth animation
        r = PixelRenderer(width, height, cell, use_alt_screen=True)
        
        try:
            frame_idx = 0
            while True:
                frame, x_offset, y_offset = frames[frame_idx]
                _image_to_pixels(frame, r, x_offset, y_offset)
                r.render()
                
                time.sleep(durations[frame_idx])
                frame_idx = (frame_idx + 1) % len(frames)
                
                # Break if not looping and we've completed one cycle
                if not loop and frame_idx == 0:
                    break
                    
        except KeyboardInterrupt:
            print("\nAnimation stopped.")
        finally:
            r.cleanup(preserve_final_frame=True)
            
    except Exception as e:
        print(f"Error loading GIF: {e}")


def show_video(video_path, width=64, height=32, cell="██", fps=None, start_time=0, duration=None):
    """
    Display a video in the terminal.
    
    Args:
        video_path (str): Path to the video file
        width (int): Terminal width in characters (default: 64)
        height (int): Terminal height in characters (default: 32)
        cell (str): Character(s) to use for each pixel (default: "██")
        fps (float): Override video FPS (default: use video's FPS)
        start_time (float): Start time in seconds (default: 0)
        duration (float): Duration to play in seconds (default: full video)
    """
    try:
        import cv2
    except ImportError:
        print("Error: opencv-python is required for video support.")
        print("Install with: pip install opencv-python")
        return
    
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    
    try:
        # Open video
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Error: Could not open video file '{video_path}'")
            return
        
        # Get video properties
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / video_fps if video_fps > 0 else 0
        
        # Set playback parameters
        if fps is None:
            fps = min(video_fps, 30)  # Cap at 30 FPS for terminal display
        
        frame_delay = 1.0 / fps if fps > 0 else 1.0 / 30
        
        # Seek to start time
        if start_time > 0:
            start_frame = int(start_time * video_fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # Calculate end frame
        if duration is not None:
            end_frame = int((start_time + duration) * video_fps)
        else:
            end_frame = total_frames
        
        print(f"Playing video: {os.path.basename(video_path)}")
        print(f"Duration: {video_duration:.1f}s, FPS: {video_fps:.1f} -> {fps:.1f}")
        print("Press Ctrl+C to stop...")
        
        # Create renderer with alt screen for smooth animation
        r = PixelRenderer(width, height, cell, use_alt_screen=True)
        
        try:
            frame_count = 0
            while True:
                ret, frame = cap.read()
                
                if not ret or cap.get(cv2.CAP_PROP_POS_FRAMES) >= end_frame:
                    break
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL Image
                pil_image = Image.fromarray(frame_rgb)
                resized_frame, x_offset, y_offset = _resize_image(pil_image, width, height)
                
                # Render frame
                _image_to_pixels(resized_frame, r, x_offset, y_offset)
                r.render()
                
                time.sleep(frame_delay)
                frame_count += 1
                
        except KeyboardInterrupt:
            print(f"\nVideo stopped after {frame_count} frames.")
        finally:
            r.cleanup(preserve_final_frame=True)
            cap.release()
            
    except Exception as e:
        print(f"Error loading video: {e}")

