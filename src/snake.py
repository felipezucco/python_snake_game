from utils import CONTROLLERS, OPOSITES_DIRECTIONS


class Status:
    NORMAL = 0
    GROW_UP = 1


class Snake:
    _body = []
    _rabbits = 0
    _status: int = Status.NORMAL
    _last_direction = "right"

    def __init__(self):
        self._body = [(11, 10), (12, 10), (13, 10)]

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
