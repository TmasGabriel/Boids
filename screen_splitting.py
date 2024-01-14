from boid import *
from __init__ import *


def find_mid(left, right, top, bot):
    middle = round((right + left) / 2), round((bot + top) / 2)

    return middle


def find_dimensions(left, right, top, bot):
    width = right - left
    height = bot - top
    return width, height


def detect_quad(boid, left, right, top, bot, mid):
    quad = 0
    left_bound, right_bound, top_bound, bot_bound = None, None, None, None
    if top < boid.center[1] < mid[1]:
        if mid[0] < boid.center[0] < right:
            quad = 1
            left_bound, right_bound, top_bound, bot_bound = mid[0], right, top, mid[1]
        elif left < boid.center[0] < mid[0]:
            quad = 2
            left_bound, right_bound, top_bound, bot_bound = mid[0], right, mid[1], bot
        else:
            print('out of bounds 1')

    elif mid[1] < boid.center[1] < bot:
        if left < boid.center[0] < mid[0]:
            quad = 3
            left_bound, right_bound, top_bound, bot_bound = left, mid[0], mid[1], bot
        elif mid[0] < boid.center[0] < right:
            quad = 4
            left_bound, right_bound, top_bound, bot_bound = mid[0], right, mid[1], bot
        else:
            print('out of bounds 2')
    else:
        print('out of bounds 3')

    return quad, left_bound, right_bound, top_bound, bot_bound

def find_adj(left, right, top, bot, width, height):
    left_bound = left - width
    right_bound = right + width
    top_bound = top - height
    bot_bound = bot + height
    return left_bound, right_bound, top_bound, bot_bound


def generate_quad_id(boid, depth):
    left, right, top, bot = 0, CANVAS_WIDTH, 0, CANVAS_HEIGHT
    middle = find_mid(left, right, top, bot)

    for i in range(depth):
        quad, left, right, top, bot = detect_quad(boid, left, right, top, bot, middle)
        middle = find_mid(left, right, top, bot)

    return left, right, top, bot, middle
