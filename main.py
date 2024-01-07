import numpy as np
import cv2 as cv
import random
import time

from __init__ import *


class Boid:
    def __init__(self, bow, port, starboard):
        self.bow = bow
        self.port = port
        self.star = starboard
        self.verts = [self.bow, self.port, self.star]

        self.center = ((self.bow[0] + self.port[0] + self.star[0]) / 3,
                       (self.bow[1] + self.port[1] + self.star[1]) / 3)

        self.theta = self.find_theta(self.bow)

    def update(self, boids):
        total_mass = [0, 0]
        shortest_dist = VISION_RADIUS
        closest_boid = None
        crashes = 0

        area = self.search_area(boids, VISION_RADIUS)
        too_close = self.search_area(area, FEEL_RADIUS)
        crash = self.search_area(too_close, CRASH_RADIUS)

        if area is not None:
            for boid in area:
                if boid not in too_close:
                    total_mass[0] += boid.center[0]
                    total_mass[1] += boid.center[1]

                closest_boid, shortest_dist = self.find_closest_boid(boid, closest_boid, shortest_dist)

            center_of_mass = self.find_center_of_mass(total_mass, len(area))
            pivot_to_com = self.dir_to_turn(center_of_mass)

            if closest_boid:
                if len(too_close) > 0:
                    pivot_to_sep = self.dir_to_turn(closest_boid.center) * -1
                    self.rotate(pivot_to_sep * 3)
                    if len(crash) > 0:
                        crashes += 1
                else:
                    self.rotate(pivot_to_com)
                    alignment = self.alignment(closest_boid)
                    if alignment:
                        self.rotate(alignment)

        self.move(self.theta)

        self.center = ((self.bow[0] + self.port[0] + self.star[0]) / 3,
                       (self.bow[1] + self.port[1] + self.star[1]) / 3)
        self.theta = self.find_theta(self.bow)

        return crashes

    def find_theta(self, point):  # (from center)
        return np.arctan2(point[1] - self.center[1], point[0] - self.center[0])

    def rotate(self, degrees):
        new_pos = [None, None, None]
        angle_rad = np.deg2rad(degrees)
        sin_angle = np.sin(angle_rad)
        cos_angle = np.cos(angle_rad)

        for i, vert in enumerate(self.verts):
            dist_x = vert[0] - self.center[0]
            dist_y = vert[1] - self.center[1]

            vert[0] = (dist_x * cos_angle) - (dist_y * sin_angle) + self.center[0]
            vert[1] = (dist_x * sin_angle) + (dist_y * cos_angle) + self.center[1]

        return new_pos

    def move(self, direction):
        sin_angle = np.sin(direction)
        cos_angle = np.cos(direction)
        for vert in self.verts:
            vert[0] += (MOVE_SPEED * cos_angle)
            vert[1] += (MOVE_SPEED * sin_angle)

    def search_area(self, boids, search_rad):
        in_area = []
        self_x = int(self.center[0])
        self_y = int(self.center[1])
        self_theta = self.theta
        for boid in boids:
            boid_x = int(boid.center[0])
            boid_y = int(boid.center[1])
            diff = boid.theta - self_theta

            if boid is not self:
                if boid_x in range(self_x - search_rad, self_x + search_rad):
                    if boid_y in range(self_y - search_rad, self_y + search_rad):
                        if (((boid_x - self_x) ** 2) + ((boid_y - self_y) ** 2)) ** .5 < search_rad:
                            in_area.append(boid)

        return in_area

    def dir_to_turn(self, target):
        dir = 0
        if target:
            target_theta = self.find_theta(target)
            delta = target_theta - self.theta
            delta_sin = round(np.sin(delta))

            if delta_sin < 0:
                # turn clockwise
                dir = -1
            elif delta_sin > 0:
                # turn clockwise
                dir = 1
            else:
                # dont turn
                dir = 0

        return dir

    def find_center_of_mass(self, total_mass, num_boids_in_area):
        if num_boids_in_area != 0:
            center_of_mass = (total_mass[0] / num_boids_in_area, total_mass[1] / num_boids_in_area)
        else:
            center_of_mass = self.center

        return center_of_mass

    def find_closest_boid(self, boid, closest_boid, shortest_dist):
        dist = abs(self.center[0] - boid.center[0]) + abs(self.center[1] - boid.center[1])
        if dist != 0:
            if dist < shortest_dist:
                shortest_dist = dist
                closest_boid = boid

        return closest_boid, shortest_dist

    def alignment(self, closest_boid):
        delta = closest_boid.theta - self.theta
        delta_sin = round(np.sin(delta))

        if delta_sin < 0:
            # turn clockwise
            dir = -1
        elif delta_sin > 0:
            # turn clockwise
            dir = 1
        else:
            # dont turn
            dir = 0

        return dir

    def magic_wall(self):
            # right wall
            if self.center[0] > CANVAS_WIDTH:
                for vertex in self.verts:
                    vertex[0] -= (CANVAS_WIDTH - 5)
            # left wall
            elif self.center[0] < 0:
                for vertex in self.verts:
                    vertex[0] += (CANVAS_WIDTH - 5)
            # bottom wall
            if self.center[1] > CANVAS_HEIGHT:
                for vertex in self.verts:
                    vertex[1] -= (CANVAS_HEIGHT - 5)
            # top wall
            elif self.center[1] < 0:
                for vertex in self.verts:
                    vertex[1] += (CANVAS_HEIGHT - 5)


class Screen:
    def __init__(self):
        self.background = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 3), np.uint8)
        self.background.fill(0)

    def draw_boid(self, boid):
        points_list = []
        for point in boid.verts:
            points_list.append([point[0], point[1]])
        boid_list32 = np.array(points_list, np.int32)
        cv.fillPoly(self.background, [boid_list32], BOID_COLOR)

    def plot_center(self, boid):
        cv.circle(self.background, [round(boid.center[0]), round(boid.center[1])], 3, CENTER_COLOR_DOT, -1)

    def plot_corners(self, boid):
        cv.circle(self.background, [round(boid.verts[0][0]), round(boid.verts[0][1])], 3, CENTER_OF_MASS_LINE_COLOR, -1)
        cv.circle(self.background, [round(boid.verts[1][0]), round(boid.verts[1][1])], 3, CENTER_COLOR_DOT, -1)
        cv.circle(self.background, [round(boid.verts[2][0]), round(boid.verts[2][1])], 3, CENTER_COLOR_DOT, -1)

    def draw_alignment_line(self, boid):
        cv.line(self.background, (round(boid.verts[0][0]), round(boid.verts[0][1])), (round(boid.center[0]), round(boid.center[1])), ALIGNMENT_LINE_COLOR, 1)

    def draw_vision(self, boid, rad):
        cv.circle(self.background, [round(boid.center[0]), round(boid.center[1])], rad, VISION_COLOR)

    def draw_com(self, boid, area):
        total_mass = [0, 0]
        for something in area:
            total_mass[0] += something.center[0]
            total_mass[1] += something.center[1]
        center_of_mass = boid.find_center_of_mass(total_mass, len(area))
        cv.line(self.background, (round(boid.center[0]), round(boid.center[1])),
                (round(center_of_mass[0]), round(center_of_mass[1])), CENTER_OF_MASS_LINE_COLOR, 1)

    def draw_closest(self, boid, area):
        shortest_dist = VISION_RADIUS
        closest_boid = area[0]
        for something in area:
            closest_boid, shortest_dist = boid.find_closest_boid(something, closest_boid, shortest_dist)
            cv.line(self.background, (round(boid.center[0]), round(boid.center[1])),
                    (round(closest_boid.center[0]), round(closest_boid.center[1])), ALIGNMENT_LINE_COLOR, 1)


def create_boid(size):
    x_offset = random.randrange(50, CANVAS_WIDTH - 50)
    y_offset = random.randrange(50, CANVAS_HEIGHT - 50)

    bow = [(4 * size) + x_offset, (1 * size) + y_offset]
    star = [x_offset, (2 * size) + y_offset]
    port = [x_offset, y_offset]

    boid = Boid(bow, star, port)

    rand_rotation = random.randrange(0, 360)
    boid.rotate(rand_rotation)

    return boid


def run(how_far):
    # pre-allocate list space and initialize boids
    boid_list = [create_boid(BOID_SCALE) for _ in range(NUM_BOIDS)]
    num_crashes = 0
    # game loop
    for num in range(how_far):


        start = time.time()
        # Create canvas
        screen = Screen()
        bg = screen.background

        for boid in boid_list:
            boid.magic_wall()
            num_crashes += boid.update(boid_list)

            screen.draw_boid(boid)
            screen.plot_center(boid)
            screen.draw_alignment_line(boid)
            #screen.draw_vision(boid, CRASH_RADIUS)

            area = boid.search_area(boid_list, VISION_RADIUS)
            if area is not None:
                #screen.draw_closest(boid, area)
                #screen.draw_com(boid, area)
                pass

        # display drawings
        cv.imshow('Boids', bg)

        end = time.time()
        time_taken_ms = (end - start) * 1000
        if SLEEP_TIME - 1 > time_taken_ms:
            time_frame = int(SLEEP_TIME - time_taken_ms)
            cv.waitKey(time_frame)
        else:
            cv.waitKey(1)

    return num_crashes


crashes = 0
for i in range(30):
    crashes += run(1000)

print(f' avg crash: {crashes / 30}')