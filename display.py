import numpy as np
import cv2 as cv

from __init__ import *
from screen_splitting import *


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

    def draw_quad(self, top, bot, left, right, middle):
        cv.line(self.background, (middle[0], top), middle, ALIGNMENT_LINE_COLOR, 1)
        cv.line(self.background, (middle[0], bot), middle, ALIGNMENT_LINE_COLOR, 1)
        cv.line(self.background, (left, middle[1]), middle, ALIGNMENT_LINE_COLOR, 1)
        cv.line(self.background, (right, middle[1]), middle, ALIGNMENT_LINE_COLOR, 1)

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
