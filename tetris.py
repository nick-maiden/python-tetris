import curses
from os import system

max_grid_height = 20
max_grid_width = 15
min_grid_height = 0
min_grid_width = 0
game_run = 1
STRAIGHT_BLOCK_X = [7, 6, 5, 4]
STRAIGHT_BLOCK_Y = [0, 0, 0, 0]
block_x = 0
block_y = 0

system("clear")
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

def draw_block(STRAIGHT_BLOCK_X, STRAIGHT_BLOCK_Y, block_x, block_y):
    i = 0
    while i < len(STRAIGHT_BLOCK_X):
        screen.addstr(STRAIGHT_BLOCK_Y[i] + block_y, STRAIGHT_BLOCK_X[i] + block_x, "*")
        i += 1



def print_background():
    global y
    y = min_grid_height
    while y < max_grid_height:

        global x
        x = min_grid_width
        while x < max_grid_width:

            screen.addstr(y, x, "-")

            x += 1

        y += 1

while game_run == 1:
    screen.clear()
    print_background()
    draw_block(STRAIGHT_BLOCK_X, STRAIGHT_BLOCK_Y, block_x, block_y)
    screen.refresh()
    system ("sleep 1")
    if block_y < max_grid_height - 1:
        block_y += 1
    else:
        block_y = max_grid_height - 1


    screen.nodelay(True)
    try:
        move = screen.getkey()
    except:
        move = ""

    if move == "q":
        game_run = 0
