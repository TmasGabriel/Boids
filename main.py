import cv2 as cv
import time

from __init__ import *
from display import Screen
from boid import *
from grid import *


def run(how_far):
    # pre-allocate list space and initialize boids
    boid_list = [create_boid(BOID_SCALE) for _ in range(NUM_BOIDS)]
    value = 0
    grid = Grid(VISION_RADIUS, VISION_RADIUS, CANVAS_WIDTH, CANVAS_HEIGHT)
    grid_vals = grid.create_grid()

    # game loop
    for num in range(how_far):
        start = time.time()
        # Create canvas
        screen = Screen()
        bg = screen.background
        for row, col in enumerate(grid_vals):
            cv.line(bg, (0, col[0][1]), (CANVAS_HEIGHT, col[0][1]),ALIGNMENT_LINE_COLOR, 1)
            cv.line(bg, (col[row][0], 0), (col[row][0], CANVAS_WIDTH), ALIGNMENT_LINE_COLOR, 1)

        for boid in boid_list:
            boid.magic_wall()
            #value += boid.update(boid_list)

            screen.draw_boid(boid)
            screen.draw_vision(boid, VISION_RADIUS)

            grid.in_cell(boid)
            for row in grid.cell_cords:
                print(row)


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
