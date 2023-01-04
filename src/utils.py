from random import choice, randint
from time import sleep
from default_configurations import FIELD_LEFT, FIELD_RIGHT, FIELD_BOTTOM, FIELD_TOP, AUXILIARIES, OPOSITES_DIRECTIONS, CONTROLLERS, VALID_INPUTS, GROUND, MARGIN
from default_configurations import SCREEN_WIDTH, SCREEN_TOP, LEVEL_SNAKE_SPEED, LEVEL_RABBIT_SPEED, SNAKES_START_LENGTH
import curses


# Increment/decrement coordinate to move character accordingly set a direction
def move(p_origin, p_direction) -> tuple:
    x, y = p_origin[0], p_origin[1]

    if p_direction == "left":
        x = x - 1 if x > FIELD_LEFT else FIELD_RIGHT
    elif p_direction == "right":
        x = x + 1 if x < FIELD_RIGHT else FIELD_LEFT
    elif p_direction == "up":
        y = y - 1 if y > FIELD_TOP else FIELD_BOTTOM
    elif p_direction == "down":
        y = y + 1 if y < FIELD_BOTTOM else FIELD_TOP

    return x, y


def calculate_shock(p_character, p_target) -> bool:
    xc, yc = p_character
    xt, yt = p_target
    return (xc, yc) == (xt, yt)


def calculate_shock_line(p_character, p_target: []) -> bool:
    for xy in p_target:
        if calculate_shock(p_character, xy):
            return True
    return False


def choice_direction():
    return choice(CONTROLLERS)


def timer(p_seconds: float):
    sleep(p_seconds)


def is_a_valid_input(p_input) -> bool:
    return p_input in VALID_INPUTS


def is_a_valid_controller(p_input) -> bool:
    return p_input in CONTROLLERS


def new_coord_respawn() -> tuple:
    x = randint(FIELD_LEFT, FIELD_RIGHT)
    y = randint(FIELD_TOP, FIELD_BOTTOM)
    return x, y


def get_level_speed(snake: bool, p_level: int) -> float:
    speed = LEVEL_SNAKE_SPEED if snake else LEVEL_RABBIT_SPEED
    return speed[p_level] if p_level <= 4 else speed[4]


def build_ground(p_stdscr, i, j):
    p_stdscr.addstr(j, i, " ", curses.color_pair(13))
