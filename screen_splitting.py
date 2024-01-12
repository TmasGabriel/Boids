from boid import *
from __init__ import *


def find_mid(top, bot, left, right):
    width = right + left
    height = bot + top
    middle = round(width / 2), round(height / 2)

    return middle


def detect_quad(boid, top, bot, left, right, mid):
    quad = 0
    t, b, l, r = 0, 0, 0, 0
    if mid[0] < boid.center[0] < right:
        if top < boid.center[1] < mid[1]:
            print('in top right')
            quad = 1
            t, b, l, r = top, mid[1], mid[0], right
        elif mid[1] < boid.center[1] < bot:
            print('in bot right')
            quad = 4
            t, b, l, r = mid[1], bot, mid[0], right
        else:
            print('out of bounds')
    elif left < boid.center[0] < mid[0]:
        if top < boid.center[1] < mid[1]:
            print('in top left')
            quad = 2
            t, b, l, r = top, mid[1], left, mid[0]
        elif mid[1] < boid.center[1] < bot:
            print('in bot left')
            quad = 3
            t, b, l, r = mid[1], bot, left, mid[0]
        else:
            print('out of bounds')
    else:
        print('out of bounds')

    return quad, t, b, l, r
