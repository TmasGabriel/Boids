import cv2 as cv
import numpy as np

from __init__2 import *

class Screen:
    def __init__(self):
        self.background = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 3), np.uint8)
        self.background.fill(0)

    def draw_boid(self, boid):
        points_list = []
        for point in boid.verts:
            points_list.append([point[0], point[1]])
        boid_list32 = np.array(points_list, np.int32)
        cv.fillPoly(self.background, [boid_list32], WHITE)

    def plot_center(self, boid):
        cv.circle(self.background, (round(boid[0]), round(boid[1])), 3, WHITE, -1)

    def plot_corners(self, boid):
        cv.circle(self.background, [round(boid.verts[0][0]), round(boid.verts[0][1])], 3, RED, -1)
        cv.circle(self.background, [round(boid.verts[1][0]), round(boid.verts[1][1])], 3, BLUE, -1)
        cv.circle(self.background, [round(boid.verts[2][0]), round(boid.verts[2][1])], 3, BLUE, -1)

    def draw_alignment_line(self, boid, color, size):
        cv.line(self.background, (round(-size * np.cos(boid.theta) + boid.pos[0]), round(-size * np.sin(boid.theta) + boid.pos[1])),
                (round(size * np.cos(boid.theta) + boid.pos[0]), round(size * np.sin(boid.theta) + boid.pos[1])),
                color, 1)

    def draw_vision(self, boid, rad):
        cv.circle(self.background, [round(boid.center[0]), round(boid.center[1])], rad, GREEN)

    def disp_fps(self, fps, offset, text):
        cv.putText(self.background, text + str(round(fps)), [2, offset + 15], 0, .5, YELLOW)

    def draw_closest(self, boid, other):
        cv.line(self.background, (round(boid.pos[0]), round(boid.pos[1])),
                (round(other.pos[0]), round(other.pos[1])), YELLOW, 1)
