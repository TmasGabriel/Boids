import numpy
import cv2
import random
import math
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
        for point in self.points:
            x_total += point.x
            y_total += point.y

        self.center = Point(x_total / 3, y_total / 3)
        self.theta = self.find_alignment(self.points[0])
        #self.indent = Point((points[1].x + points[2].x) / 2, (points[1].y + points[2].y) / 2)

    def update(self):
        x_total = 0
        y_total = 0
        for point in self.points:
            x_total += point.x
            y_total += point.y

        #find the center based on current updated points
        self.center = Point(x_total / 3, y_total / 3)
        #update alignment
        self.theta = self.find_alignment(self.points[0])
        #self.indent = Point((points[1].x + points[2].x) / 2, (points[1].y + points[2].y) / 2)

    def move(self, direc):
        for point in self.points:
            point.x += MOVE_SPEED * numpy.cos(direc)
            point.y += MOVE_SPEED * numpy.sin(direc)

    def rotate_point(self, pointx, pointy, originx, originy, degrees):
        radians = numpy.deg2rad(degrees)
        x = pointx
        y = pointy
        qx = x * math.cos(radians) - y * math.sin(radians)
        qy = x * math.sin(radians) + y * math.cos(radians)
        return qx, qy

    #Takes number of degrees to rotate - to change rotation direction
    def rotate(self, angle):
        for point in self.points:
            x = 0
            y = 0
            x = point.x - self.center.x
            y = point.y - self.center.y
            #WASangle_rad = angle * numpy.pi / 180
            angle_rad = numpy.deg2rad(angle)
            point.x = (x * numpy.cos(angle_rad)) - (y * numpy.sin(angle_rad)) + self.center.x
            point.y = (x * numpy.sin(angle_rad)) + (y * numpy.cos(angle_rad)) + self.center.y

    def search_area(self, boids, search_radius):
        start_time = time.time()
        boids_in_your_area = []
        for boid in boids:
            boid.center.x = int(boid.center.x)
            boid.center.y = int(boid.center.y)
            self_center_x = int(self.center.x)
            self_center_y = int(self.center.y)

            if boid.center.x in range(self_center_x - search_radius, self_center_x + search_radius) and \
                    boid.center.y in range(self_center_y - search_radius, self_center_y + search_radius):
                boids_in_your_area.append(boid)

        
        return boids_in_your_area

    """
    slower
    def search_area(self, boids, search_radius):
        neighbors = []
        for boid in boids:
            if boid != self.center and numpy.sqrt((boid.center.x - self.center.x) ** 2 + (boid.center.y - self.center.y) ** 2) < search_radius:
                neighbors.append(boid)
        return neighbors
        
        """

########################################################################################################################

    def controller(self):
        com = self.find_com(all_boids, VISION_RADIUS)
        closest_boid = self.find_closest_boid(all_boids, VISION_RADIUS)
        alignment = self.alignment(all_boids, VISION_RADIUS)

        pivot_com = self.turn_to_face(com)
        pivot_sep = self.turn_to_face(closest_boid) * -1
        #self.rotate(1 * 1 * alignment)

        self.rotate( alignment )
        #self.rotate(pivot_com)
        self.rotate(pivot_sep)

        #I think we need to recalculate theta after rotation  TEST TEST TEST
        #self.theta = self.find_alignment(self.points[0])

        # 1 * 1 * alignment

        self.move(self.theta)


########################################################################################################################

    def is_facing(self):
        is_facing = False
        multiplier = 100
        fov = 120
        fov_rad = (fov * numpy.pi / 180) / 2
        #target_theta = int(self.find_alignment(target) * multiplier)

        upper_bound = int((self.theta + fov_rad) * multiplier)
        lower_bound = int((self.theta - fov_rad) * multiplier)

        #if target_theta in range(lower_bound, upper_bound):
            #is_facing = True

        return [upper_bound, lower_bound]

    def turn_to_face(self, target):
        pivot = 0
        if target != None:
            target_theta = self.find_alignment(target)
            delta = target_theta - self.theta

            # normalizing data
            if delta > numpy.pi:
                delta -= 2 * numpy.pi
            elif delta < -numpy.pi:
                delta += 2 * numpy.pi

            if delta > 0:
                pivot = 1
            elif delta < 0:
                pivot = -1

        return pivot

    def find_com(self, boids, search_radius):
        total_mass = [0, 0]
        area = self.search_area(boids, search_radius)
        for boid in area:
            total_mass[0] += boid.center.x
            total_mass[1] += boid.center.y

        center_of_mass = Point(total_mass[0], total_mass[1])
        center_of_mass.x /= len(area)
        center_of_mass.y /= len(area)

        return center_of_mass

    def find_closest_boid(self, boids, search_radius):
        shortest_dist = search_radius
        closest_boid = None
        area = self.search_area(boids, search_radius)
        for boid in area:
            dist = abs(self.center.x - boid.center.x) + abs(self.center.y - boid.center.y)
            if dist != 0:
                if dist < shortest_dist:
                    shortest_dist = dist
                    closest_boid = boid.center

        return closest_boid

    def to_deg(selfself, rads):
        #angle = round(rads * 180 / numpy.pi)
        #if angle < 0:
        #    angle = abs(angle) * 180
        angle_in_degrees = math.degrees(rads)
        return angle_in_degrees

    def find_alignment(self, point):
        result = 0
        result = numpy.arctan2((point.y - self.center.y), point.x - self.center.x)
        result_bak = numpy.arctan2(point.y - self.center.y, point.x - self.center.x)

        # Below code is need as numpy.arctan2 returns -1 quadrant values, below code converts to positive radians 0 thru 6.2
        if result < 0:
            result = (numpy.pi - abs(result)) + numpy.pi

        result_degrees = (result * 180) / numpy.pi
        #print("Find Alignment: " + str(result))
        return result

    def alignment(self, boids, search_radius):
        total_theta = 0
        pivot = -1
        clock = 0
        counter = 0
        boid_dir = 0
        self_dir = 0
        in_area = self.search_area(boids, search_radius)
        for boid in in_area:
            total_theta += boid.theta
            delta = self.to_deg(self.theta) - self.to_deg(boid.theta)
            self_dir = self.to_deg(self.theta)
            boid_dir = self.to_deg(boid.theta)
            #if delta < 0:
            #    if abs(delta) > 180:
            #        clock += 1
            #    else:
            #        counter += 1
            #if delta > 0:
            #    if abs(delta) > 180:
            #        counter += 1
            #    else:
            #        clock += 1
            #print("Boid: " + str(boid_dir) + "Self: " + str(self_dir))

            #The self in right top and boid in right bottom ALSO if self in right bottom and boid in right top
            if (self_dir < 90) & (boid_dir > 270):
                clock += 1
            elif (self_dir > 270) & (boid_dir < 90):
                counter += 1
            elif boid_dir > self_dir:
                counter += 1
            elif boid_dir < self_dir:
                clock += 1

        #avg_alignment = total_theta / len(in_area)

        #delta = avg_alignment - self.theta
        '''
        if delta > numpy.pi:
            delta -= 2 * numpy.pi
        elif delta < -numpy.pi:
            delta += 2 * numpy.pi
        
        if delta > 0:
            pivot = 1
        elif delta < 0:
            pivot = -1
        '''

        pivot = 0
        if clock > counter:
            pivot = -1 * ROTATE_AMOUNT
        if counter > clock:
            pivot = 1 * ROTATE_AMOUNT

        return pivot

    def magic_wall(self):
        # right wall
        if self.center.x > CANVAS_WIDTH:
            for point in self.points:
                point.x -= (CANVAS_WIDTH - 5)
        # left wall
        elif self.center.x < 0:
            for point in self.points:
                point.x += (CANVAS_WIDTH - 5)
        # bottom wall
        if self.center.y > CANVAS_HEIGHT:
            for point in self.points:
                point.y -= (CANVAS_HEIGHT - 5)
        # top wall
        elif self.center.y < 0:
            for point in self.points:
                point.y += (CANVAS_HEIGHT - 5)


def create_boid(size):
    points = []
    x_offset = random.randrange(50, CANVAS_WIDTH - 50 - (4 * size))
    y_offset = random.randrange(50, CANVAS_HEIGHT - 50 - (2 * size))

    #Boids are created with positive y and x
    #what if these change

    # Added to make more randomness in initialization
    if random.randrange(0,3) > 1:
        xdir = -1
    else:
        xdir = 1

    if random.randrange(0,3) > 1:
        ydir = -1
    else:
        ydir = 1

    points.append(Point((4 * size) + x_offset * xdir, (1 * size) + y_offset * ydir))
    points.append(Point(0 + x_offset * xdir, (2 * size) + y_offset * ydir))
    points.append(Point(0 + x_offset * xdir, 0 + y_offset * ydir))

    #theta not initialized , hmm

    return points

# vector initialization
all_boids = []
for i in range(NUM_BOIDS):
    all_boids.append(Boid(create_boid(BOID_SCALE)))
for i in all_boids:
    rand_rotation = random.randrange(0, 359)
    i.rotate(rand_rotation)
    x_total = y_total = 0
    for point in i.points:
        x_total += point.x
        y_total += point.y
    # find the center based on current updated points
    i.center = Point(x_total / 3, y_total / 3)
    i.find_alignment(i.points[0])  #TEST


class Screen:
    def __init__(self, boid):
        points_list = []
        for point in boid.points:
            points_list.append([point.x, point.y])
        self.boid_list32 = numpy.array(points_list, numpy.int32)

    def draw_boid(self):
        cv2.fillPoly(background, [self.boid_list32], BOID_COLOR)

    def plot_center(self):
        cv2.circle(background, [round(each_boid.center.x), round(each_boid.center.y)], 3, CENTER_COLOR_DOT, -1)
    def plot_corners(self):
        cv2.circle(background, [round(each_boid.points[0].x), round(each_boid.points[0].y)], 3, CENTER_OF_MASS_LINE_COLOR, -1)
        cv2.circle(background, [round(each_boid.points[1].x), round(each_boid.points[1].y)], 3, CENTER_COLOR_DOT, -1)
        cv2.circle(background, [round(each_boid.points[2].x), round(each_boid.points[2].y)], 3, CENTER_COLOR_DOT, -1)

    def draw_alignment_line(self):
        cv2.line(background, (round(each_boid.points[0].x), round(each_boid.points[0].y)), (round(each_boid.center.x), round(each_boid.center.y)), ALIGNMENT_LINE_COLOR, 1)

    def draw_vision(self):
        cv2.circle(background, [round(each_boid.center.x), round(each_boid.center.y)], VISION_RADIUS, VISION_COLOR)

    def draw_com(self):
        center_of_mass = each_boid.find_com(all_boids, VISION_RADIUS)
        cv2.line(background, [round(each_boid.center.x), round(each_boid.center.y)],
                 [round(center_of_mass.x), round(center_of_mass.y)], CENTER_OF_MASS_LINE_COLOR, 1)

    def draw_closest(self):
        apple = each_boid.find_closest_boid(all_boids, VISION_RADIUS)
        if apple != None:
            cv2.line(background, (round(each_boid.center.x), round(each_boid.center.y)),
                     (round(apple.x), round(apple.y)), ALIGNMENT_LINE_COLOR, 1)


# game loop
some_time = 10
each_time = 1
background = 0
for i in range(100):
    # Create canvas

    if each_time > some_time:
        background = numpy.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 3), numpy.uint8)
        background.fill(0)
    # changes for each individual boid
        counter = 0
        for each_boid in all_boids:
            screen = Screen(each_boid)
            points_list = []
            counter += 1

        # translations
            each_boid.controller()

        # create magic walls
            each_boid.magic_wall()

        # update boid with new info
            each_boid.update()

        # plot boid
            screen.draw_boid()

        # plot center point
            screen.plot_center()

        # plot boid points
            screen.plot_corners()

        # plot alignment line
            screen.draw_alignment_line()

        # plot vision circle
            screen.draw_vision()
        # find closest boid
            screen.draw_com()
            screen.draw_closest()
        some_time += SIM_SLOW_SPEED

    each_time += 1
    # display drawings
    cv2.imshow('Boids', background)
    cv2.waitKey(SLEEP_TIME)

