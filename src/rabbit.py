
class Rabbit:
    _is_dead = False

    _game = None
    _position = (15, 15)

    def __init__(self):
        pass

    def is_dead(self):
        return self._is_dead

    def kill(self):
        self._is_dead = True

    def respawn(self, p_new_position):
        self._position = p_new_position
        self._is_dead = False

    def set_position(self, p_position):
        self._position = p_position

    def get_position(self):
        return self._position
