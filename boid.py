import numpy as np
import random

from __init__ import *


def find_avg_theta(abs_total_theta, area, too_close, total_theta):
    avg_theta = abs_total_theta / (len(area) - len(too_close)) * np.sign(total_theta)

    return avg_theta


def find_center_of_mass(total_mass, num_boids_in_area):
    center_of_mass = (total_mass[0] / num_boids_in_area, total_mass[1] / num_boids_in_area)

    return center_of_mass


class Boid:
    def __init__(self, bow, port, starboard):
        self.bow = bow
        self.port = port
        self.star = starboard
        self.verts = [self.bow, self.port, self.star]

        self.center = ((self.bow[0] + self.port[0] + self.star[0]) / 3,
                       (self.bow[1] + self.port[1] + self.star[1]) / 3)

        self.theta = self.find_theta(self.bow)

        self.speed = MAX_SPEED

    def update(self, boids):
        total_mass = [0, 0]
        shortest_dist = VISION_RADIUS
        closest_boid = None
        total_theta = 0
        comb_theta = 0
        direct_in_front = []

        area = self.search_area(boids, VISION_RADIUS)
        too_close = self.search_area(area, FEEL_RADIUS)
        crash = self.search_area(too_close, CRASH_RADIUS)

        if len(area) > 0:
            for boid in area:
                if boid not in too_close:
                    total_mass = [total_mass[0] + boid.center[0], total_mass[1] + boid.center[1]]
                    comb_theta += boid.theta
                    total_theta += abs(boid.theta)

                    if self.is_in_cone(boid.bow, np.pi / 8):
                        direct_in_front.append(boid)

                closest_boid, shortest_dist = self.find_closest_boid(boid, closest_boid, shortest_dist)

            if len(too_close) > 0:
                self.turn_to(closest_boid.center, extra_mult=-1)
            elif len(direct_in_front) > 0:
                self.turn_to(direct_in_front[0].bow, extra_mult=-1)
            else:
                center_of_mass = find_center_of_mass(total_mass, len(area) - len(too_close))
                self.turn_to(center_of_mass)

                avg_alignment = find_avg_theta(total_theta, area, too_close, comb_theta)
                self.turn_to(None, target_theta=avg_alignment)

        self.move(self.theta)

        self.center = ((self.bow[0] + self.port[0] + self.star[0]) / 3,
                       (self.bow[1] + self.port[1] + self.star[1]) / 3)
        self.theta = self.find_theta(self.bow)

        return len(crash)

    def find_theta(self, point):  # (from center)
        return np.arctan2(point[1] - self.center[1], point[0] - self.center[0])

    def rotate(self, degrees):
        new_pos = [None, None, None]
        angle_rad = np.deg2rad(degrees)
        sin_angle = np.sin(angle_rad)
        cos_angle = np.cos(angle_rad)

        for vert in self.verts:
            dist_x = vert[0] - self.center[0]
            dist_y = vert[1] - self.center[1]

            vert[0] = (dist_x * cos_angle) - (dist_y * sin_angle) + self.center[0]
            vert[1] = (dist_x * sin_angle) + (dist_y * cos_angle) + self.center[1]

        return new_pos

    def move(self, direction):
        sin_angle = np.sin(direction)
        cos_angle = np.cos(direction)
        for vert in self.verts:
            vert[0] += (self.speed * cos_angle)
            vert[1] += (self.speed * sin_angle)

    def search_area(self, boids, search_rad):
        in_area = []
        self_x = int(self.center[0])
        self_y = int(self.center[1])
        for boid in boids:
            boid_x = int(boid.center[0])
            boid_y = int(boid.center[1])

            if boid is not self:
                if boid_x in range(self_x - search_rad, self_x + search_rad):
                    if boid_y in range(self_y - search_rad, self_y + search_rad):
                        if (((boid_x - self_x) ** 2) + ((boid_y - self_y) ** 2)) ** .5 < search_rad:
                            perf = self.is_in_cone(boid.center, (np.pi * 3) / 2)
                            if perf:
                                in_area.append(boid)


        return in_area

    def is_in_cone(self, target, width_rad):
        V2 = [target[0] - self.center[0], target[1] - self.center[1]]
        dot_product = np.cos(self.theta) * V2[0] + np.sin(self.theta) * V2[1]

        mag_v1 = np.sqrt(np.cos(self.theta) ** 2 + np.sin(self.theta) ** 2)
        mag_v2 = np.sqrt(V2[0] ** 2 + V2[1] ** 2)

        # Avoid division by zero
        if mag_v1 * mag_v2 == 0:
            return False

        angle = np.arccos(dot_product / (mag_v1 * mag_v2))

        # Check if the target is within the cone
        return angle <= width_rad / 2

    def dir_to_turn(self, target=None, target_theta=None):
        if target_theta is None:
            target_theta = self.find_theta(target)
        delta = target_theta - self.theta
        delta_sin = round(np.sin(delta))

        if delta_sin < 0:
            # turn clockwise
            to_turn = -1
        elif delta_sin > 0:
            # turn clockwise
            to_turn = 1
        else:
            # dont turn
            to_turn = 0

        return to_turn

    def turn_to(self, target, extra_mult=1, target_theta=None):
        self.rotate(self.dir_to_turn(target, target_theta) * ROTATION * extra_mult)

    def find_closest_boid(self, boid, closest_boid, shortest_dist):
        dist = abs(self.center[0] - boid.center[0]) + abs(self.center[1] - boid.center[1])
        if dist < shortest_dist:
            shortest_dist = dist
            closest_boid = boid

        return closest_boid, shortest_dist

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
