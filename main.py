import cv2 as cv
import time

from __init__ import *
from display import Screen
from boid import *


def run(how_far):
    # pre-allocate list space and initialize boids
    boid_list = [create_boid(BOID_SCALE) for _ in range(NUM_BOIDS)]
    value = 0
    # game loop
    for num in range(how_far):
        start = time.time()
        # Create canvas
        screen = Screen()
        bg = screen.background

        for boid in boid_list:
            boid.magic_wall()
            value += boid.update(boid_list)

            screen.draw_boid(boid)

        # display drawings
        cv.imshow('Boids', bg)

        #processing inbetween frames
        end = time.time()
        time_taken_ms = (end - start) * 1000
        if SLEEP_TIME - 1 > time_taken_ms:
            time_frame = int(SLEEP_TIME - time_taken_ms)
            cv.waitKey(time_frame)
        else:
            cv.waitKey(1)

    return value

value = 0
for i in range(30):
    value += run(1000)
print(value/30)