import curses
import time
from curses.textpad import rectangle
from snake import Snake
from game import Game
from rabbit import Rabbit
from configurations import HEIGHT, WIDTH, TOP_PADDING, LEFT_PADDING, MARGIN, SCREEN_TOP, SCREEN_WIDTH, STROKE_TOP, STROKE_LEFT


stdscr = curses.initscr()

colors = {'white': curses.COLOR_WHITE, 'red': curses.COLOR_RED, 'green': curses.COLOR_GREEN,
          'yellow': curses.COLOR_YELLOW, 'blue': curses.COLOR_BLUE, 'magenta': curses.COLOR_MAGENTA,
          'cyan': curses.COLOR_CYAN, 'black': curses.COLOR_BLACK}

def scr_configuration(p_stdscr):
    curses.start_color()
    curses.use_default_colors()
    set_pairs(1, 1)
    curses.cbreak()  # avoid close window after input
    curses.curs_set(0)  # hide cursor
    curses.resize_term(SCREEN_TOP, SCREEN_WIDTH)
    p_stdscr.clear()  # first cleaning
    p_stdscr.keypad(True)
    p_stdscr.nodelay(True)  # non-blocking input
    rectangle(p_stdscr, MARGIN + TOP_PADDING, MARGIN + LEFT_PADDING, MARGIN + TOP_PADDING
              + HEIGHT, MARGIN + LEFT_PADDING + WIDTH)

def set_pairs(fg, bg):
    curses.init_pair(1, fg, colors['black'])
    curses.init_pair(2, fg, colors['yellow'])
    curses.init_pair(3, fg, colors['white'])
    curses.init_pair(4, fg, colors['red'])
    curses.init_pair(5, colors['black'], bg)
    curses.init_pair(6, colors['yellow'], bg)
    curses.init_pair(7, colors['white'], bg)
    curses.init_pair(8, colors['red'], bg)
    curses.init_pair(9, colors['red'], 0)
    curses.init_pair(10, colors['green'], colors['green'])

def main(p_stdscr):
    scr_configuration(p_stdscr)
    snake = Snake()
    rabbit = Rabbit()
    game = Game(p_stdscr, snake, rabbit)
    game.run()


curses.wrapper(main)
