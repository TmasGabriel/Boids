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

    def move(self, points, to_move_to):
        for point in points:
            point.x = point.x + to_move_to.x
            point.y = point.y + to_move_to.y

        return points

    def rotate(self, points, center, angle):
        for point in points:
            x = point.x - center.x
            y = point.y - center.y
            angle_rad = angle * numpy.pi / 180
            point.x = (x * numpy.cos(angle_rad)) - (y * numpy.sin(angle_rad)) + center.x
            point.y = (x * numpy.sin(angle_rad)) + (y * numpy.cos(angle_rad)) + center.y

        return points

    def controller(self, points, center, min, max, boids):
        cohesion = self.cohesion(max * .1, boids)
        seperation = self.seperation(max * .9, boids)

        to_move_to = Point((cohesion.x + seperation.x), (cohesion.y + seperation.y))
        #to_move_to = Point(seperation.x, seperation.y)

        allotted_rotation = random.randrange(-5, 6)
        self.rotate(points, center, allotted_rotation)
        self.move(points, to_move_to)

        return points

    def find_com(self, boids, search_radius):
        center_of_mass = Point(0, 0)
        counter = 0
        for boid in boids:
            boid.center.x = int(boid.center.x)
            boid.center.y = int(boid.center.y)
            self_center_x = int(self.center.x)
            self_center_y = int(self.center.y)

            if boid.center.x in range(self_center_x - search_radius, self_center_x + search_radius) and \
                    boid.center.y in range(self_center_y - search_radius, self_center_y + search_radius):
                center_of_mass.x += boid.center.x
                center_of_mass.y += boid.center.y
                counter += 1

        center_of_mass.x /= counter
        center_of_mass.y /= counter
        return center_of_mass

    def cohesion(self, allotment, boids):
        com = self.find_com(boids, VISION_RADIUS)
        dist_from_com = Point(self.center.x - com.x, self.center.y - com.y)
        total_dist_from_com = abs(dist_from_com.x) + abs(dist_from_com.y)
        if total_dist_from_com < 1:
            x_ratio = 0
            y_ratio = 0
        else:
            x_ratio = dist_from_com.x / total_dist_from_com
            y_ratio = dist_from_com.y / total_dist_from_com

        to_move = Point(None, None)
        if abs(dist_from_com.x) > allotment:
            to_move.x = -x_ratio * allotment
        else:
            to_move.x = dist_from_com.x

        if abs(dist_from_com.y) > allotment:
            to_move.y = -y_ratio * allotment
        else:
            to_move.y = dist_from_com.y

        return to_move

    def seperation(self, allotment, boids):
        to_move_to = Point(0, 0)
        for boid in boids:
            dist = Point(boid.center.x - self.center.x, boid.center.y - self.center.y)

            if FEELING_RADIUS > abs(dist.x) + abs(dist.y) != 0:
                if abs(dist.x) < FEELING_RADIUS:
                    norm = 1 - abs(dist.x / FEELING_RADIUS)
                    to_move_to.x += -norm * allotment * numpy.sign(dist.x)
                if abs(dist.y) < FEELING_RADIUS:
                    norm = 1 - abs(dist.y / FEELING_RADIUS)
                    to_move_to.y += -norm * allotment * numpy.sign(dist.y)

        """
        limiter
        total_move = to_move_to.x + to_move_to.y

        if total_move > allotment:
            x_ratio = to_move_to.x / total_move
            y_ratio = to_move_to.y / total_move
            to_move_to.x = x_ratio * allotment * numpy.sign(to_move_to.x)
            to_move_to.y = y_ratio * allotment * numpy.sign(to_move_to.x)
        """
        return to_move_to



def create_boid(size):
    points = []
    x_offset = random.randrange(200, 1400 - (4 * size))
    y_offset = random.randrange(100, 800 - (2 * size))
    points.append(Point((4 * size) + x_offset, (1 * size) + y_offset))
    points.append(Point(0 + x_offset, (2 * size) + y_offset))
    points.append(Point(0 + x_offset, 0 + y_offset))

    return points


# vector initialization
boids = []
for i in range(NUM_BOIDS):
    boids.append(Boid(create_boid(BOID_SCALE)))

rotation_angle = 90

# game loop
while True:
    # Create canvas
    background = numpy.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 3), numpy.uint8)
    background.fill(0)

    # changes for each individual boid
    counter = 0
    for boid in boids:
        boid_list = []
        counter += 1

        # translations
        boid.controller(boid.points, boid.center, MIN_MOVE, MAX_MOVE, boids)

        # turn boid object into format for cv2
        for pt in boid.points:
            boid_list.append([pt.x, pt.y])
        boid_list32 = numpy.array(boid_list, numpy.int32)

        # update boid with new info
        boid.update(boid.points)

        # plot boid
        #cv2.fillPoly(background, [boid_list32], BOID_COLOR)
        # plot center point
        cv2.circle(background, [round(boid.center.x), round(boid.center.y)], 5, (0, 255, 0), -1)

        # plot center line
        #cv2.line(background, (round(boid.points[0].x), round(boid.points[0].y)),
                 #(round(boid.center.x), round(boid.center.y)), (0, 0, 255), 1)
        # plot vision circle
        #cv2.circle(background, [round(boid.center.x), round(boid.center.y)], VISION_RADIUS, (0, 255, 0))
        # plot dist to com
        com = boid.find_com(boids, VISION_RADIUS)
        cv2.line(background, [round(boid.center.x), round(boid.center.y)], [round(com.x), round(com.y)], (0, 0, 255), 1)

    # display drawings
    cv2.imshow('Boids', background)
    cv2.waitKey(SLEEP_TIME)
