import numpy as np
import random
from __init__2 import *


# my interpretation of boids in this instance is just a point with a direction
class Boid:
    def __init__(self, position, theta):
        self.pos = position
        self.vel = INIT_VEL  # velocity is the derivative of position
        self.vel_x = self.vel * np.cos(theta)
        self.vel_y = self.vel * np.sin(theta) * -1
        self.acc = float  # acceleration is the derivative of velocity
        self.theta = theta

    def search_area(self, boids, search_rad):
        in_area = []
        for boid in boids:
            if boid is not self:
                if self.find_dist(boid.pos) < search_rad:
                    in_area.append(boid)

        return in_area

    def find_dist(self, target_pos):
        distance = ((target_pos[0] - self.pos[0]) ** 2 + (target_pos[1] - self.pos[1]) ** 2) ** .5
        return distance

    def find_closest(self, boid, dist, closest_boid, shortest_dist):
        if dist < shortest_dist:
            shortest_dist = dist
            closest_boid = boid

        return closest_boid, shortest_dist

    def simple_avoid(self, closest):
        impact_factor = 1
        away_vector = np.array(self.pos) - np.array(closest.pos)
        foo = impact_factor / away_vector[0]
        bar = impact_factor / away_vector[1]
        if abs(foo) < impact_factor:
            self.vel_x += foo
        if abs(bar) < impact_factor:
            self.vel_y -= bar

    def calculate(self, in_range):
        closest, shortest = None, VISION_RADIUS
        area = self.search_area(in_range, VISION_RADIUS)
        for boid in area:
            dist = self.find_dist(boid.pos)
            closest, shortest = self.find_closest(boid, dist, closest, shortest)


        if closest:
            self.simple_avoid(closest)

            if self.find_dist(closest.pos) < 5:
                print('crash')
        return [closest]

    def update(self):
        # arctan only has a range of [-pi/2, pi/2] so use arctan2 which has a range of [-pi, pi]
        self.theta = np.arctan2(self.vel_y, self.vel_x)

        self.pos = [round(self.vel_x + self.pos[0]),
                    round(self.vel_y * -1 + self.pos[1])]

    def magic_wall(self, width, height):
        # right wall
        if self.pos[0] > width:
            self.pos[0] -= (width - 5)
        # left wall
        elif self.pos[0] < 0:
            self.pos[0] += (width - 5)
        # bottom wall
        if self.pos[1] > height:
            self.pos[1] -= (height - 5)
        # top wall
        elif self.pos[1] < 0:
            self.pos[1] += (height - 5)


def spawn_boid(x, y, degrees):
    rads = np.deg2rad(degrees)
    return Boid([x, y], rads)


def spawn_boids_randomly(num_boids, left=0, right=1000, top=0, bot=1000, deg_bot=0, deg_top=359):
    boids = []
    for i in range(num_boids):
        pos = [random.randrange(left, right + 1), random.randrange(top, bot + 1)]
        theta = random.randrange(deg_bot, deg_top + 1)
        boids.append(spawn_boid(pos[0], pos[1], theta))
    return boids
