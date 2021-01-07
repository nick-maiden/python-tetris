import curses
from os import system
import time
import random

grid_height = 20
grid_width = 15
min_grid_y = 2
min_grid_x = 5
game_run = 1
STANDARD_BLOCK_LENGTH = 4

#STRAIGHT_BLOCK_XS = [0, 1, 2, 3], [2, 2, 2, 2], [0, 1, 2, 3], [3, 3, 3, 3]]
#STRAIGHT_BLOCK_YS = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 0, 0, 0], [0, 1, 2, 3]]
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



#block_index = random.randint(0, 2)
block_index = 3
NUM_BLOCK_SORTS = 7
rotation_index = 0
frame = 1
MOVE_FRAME = 10
block_x = 0
block_y = 0
#NEGATIVE_VALUE_FACTOR = 2

system("clear")
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

def draw_char(x, y, c):
    screen.addstr(y, x*2, c)

def bump_amount(block_xs):
    f = lambda x: x + block_x
    new_block_xs = list(map(f, block_xs))
    minimum = min(new_block_xs)
    if minimum < 0:
        return -minimum
    maximum = max(new_block_xs)
    max_grid_x = min_grid_x + grid_width - 1
    if maximum > max_grid_x:
        return (maximum - max_grid_x)
    return 0


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

screen.nodelay(True)
while game_run == 1:
    screen.clear()
    print_background()
    block_x += bump_amount(BLOCK_XS[block_index][rotation_index])
    draw_block(BLOCK_XS[block_index][rotation_index], BLOCK_YS[block_index][rotation_index], block_x, block_y)
    screen.refresh()
    if frame % MOVE_FRAME == 0:
        block_y += 1
        #i = 0
        #while i < STANDARD_BLOCK_LENGTH:

        #    if BLOCK_YS[block_index][rotation_index][i] < grid_height - 1:
        #        block_y += 1
        #    else:
        #        block_y = grid_height - 1
        #    i += 1

    try:
        move = screen.getkey()
    except:
        move = ""

    if move == "w":
        #block_x += STRAIGHT_BLOCK_X_OFFSETS[rotation_index]
        #block_y += STRAIGHT_BLOCK_Y_OFFSETS[rotation_index]
        rotation_index = (rotation_index + 1) % 4

    if move == "a":
        block_x -= 1

    if move == "d":
        block_x += 1

    if move == "s":
        block_y += 1

    if move == "q":
        game_run = 0

    if move == "p":
        block_index = (block_index + 1) % NUM_BLOCK_SORTS
        block_y = 0


    time.sleep(0.033)
    frame += 1
