import numpy
import cv2
import random
import time

from __init__ import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Boid:
    def __init__(self, points):
        self.points = points

        x_total = 0
        y_total = 0
        for point in points:
            x_total += point.x
            y_total += point.y
        self.center = Point(x_total / 3, y_total / 3)

        self.indent = Point((points[1].x + points[2].x) / 2, (points[1].y + points[2].y) / 2)

        self.slope = (self.indent.y - points[0].y) / (self.indent.x - points[0].x)
        self.y_int = self.indent.y + (self.slope * self.indent.x)

    def update(self, points):
        x_total = 0
        y_total = 0
        for point in points:
            x_total += point.x
            y_total += point.y
        self.center = Point(x_total / 3, y_total / 3)

        self.indent = Point((points[1].x + points[2].x) / 2, (points[1].y + points[2].y) / 2)

        try:
            self.slope = (self.indent.y - points[0].y) / (self.indent.x - points[0].x)
        except ZeroDivisionError:
            self.slope = numpy.inf
            print('zero slope')
        self.y_int = self.indent.y + (self.slope * self.indent.x)

    def move(self, points, x, y):
        for point in points:
            point.x = point.x + x
            point.y = point.y + y

        return points

    def rotate(self, points, center, angle):
        for point in points:
            x = point.x - center.x
            y = point.y - center.y
            angle_rad = angle * numpy.pi / 180
            point.x = (x * numpy.cos(angle_rad)) - (y * numpy.sin(angle_rad)) + center.x
            point.y = (x * numpy.sin(angle_rad)) + (y * numpy.cos(angle_rad)) + center.y

        return points

    def controller(self, points, center, allotted_movement):
        rand_movement = random.randrange(1, allotted_movement)
        foo = random.randrange(0, 4)
        x_movement = random.randrange(0, rand_movement)
        y_movement = rand_movement - x_movement
        if foo == 0:
            y_movement = -y_movement
            x_movement = -x_movement
        elif foo == 1:
            y_movement = -y_movement
        elif foo == 2:
            x_movement = -x_movement

        allotted_rotation = random.randrange(-5, 6)
        self.rotate(points, center, allotted_rotation)
        self.move(points, x_movement, y_movement)

        return points


def create_boid(size):
    points = []
    x_offset = random.randrange(0, CANVAS_WIDTH - (4 * size))
    y_offset = random.randrange(0, CANVAS_HEIGHT - (2 * size))
    points.append(Point((4 * size) + x_offset, (1 * size) + y_offset))
    points.append(Point(0 + x_offset, (2 * size) + y_offset))
    points.append(Point(0 + x_offset, 0 + y_offset))

    return points


# vector initialization
boids = []
for i in range(100):
    boids.append(Boid(create_boid(5)))

rotation_angle = 90
allotted_movement = 10

# game loop
while True:
    # Create canvas
    background = numpy.zeros((CANVAS_WIDTH, CANVAS_HEIGHT, 3), numpy.uint8)
    background.fill(0)

    # changes for each individual boid
    for test_boid in boids:
        a = []

        # translations
        test_boid.controller(test_boid.points, test_boid.center, allotted_movement)

        # turn boid object into usable tuple
        for pt in test_boid.points:
            a.append([pt.x, pt.y])
        pts = numpy.array(a, numpy.int32)

        # update boid with new info
        test_boid.update(test_boid.points)

        # plot boid
        cv2.fillPoly(background, [pts], BOID_COLOR)
        # plot center point                                                                 b   g   r
        cv2.circle(background, [round(test_boid.center.x), round(test_boid.center.y)], 3, (0, 255, 0), -1)
        # center line
        cv2.line(background, (round(test_boid.points[0].x), round(test_boid.points[0].y)),
                 (round(test_boid.indent.x), round(test_boid.indent.y)), (0, 0, 255), 1)

    # display boid
    cv2.imshow('Boids', background)
    # sleep function in milliseconds
    cv2.waitKey(17)
