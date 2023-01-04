GROUND = " "
CONTROLLERS = ("right", "left", "up", "down")
AUXILIARIES = "space", "r",
OPOSITES_DIRECTIONS = {"right": "left", "left": "right", "up": "down", "down": "up"}
SNAKES_START_LENGTH = 10
VALID_INPUTS = CONTROLLERS + AUXILIARIES
HEIGHT = 30
WIDTH = 80
TOP_PADDING = 1
LEFT_PADDING = 1
MARGIN = 2
SCREEN_TOP = HEIGHT + TOP_PADDING + MARGIN * 2 + 2
SCREEN_WIDTH = WIDTH + LEFT_PADDING + MARGIN * 2 + 2
FIELD_TOP = MARGIN + TOP_PADDING + 1
FIELD_LEFT = MARGIN + LEFT_PADDING + 1
FIELD_RIGHT = MARGIN + LEFT_PADDING + WIDTH - 1
FIELD_BOTTOM = MARGIN + TOP_PADDING + HEIGHT - 1
STROKE_TOP = MARGIN + TOP_PADDING
STROKE_LEFT = MARGIN + LEFT_PADDING
STROKE_BOTTOM = MARGIN + TOP_PADDING + HEIGHT
STROKE_RIGHT = MARGIN + LEFT_PADDING + WIDTH

##
LEVEL_SNAKE_SPEED = {1: .2, 2: .1, 3: .05, 4: .04}
LEVEL_RABBIT_SPEED = {1: .7, 2: .5, 3: .3, 4: .1 }