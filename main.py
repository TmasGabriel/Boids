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

    def controller(self, points, center):
        allotted_movement = random.randrange(1, 10)
        foo = random.randrange(0, 4)
        x_movement = random.randrange(0, allotted_movement)
        y_movement = allotted_movement - x_movement
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



# vector initialization
bow = Point(600, 300)
starboard = Point(200, 400)
port = Point(200, 200)

test_boid = Boid([bow, starboard, port])
center = Point((test_boid.points[0].x + test_boid.points[1].x + test_boid.points[2].x) / 3,
               (test_boid.points[0].y + test_boid.points[1].y + test_boid.points[2].y) / 3)

rotation_angle = 90
allotted_movement = 10


for i in range(7210):
    a = []
    # Background
    background = numpy.zeros((600, 600, 3), numpy.uint8)
    background.fill(0)

    # translations
    #test_boid.rotate(test_boid.points, center, rotation_angle)
    #test_boid.move(test_boid.points, 10, 10)
    test_boid.controller(test_boid.points, center)

    # recalculate center point
    center = Point((test_boid.points[0].x + test_boid.points[1].x + test_boid.points[2].x) / 3,
                   (test_boid.points[0].y + test_boid.points[1].y + test_boid.points[2].y) / 3)
    indent = [(test_boid.points[1].x + test_boid.points[2].x) / 2, (test_boid.points[1].y + test_boid.points[2].y) / 2]
    #slope = (indent[1] - bow.y) / (indent[0] - bow.x)
    #yint = indent[1] + (slope * indent[0])
    #print("slope " + str(round(slope)))
    #print(numpy.cos(slope))


    # turn boid object into usable tuple
    for pt in test_boid.points:
        a.append([pt.x, pt.y])
    pts = numpy.array(a, numpy.int32)

    # plot boid
    cv2.fillPoly(background, [pts], BOID_COLOR)
    # plot center point                                            b   g   r
    cv2.circle(background, [round(center.x), round(center.y)], 3, (0, 255, 0), -1)
    # center line
    cv2.line(background, (round(bow.x), round(bow.y)), (round(indent[0]), round(indent[1])), (0, 0, 255), 1)

    # display boid
    cv2.imshow('Boids', background)
    # sleep function in milliseconds
    cv2.waitKey(17)

