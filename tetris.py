import curses
from os import system
import time
import random

STRAIGHT_BLOCK_XS = [[-2, -1, 0, 1], [0, 0, 0, 0], [-2, -1, 0, 1], [-1, -1, -1, -1]]
STRAIGHT_BLOCK_YS = [[0, 0, 0, 0], [-2, -1, 0, 1], [0, 0, 0, 0], [-2, -1, 0, 1]]
L_BLOCK_LEFT_XS = [[0, 0, -1, 0], [-1, -1, 0, 1], [0, 1, 0, 0], [-1, 0, 1, 1]]
L_BLOCK_LEFT_YS = [[-1, 0, 1, 1], [-1, 0, 0, 0], [-1, -1, 0, 1], [0, 0, 0, 1]]
L_BLOCK_RIGHT_XS =[[0, 0, 0, 1], [-1, 0, 1, -1], [-1, 0, 0, 0], [1, -1, 0, 1]]
L_BLOCK_RIGHT_YS = [[-1, 0, 1, 1], [0, 0, 0, 1], [-1, -1, 0, 1], [-1, 0, 0, 0]]
Z_BLOCK_LEFT_XS = [[-1, 0, 0, 1], [0, -1, 0, -1], [-1, 0, 0, 1], [1, 0, 1, 0]]
Z_BLOCK_LEFT_YS = [[0, 0, 1, 1], [-1 ,0, 0, 1], [-1, -1, 0, 0], [-1 ,0, 0, 1]]
Z_BLOCK_RIGHT_XS = [[0, 1, -1, 0], [-1, -1, 0, 0], [0, 1, -1, 0], [0, 0, 1, 1]]
Z_BLOCK_RIGHT_YS = [[0, 0, 1, 1], [-1, 0, 0, 1], [-1, -1, 0, 0], [-1, 0, 0, 1]]
PYRAMID_BLOCK_XS = [[0, -1, 0, 1], [0, 0, 1, 0], [-1, 0, 1, 0], [0, -1, 0, 0]]
PYRAMID_BLOCK_YS = [[-1, 0, 0, 0], [-1, 0, 0, 1], [0, 0, 0, 1], [-1, 0, 0, 1]]
SQUARE_BLOCK_XS = [[0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 1]]
SQUARE_BLOCK_YS = [[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1]]


BLOCK_XS = [STRAIGHT_BLOCK_XS, L_BLOCK_LEFT_XS, L_BLOCK_RIGHT_XS, Z_BLOCK_LEFT_XS, Z_BLOCK_RIGHT_XS, PYRAMID_BLOCK_XS, SQUARE_BLOCK_XS]
BLOCK_YS = [STRAIGHT_BLOCK_YS, L_BLOCK_LEFT_YS, L_BLOCK_RIGHT_YS, Z_BLOCK_LEFT_YS, Z_BLOCK_RIGHT_YS, PYRAMID_BLOCK_YS, SQUARE_BLOCK_YS]


grid_height = 20
grid_width = 15
min_grid_y = 2
min_grid_x = 5
game_run = 1
STANDARD_BLOCK_LENGTH = 4
block_index = random.randint(0, 6)
NUM_BLOCK_SORTS = 7
rotation_index = 0
frame = 1
MOVE_FRAME = 10
block_x = 0
block_y = 0
saved_block_array_ys = []
saved_block_array_xs = []
z = -1
debug_texts = []

system("clear")
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

def draw_debug():
    i = 0
    while i < len(debug_texts):
        screen.addstr(i, (min_grid_x + grid_width + 1)*2, debug_texts[i])
        i += 1

def draw_char(x, y, c):
    screen.addstr(y, x*2, c)



def bump_amount(block_xs):
    f = lambda x: x + block_x
    new_block_xs = list(map(f, block_xs))
    minimum = min(new_block_xs)
    if minimum < 0:
        return -minimum
    maximum = max(new_block_xs)
    max_grid_x = grid_width - 1
    if maximum > max_grid_x:
        return (max_grid_x - maximum)
    return 0

def collision_check(block_x, block_y, block_xs, block_ys):
    f = lambda x: x + block_x
    abs_block_xs = list(map(f, block_xs))
    l = lambda y: y + block_y
    abs_block_ys = list(map(l, block_ys))

    i = 0
    while i < STANDARD_BLOCK_LENGTH:
        d = 0
        if abs_block_ys[i] >= grid_height:
            return True
        while d < len(saved_block_array_ys):
            if abs_block_xs[i] == saved_block_array_xs[d] and abs_block_ys[i] == saved_block_array_ys[d]:
                return True
            d += 1
        i += 1
    return False

# def moving_right_collision_check(block_xs, block_ys):
#     f = lambda x: x + block_x
#     new_block_xs = list(map(f, block_xs))
#     maximum = max(new_block_xs) + 1               #<< +1 is to indicate when we are
#     l = lambda y: y + block_y                     # one step away from a collision
#     new_block_ys = list(map(l, block_ys))
#
#     i = 0
#     while i < STANDARD_BLOCK_LENGTH:
#         d = 0
#         while d < len(saved_block_array_ys):
#             if maximum == saved_block_array_xs[d] and new_block_ys[i] == saved_block_array_ys[d]:
#                 return 1
#             d += 1
#         i += 1
#     return 0




#checks for bottom of board
#returns True if past the bottom of the board
def board_bottom_check(block_ys, block_xs, block_y):
    current_pos = max(block_ys)
    if current_pos + block_y >= grid_height - 1:
        return {'current_pos':current_pos,'past_bottom':True}
    d = 0
    while d < STANDARD_BLOCK_LENGTH:
        i = 0
        while i < len(saved_block_array_ys):
            abs_block_y = block_ys[d] + block_y
            abs_block_x = block_xs[d] + block_x
            if abs_block_y == saved_block_array_ys[i] - 1 and abs_block_x == saved_block_array_xs[i]:
                return {'current_pos':current_pos,'past_bottom':False, 'collision_y':abs_block_y}


            i += 1
        d += 1
    return {'current_pos':current_pos,'past_bottom':False}


def draw_saved_blocks(block_x, block_y):
    i = 0
    while i < len(saved_block_array_xs):
        x = saved_block_array_xs[i] + min_grid_x
        y = saved_block_array_ys[i] + min_grid_y
        draw_char(x, y, "*")

        i += 1



def draw_block(BLOCK_XS, BLOCK_YS, block_x, block_y):
    i = 0
    while i < STANDARD_BLOCK_LENGTH:
        x = BLOCK_XS[i] + block_x + min_grid_x
        y = BLOCK_YS[i] + block_y + min_grid_y
        if x >= min_grid_x and x < min_grid_x + grid_width and y >= min_grid_y and y < min_grid_y + grid_height:
            draw_char(x, y, "*")

        i += 1



def print_background():
    global y
    y = min_grid_y
    while y < min_grid_y + grid_height:

        global x
        x = min_grid_x
        while x < min_grid_x + grid_width:

            draw_char(x, y, "-")

            x += 1

        y += 1


def add_to_saved_blocks():
    global saved_block_array_xs
    global saved_block_array_ys
    final_block_xs = []
    final_block_ys = []
    i = 0
    while i < STANDARD_BLOCK_LENGTH:
        final_block_xs.append(BLOCK_XS[block_index][rotation_index][i] + block_x)
        final_block_ys.append(BLOCK_YS[block_index][rotation_index][i] + block_y)
        i += 1
    saved_block_array_xs = saved_block_array_xs + final_block_xs
    saved_block_array_ys = saved_block_array_ys + final_block_ys




# MAIN GAME LOOP BELOW

screen.nodelay(True)
while game_run == 1:
    screen.clear()
    print_background()
    block_x += bump_amount(BLOCK_XS[block_index][rotation_index])




    # result = board_bottom_check(BLOCK_YS[block_index][rotation_index], BLOCK_XS[block_index][rotation_index], block_y)
    # if result['past_bottom']:
    #     block_y = grid_height - result['current_pos'] - 1
    #
    # if 'collision_y' in result or result['past_bottom']:
    #     final_block_xs = []
    #     final_block_ys = []
    #     i = 0
    #     while i < STANDARD_BLOCK_LENGTH:
    #         final_block_xs.append(BLOCK_XS[block_index][rotation_index][i] + block_x)
    #         final_block_ys.append(BLOCK_YS[block_index][rotation_index][i] + block_y)
    #         i += 1
    #     saved_block_array_xs = saved_block_array_xs + final_block_xs
    #     saved_block_array_ys = saved_block_array_ys + final_block_ys
    #     block_index = random.randint(0, 6)
    #     block_y = 0


    draw_saved_blocks(block_x, block_y)
    draw_block(BLOCK_XS[block_index][rotation_index], BLOCK_YS[block_index][rotation_index], block_x, block_y)
    draw_debug()
    screen.refresh()


    try:
        move = screen.getkey()
        curses.flushinp()
    except:
        move = ""

    if move == "w":
        new_rotation_index = (rotation_index + 1) % 4
        if not collision_check(block_x, block_y, BLOCK_XS[block_index][new_rotation_index], BLOCK_YS[block_index][new_rotation_index]):
            rotation_index = (rotation_index + 1) % 4

    if move == "a":
        if not collision_check(block_x - 1, block_y, BLOCK_XS[block_index][rotation_index], BLOCK_YS[block_index][rotation_index]):
            block_x -= 1

    if move == "d":
        if not collision_check(block_x + 1, block_y, BLOCK_XS[block_index][rotation_index], BLOCK_YS[block_index][rotation_index]):
            block_x += 1

    if move == "s" or frame % MOVE_FRAME == 0:
        if collision_check(block_x, block_y + 1, BLOCK_XS[block_index][rotation_index], BLOCK_YS[block_index][rotation_index]):
            add_to_saved_blocks()
            block_index = random.randint(0, 6)
            block_y = 0
        else:
            block_y += 1

    if move == "q":
        game_run = 0


    time.sleep(0.033)
    frame += 1
