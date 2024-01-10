CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 900
#              b    g    r
BOID_COLOR = (255, 255, 255)
CENTER_COLOR_DOT = (000, 255, 000)
ALIGNMENT_LINE_COLOR = (238, 244, 21)
VISION_COLOR = (0, 255, 0)
CENTER_OF_MASS_LINE_COLOR = (0, 0, 255)


MIN_SPEED = 3  # min amount of pixels a boid will move per frame
MAX_SPEED = 6  # max amount of pixels a boid will move per frame
ROTATION = 3

NUM_BOIDS = 60
BOID_SCALE = 3  # how many times larger should boids be than base size (4 by 2 pixels)

VISION_RADIUS = 150  # how far boids can see
FEEL_RADIUS = 40  # how close is too close
CRASH_RADIUS = 10

SLEEP_TIME = 1  # how long to wait inbetween frames in milliseconds
