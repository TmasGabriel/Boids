from boid import *
from __init__ import *


def find_mid(top, bot, left, right):
    middle = round((right + left) / 2), round((bot + top) / 2)

    return middle


def find_dim(top, bot, left, right):
    width = right - left
    height = bot - top
    return width, height

def detect_quad(boid, top, bot, left, right, mid):
    quad = 0
    t, b, l, r = 0, 0, 0, 0
    if mid[0] < boid.center[0] < right:
        if top < boid.center[1] < mid[1]:
            quad = 1
            t, b, l, r = top, mid[1], mid[0], right
        elif mid[1] < boid.center[1] < bot:
            quad = 4
            t, b, l, r = mid[1], bot, mid[0], right
        else:
            print('out of bounds')
    elif left < boid.center[0] < mid[0]:
        if top < boid.center[1] < mid[1]:
            quad = 2
            t, b, l, r = top, mid[1], left, mid[0]
        elif mid[1] < boid.center[1] < bot:
            quad = 3
            t, b, l, r = mid[1], bot, left, mid[0]
        else:
            print('out of bounds')
    else:
        print('out of bounds')

    return quad, t, b, l, r


def find_adj(quad, top, bot, left, right):
    width, height = find_dim(top, bot, left, right)
    t = top - height
    b = bot + height
    l = left - width
    r = right + width
    return t, b, l, r
    """
    if quad == 1:
        t = top - height
        b = bot + height
        l = left - width
        r = right + width
        return t, b, l, r
    elif quad == 2:
        t = bot + (height * 2)
        l = left - (width * 2)
        return t, bot, l, right
    elif quad == 3:
        b = bot - (height * 2)
        l = left - (width * 2)
        return top, b, l, right
    elif quad == 4:
        b = bot - (height * 2)
        r = left + (width * 2)
        return top, b, left, r
    else:
        print('out of bounds 2')
    """