import time, random

def sleep_frame(fps=30):
    time.sleep(1 / fps)

def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
