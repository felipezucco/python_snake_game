from snake import Snake, Status
from rabbit import Rabbit
from utils import on_press, is_a_valid_controller, choice_direction, move, timer, calculate_shock, calculate_shock_line, new_coord_respawn, \
    get_level_speed, build_ground, is_a_valid_input
import curses
import threading
import asyncio


class Game:
    _stdscr = None
    _snake: Snake = None
    _rabbit: Rabbit = None
    _level: int = 1
    _kill_threads = False

    def __init__(self, p_stdscr):
        self._snake = Snake()
        self._rabbit = Rabbit()
        self._stdscr = p_stdscr

    def run(self):
        self.__start_threads()

    def __start_threads(self):
        # Keyboard listener for inputs
        on_press(lambda e: self.__input_listener(e))
        self.__start_actors()

    def __start_actors(self):
        # Create rabbits thread
        t_rabbit = threading.Thread(target=self.__run_rabbit)
        t_rabbit.start()

        # Create snakes thread
        t_snake = threading.Thread(target=self.__run_snake)
        t_snake.start()

    def __input_listener(self, key):
        snake = self._snake

        if is_a_valid_input(key.name):
            if is_a_valid_controller(key.name) and snake.get_did_last_moviment():
                snake.set_direction(key.name)
                snake.set_did_last_moviment(False)
            elif key.name == "r":
                self.__reset_game()

    def __run_rabbit(self):
        rabbit = self._rabbit
        stdscr = self._stdscr
        snake = self._snake
        xr, yr = rabbit.get_position()

        while True:
            if not rabbit.is_dead():
                build_ground(stdscr, xr, yr)  # remove old rabbit's position

                # Check new position to avoid shock with snake
                with_shock = True
                while with_shock:
                    choose_direction = choice_direction()  # choose a direction
                    xr, yr = move(rabbit.get_position(), choose_direction)
                    with_shock = calculate_shock_line((xr, yr), snake.get_body())

                rabbit.set_position((xr, yr))
                stdscr.addstr(yr, xr, "o", curses.color_pair(9))  #
                stdscr.refresh()
                timer(get_level_speed(False, self._level))
            else:
                timer(3)
                rabbit.respawn(new_coord_respawn())

    def __reset_game(self):
        self._snake.start_snake()
        self._rabbit.start_rabbit()
        self._level = 1

    def __run_snake(self):
        stdscr = self._stdscr
        snake = self._snake

        # Build snake in screen
        for x, y in snake.get_body():
            stdscr.addstr(y, x, "x", curses.color_pair(10))
            stdscr.refresh()

        # Start loop for run snake
        while not self._kill_threads:
            if snake.get_status() == Status.NORMAL:
                xst, yst = snake.get_tail()
                build_ground(stdscr, xst, yst)
                stdscr.refresh()
                snake.remove_tail()
            elif snake.get_status() == Status.GROW_UP:
                snake.set_status(Status.NORMAL)

            xsh, ysh = move(snake.get_head(), snake.get_last_direction())
            snake.get_body().append((xsh, ysh))
            stdscr.addstr(ysh, xsh, "x", curses.color_pair(10))
            stdscr.refresh()
            if self.__snake_shock():
                break

            snake.set_did_last_moviment(True)
            timer(get_level_speed(True, self._level))

    def __snake_shock(self):
        snake = self._snake
        rabbit = self._rabbit
        stdscr = self._stdscr

        if calculate_shock(snake.get_head(), rabbit.get_position()):
            rabbit.kill()
            snake.add_rabbit()
            self._level += 1 if snake.get_rabbits() % 3 == 0 else 0
        elif calculate_shock_line(snake.get_head(), snake.get_body()[0:-2]):
            curses.flash()
            return True

        stdscr.addstr(0, 0, "Kills: {0}".format(snake.get_rabbits()))
        return False

