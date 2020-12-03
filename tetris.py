import curses
from os import system

max_grid_height = 20
max_grid_width = 15
min_grid_height = 0
min_grid_width = 0
game_run = 1
STRAIGHT_BLOCK_X = [7, 6, 5, 4]
STRAIGHT_BLOCK_Y = [0, 0, 0, 0]

system("clear")
screen = curses.initscr()
curses.noecho()
curses.cbreak()


def printscreen():
    y = min_grid_height
    screen.clear()
    while y < max_grid_height:

        x = min_grid_width
        while x < max_grid_width:

            screen.addstr(y, x, "-")

            i = 0
            while i < len(STRAIGHT_BLOCK_X):

                if x == STRAIGHT_BLOCK_X[i] and y == STRAIGHT_BLOCK_Y[i]:

                    screen.addstr(y, x, "*")

                i += 1

            x += 1

        y += 1
    screen.refresh()

while game_run == 1:
    printscreen()
    system ("sleep 1")
    i = 0
    while i < len(STRAIGHT_BLOCK_Y):
        STRAIGHT_BLOCK_Y[i] = STRAIGHT_BLOCK_Y[i] + 1
        if STRAIGHT_BLOCK_Y[i] == max_grid_height:
            break
        i += 1
