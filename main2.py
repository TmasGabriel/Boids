import time

from __init__2 import *
from display2 import *
from boids2 import *


def find_delta_time(start, end):
    compute_time = (end - start)
    compute_time_ms = compute_time * 1000
    desired_ms = (1 / DESIRED_FPS) * 1000
    # plus 1 seems to give more accurate values
    delta_time = desired_ms - compute_time_ms + 1

    return delta_time, compute_time


def eval_fps(delta_time, compute_time):
    real_fps = 1 / (delta_time / 1000)
    if compute_time != 0:
        max_fps = 1 / compute_time
    else:
        max_fps = 0

    return real_fps, max_fps


def account_for_compute_time(delta_time):
    if delta_time < 1:
        wait_time_ms = 1
    else:
        wait_time_ms = round(delta_time)

    return wait_time_ms


def quit_if_win_closed(win_name):
    try:
        cv.getWindowProperty(win_name, 0)
    except cv.error:
        if cv.error.code == -27:
            print('User Closed Window')
            quit()
        else:
            print(cv.error.msg)


def run(how_far, boids):
    real_fps, max_fps, time_tracker = 1, 0, 0
    target = [800, 400]
    for i in range(how_far):
        start = time.time()
        container = []

        screen = Screen()
        bg = screen.background

        screen.disp_fps(real_fps, 20, 'Displayed FPS: ')
        screen.disp_fps(max_fps, 2, 'Theoretical FPS: ')

        for boid in boids:
            container.append(boid.calculate(boid_list, target))

        for j, boid in enumerate(boids):

            screen.plot_center(boid.pos)
            #screen.plot_center(target)

            screen.draw_alignment_line(boid, LIGHT_BLUE, 100)

            if container[j][2]:
                screen.plot_center(container[j][2])
            #if container[j][1]:
                #screen.draw_closest(boid, container[j][1])

        for j, boid in enumerate(boids):
            boid.update(SPEED, ROTATION, container[j][0])
            boid.magic_wall(CANVAS_WIDTH, CANVAS_HEIGHT)

        cv.imshow('Boids', bg)
        end = time.time()

        delta_time, compute_time = find_delta_time(start, end)
        wait_time_ms = account_for_compute_time(delta_time)
        cv.waitKey(wait_time_ms)

        real_fps, max_fps = eval_fps(delta_time, compute_time)

        quit_if_win_closed('Boids')


boid_list = spawn_boids_randomly(NUM_BOIDS, left=0, right=CANVAS_WIDTH, top=0, bot=CANVAS_HEIGHT)
run(1000000000, boid_list)
