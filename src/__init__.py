import curses
from game import Game
from default_configurations import HEIGHT, WIDTH, TOP_PADDING, LEFT_PADDING, MARGIN, SCREEN_TOP, SCREEN_WIDTH, STROKE_TOP, STROKE_LEFT, STROKE_BOTTOM, STROKE_RIGHT, \
    FIELD_RIGHT, FIELD_BOTTOM, FIELD_TOP, FIELD_LEFT


stdscr = curses.initscr()

colors = {'white': curses.COLOR_WHITE, 'red': curses.COLOR_RED, 'green': curses.COLOR_GREEN,
          'yellow': curses.COLOR_YELLOW, 'blue': curses.COLOR_BLUE, 'magenta': curses.COLOR_MAGENTA,
          'cyan': curses.COLOR_CYAN, 'black': curses.COLOR_BLACK}

def scr_configuration(p_stdscr):
    curses.start_color()
    curses.use_default_colors()
    set_pairs()
    curses.cbreak()  # avoid close window after input
    curses.curs_set(0)  # hide cursor
    curses.resize_term(SCREEN_TOP, SCREEN_WIDTH)
    p_stdscr.clear()  # first cleaning
    p_stdscr.keypad(True)
    p_stdscr.nodelay(True)  # non-blocking input
    build_strokes(p_stdscr)
    fill_grid(p_stdscr)


def build_strokes(p_stdscr):
    # Top/Bottom Strokes
    for i in range(STROKE_LEFT, STROKE_RIGHT + 1):
        p_stdscr.addstr(STROKE_TOP, i, "x", curses.color_pair(12))
        p_stdscr.addstr(STROKE_BOTTOM, i, "x", curses.color_pair(12))

    # Left/Right Strokes
    for i in range(STROKE_TOP, STROKE_BOTTOM + 1):
        p_stdscr.addstr(i, STROKE_LEFT, "x", curses.color_pair(12))
        p_stdscr.addstr(i, STROKE_RIGHT, "x", curses.color_pair(12))


def fill_grid(p_stdscr):
    for i in range(FIELD_LEFT, FIELD_RIGHT + 1):
        for j in range(FIELD_TOP, FIELD_BOTTOM + 1):
            p_stdscr.addstr(j, i, " ", curses.color_pair(13))


def set_pairs():
    curses.init_pair(9, colors['magenta'], colors['white'])
    curses.init_pair(10, colors['green'], colors['white'])
    curses.init_pair(11, colors['blue'], colors['blue'])
    curses.init_pair(12, colors['yellow'], colors['yellow'])
    curses.init_pair(13, colors['white'], colors['white'])
    curses.init_pair(14, colors['green'], colors['green'])


def main(p_stdscr):
    scr_configuration(p_stdscr)
    game = Game(p_stdscr)
    game.run()


if __name__ == "__main__":
    curses.wrapper(main)
