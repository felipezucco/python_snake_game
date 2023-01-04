from utils import CONTROLLERS, OPOSITES_DIRECTIONS, SNAKES_START_LENGTH, FIELD_TOP


class Status:
    NORMAL = 0
    GROW_UP = 1


# Class for build Snakes properties and method.
# All the logical programming is in the Game class.
class Snake:
    _body = []
    _rabbits = 0
    _status: int = Status.NORMAL
    _last_direction = "right"
    _did_last_moviment = True

    def __init__(self):
        self.start_snake()

    def start_snake(self):
        self._body = [(i, FIELD_TOP) for i in range(FIELD_TOP, FIELD_TOP + SNAKES_START_LENGTH)]
        self._last_direction = "right"
        self._did_last_moviment = True
        self._status = Status.NORMAL
        self._rabbits = 0

    def get_head(self):
        return self._body[-1]

    def get_tail(self):
        return self._body[0]

    def get_body(self):
        return self._body

    def remove_tail(self):
        del self.get_body()[0]

    def add_rabbit(self):
        self._rabbits += 1
        self._status = Status.GROW_UP

    def set_status(self, p_status: int):
        self._status = p_status

    def get_status(self):
        return self._status

    def get_rabbits(self):
        return self._rabbits

    def get_last_direction(self):
        return self._last_direction

    def set_direction(self, p_direction):
        if p_direction in CONTROLLERS \
                and p_direction != self._last_direction \
                and self._last_direction != OPOSITES_DIRECTIONS[p_direction]:
            self._last_direction = p_direction

    def set_did_last_moviment(self, p_param: bool):
        self._did_last_moviment = p_param

    def get_did_last_moviment(self):
        return self._did_last_moviment