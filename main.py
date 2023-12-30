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

    def controller(self, points, center, allotted_movement, min_movement, boids):
        min = min_movement
        max = allotted_movement
        center_of_local_mass = self.find_center(boids)
        dist_from_center_of_mass = (center_of_local_mass[0] + center_of_local_mass[1]) / 2
        if dist_from_center_of_mass != 0:
            x_ratio = center_of_local_mass[0] / dist_from_center_of_mass
            y_ratio = center_of_local_mass[1] / dist_from_center_of_mass
        else:
            x_ratio = 0
            y_ratio = 0
        relative_pos_x = self.center.x - center_of_local_mass[0]
        relative_pos_y = self.center.y - center_of_local_mass[1]

        if abs(relative_pos_x) > max:
            if relative_pos_x > 0:
                x_movement = x_ratio * -max
            else:
                x_movement = x_ratio * max

        elif abs(relative_pos_x) < min:
            x_movement = random.randrange(-min, min + 1)
        else:
            x_movement = relative_pos_x

        if abs(relative_pos_y) > max:
            if relative_pos_y > 0:
                y_movement = y_ratio * -max
            else:
                y_movement = y_ratio * max
        elif abs(relative_pos_y) < min:
            y_movement = random.randrange(-min, min + 1)
        else:
            y_movement = relative_pos_y



        allotted_rotation = random.randrange(-5, 6)
        self.rotate(points, center, allotted_rotation)
        self.move(points, x_movement, y_movement)

        return points

    def find_center(self, boids):
        search_radius = 150
        center_of_mass_x = 0
        center_of_mass_y = 0
        counter = 0
        for boid in boids:
            boid.center.x = int(boid.center.x)
            boid.center.y = int(boid.center.y)
            foox = int(self.center.x)
            fooy = int(self.center.y)
            if boid.center.x in range(foox - search_radius, foox + search_radius) and \
                    boid.center.y in range(fooy - search_radius, fooy + search_radius):
                center_of_mass_x += boid.center.x
                center_of_mass_y += boid.center.y
                counter += 1

        center_of_mass_x /= counter
        center_of_mass_y /= counter
        return [center_of_mass_x, center_of_mass_y]




def create_boid(size):
    points = []
    x_offset = random.randrange(200, 1400 - (4 * size))
    y_offset = random.randrange(200, 700 - (2 * size))
    points.append(Point((4 * size) + x_offset, (1 * size) + y_offset))
    points.append(Point(0 + x_offset, (2 * size) + y_offset))
    points.append(Point(0 + x_offset, 0 + y_offset))

    return points



# vector initialization
boids = []
for i in range(50):
    boids.append(Boid(create_boid(10)))

rotation_angle = 90
allotted_movement = 5
min_movement = 3

# game loop
while True:
    # Create canvas
    background = numpy.zeros((CANVAS_WIDTH, CANVAS_HEIGHT, 3), numpy.uint8)
    background.fill(0)

    # changes for each individual boid
    for test_boid in boids:
        a = []

        # translations
        test_boid.controller(test_boid.points, test_boid.center, allotted_movement, min_movement, boids)

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
        #cv2.line(background, (round(test_boid.points[0].x), round(test_boid.points[0].y)),
                 #(round(test_boid.indent.x), round(test_boid.indent.y)), (0, 0, 255), 1)

        cv2.circle(background, [round(test_boid.center.x), round(test_boid.center.y)], 150, (0, 255, 0))
        apple = test_boid.find_center(boids)
        #cv2.circle(background, [round(apple[0]), round(apple[1])], 5, (0, 0, 255), -1)
        cv2.line(background, [round(test_boid.center.x), round(test_boid.center.y)], [round(apple[0]), round(apple[1])],
                 (0, 0, 255), 1)


    # display boid
    cv2.imshow('Boids', background)
    # sleep function in milliseconds
    cv2.waitKey(17)
