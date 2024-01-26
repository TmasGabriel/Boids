import numpy as np
import random


def find_vel(speed, direction):
    new_velocity = []
    for axis in direction:
        new_velocity.append(speed * axis)
    return new_velocity


# my interpretation of boids in this instance is just a point with a direction
class Boid:
    def __init__(self, position, theta):
        self.pos = position
        self.theta = theta

        # turn theta into a value on the range [-1, 1] for x and y axis's
        # invert y value because graphical interfaces have inverted y-axis's
        self.dir = (np.cos(self.theta), np.sin(self.theta) * -1)
        self.vel = [0, 0]
        self.speed = 0

    def search_area(self, boids, search_rad):
        in_area = []
        self_x = int(self.pos[0])
        self_y = int(self.pos[1])
        for boid in boids:
            boid_x = int(boid.pos[0])
            boid_y = int(boid.pos[1])

            if boid is not self:
                if boid_x in range(self_x - search_rad, self_x + search_rad):
                    if boid_y in range(self_y - search_rad, self_y + search_rad):
                        if (((boid_x - self_x) ** 2) + ((boid_y - self_y) ** 2)) ** .5 < search_rad:
                            in_area.append(boid)

        return in_area

    def is_in_cone(self, target, width_rad):
        V2 = [target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]]
        dot_product = np.cos(self.theta) * V2[0] + np.sin(self.theta) * V2[1]

        mag_v1 = np.sqrt(np.cos(self.theta) ** 2 + np.sin(self.theta) ** 2)
        mag_v2 = np.sqrt(V2[0] ** 2 + V2[1] ** 2)

        # Avoid division by zero
        if mag_v1 * mag_v2 == 0:
            return False

        angle = np.arccos(dot_product / (mag_v1 * mag_v2))

        # Check if the target is within the cone
        return angle <= width_rad / 2

    def move(self, speed):
        self.vel = find_vel(speed, self.dir)
        self.pos = [self.pos[i] + self.vel[i] for i in range(len(self.vel))]

        return self.pos

    def rotate(self, angle):
        ang_rad = np.deg2rad(angle)
        self.theta += ang_rad
        self.dir = (np.cos(self.theta), np.sin(self.theta) * -1)

    def find_dist(self, target):
        distance = [int(target[0] - self.pos[0]), int(target[1] - self.pos[1])]
        return distance

    def find_closest(self, boid, dist, closest_boid, shortest_dist):
        tot_dist = abs(dist[0]) + abs(dist[1])
        if tot_dist < shortest_dist:
            shortest_dist = tot_dist
            closest_boid = boid

        return closest_boid, shortest_dist

    def find_cross(self, other):
        self_slope = self.dir[1] / self.dir[0]
        other_slope = other.dir[1] / other.dir[0]
        self_y_int = self.pos[1] - (self_slope * self.pos[0])
        other_y_int = other.pos[1] - (other_slope * other.pos[0])

        if self_slope - other_slope == 0:
            return None
        x = (other_y_int - self_y_int) / (self_slope - other_slope)
        y = self_slope * x + self_y_int

        d = [x - self.pos[0], y - self.pos[1], x - other.pos[0], y - other.pos[1]]

        if np.sign(d[0]) != np.sign(self.dir[0]):
            return None
        if np.sign(d[1]) != np.sign(self.dir[1]):
            return None
        if np.sign(d[2]) != np.sign(other.dir[0]):
            return None
        if np.sign(d[3]) != np.sign(other.dir[1]):
            return None

        return [x, y]

    def dir_to_turn(self, target):
        dist = self.find_dist(target)
        cross = float(np.cross(self.dir, dist))

        if cross > 0:
            turn = -1
        elif cross < 0:
            turn = 1
        else:
            turn = 0
        return turn

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

    def calculate(self, in_range, target):
        closest, shortest, intersection, seperation = None, 10000, None, 0
        # dir_to_turn = self.dir_to_turn(target)
        area = self.search_area(in_range, 100)
        for boid in area:
            dist = self.find_dist(boid.pos)
            closest, shortest = self.find_closest(boid, dist, closest, shortest)

        if closest:
            intersection = self.find_cross(closest)
            if intersection:
                seperation = self.dir_to_turn(intersection)
        return [seperation, closest, intersection]

    def update(self, speed, rotation, dir_to_turn):
        self.rotate(dir_to_turn * rotation)
        self.move(speed)


def spawn_boids_randomly(num_boids, left=0, right=1000, top=0, bot=1000, deg_bot=0, deg_top=359):
    boids = []
    for i in range(num_boids):
        pos = [random.randrange(left, right + 1), random.randrange(top, bot + 1)]
        theta = np.deg2rad(random.randrange(deg_bot, deg_top + 1))
        boids.append(Boid(pos, theta))
    return boids
