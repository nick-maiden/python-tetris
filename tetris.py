import curses
from os import system
import time

max_grid_height = 20
max_grid_width = 15
min_grid_height = 0
min_grid_width = 0
game_run = 1
STRAIGHT_BLOCK_XS = [[0, 1, 2, 3], [0, 0, 0, 0], [0, 1, 2, 3], [0, 0, 0, 0]]
STRAIGHT_BLOCK_YS = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 0, 0, 0], [0, 1, 2, 3]]
STRAIGHT_BLOCK_X_OFFSETS = [2, -2, 1, -1]
STRAIGHT_BLOCK_Y_OFFSETS = [-1, 1, -1, 1]
rotation_index = 0
frame = 1
MOVE_FRAME = 10
block_x = 0
block_y = 0

system("clear")
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

def draw_char(x, y, c):
    screen.addstr(y, x*2, c)

def draw_block(STRAIGHT_BLOCK_X, STRAIGHT_BLOCK_Y, block_x, block_y):
    i = 0
    while i < len(STRAIGHT_BLOCK_X):
        draw_char(STRAIGHT_BLOCK_X[i] + block_x, STRAIGHT_BLOCK_Y[i] + block_y, "*")
        i += 1



def print_background():
    global y
    y = min_grid_height
    while y < max_grid_height:

        global x
        x = min_grid_width
        while x < max_grid_width:

            draw_char(x, y, "-")

            x += 1

        y += 1

screen.nodelay(True)
while game_run == 1:
    screen.clear()
    print_background()
    draw_block(STRAIGHT_BLOCK_XS[rotation_index], STRAIGHT_BLOCK_YS[rotation_index], block_x, block_y)
    screen.refresh()
    if frame % MOVE_FRAME == 0:
        if block_y < max_grid_height - 1:
            block_y += 1
        else:
            block_y = max_grid_height - 1


    try:
        move = screen.getkey()
    except:
        move = ""

    if move == "w":
        block_x += STRAIGHT_BLOCK_X_OFFSETS[rotation_index]
        block_y += STRAIGHT_BLOCK_Y_OFFSETS[rotation_index]
        rotation_index = (rotation_index + 1) % 4

    if move == "a":
        block_x -= 1

    if move == "d":
        block_x += 1

    if move == "s":
        block_y += 1

    if move == "q":
        game_run = 0

    time.sleep(0.033)
    frame += 1
