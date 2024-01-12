import cv2 as cv
import time

from __init__ import *
from display import Screen
from boid import *
from screen_splitting import *


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

        top, bot, left, right = 0, CANVAS_HEIGHT, 0, CANVAS_WIDTH
        middle = find_mid(top, bot, left, right)
        screen.draw_quad(top, bot, left, right, middle)
        quad_list = []

        for boid in boid_list:
            boid.magic_wall()
            value += boid.update(boid_list)
            screen.draw_vision(boid, VISION_RADIUS)

            quad, t, b, l, r = detect_quad(boid, top, bot, left, right, middle)
            mid = find_mid(t, b, l, r)
            screen.draw_quad(t, b, l, r, mid)
            quad, t, b, l, r = detect_quad(boid, t, b, l, r, mid)
            mid = find_mid(t, b, l, r)
            screen.draw_quad(t, b, l, r, mid)
            quad, t, b, l, r = detect_quad(boid, t, b, l, r, mid)
            mid = find_mid(t, b, l, r)
            screen.draw_quad(t, b, l, r, mid)

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
    value += run(10000000)
print(value/30)