from snake import Snake, Status
from rabbit import Rabbit
from keyboard import on_press
from utils import is_a_valid_controller, choice_direction, move, timer, calculate_shock, calculate_shock_line, new_coord_respawn, \
    get_level_speed, build_ground, is_a_valid_input
import curses
import threading


class Game:
    _stdscr = None
    _snake: Snake = None
    _rabbit: Rabbit = None
    _level: int = 1

    def __init__(self, p_stdscr):
        self._snake = Snake()
        self._rabbit = Rabbit()
        self._stdscr = p_stdscr


    # Game's start
    def run(self):
        self.__start_threads()


    # Create and initialize snake's and rabbit's thread
    # Also create a Window's keyboard listener to
    # detect input keys to control the snake's direction
    def __start_threads(self):
        # Keyboard listener for inputs
        on_press(lambda e: self.__input_listener(e))
        self.__start_characters()


    # Create and starts snakes and rabbit thread
    # Both characters are running in separated threads
    def __start_characters(self):
        # Create and starts rabbits thread
        t_rabbit = threading.Thread(target=self.__run_rabbit)
        t_rabbit.start()

        # Create and starts snakes thread
        t_snake = threading.Thread(target=self.__run_snake)
        t_snake.start()


    # Get input key
    # Check if it is a valid and controller input key
    # * Was necessary to set a bool variable for snake direction controlling
    # * to detect if the snakes did the last movement
    def __input_listener(self, p_key):
        snake = self._snake

        if is_a_valid_input(p_key.name):
            if is_a_valid_controller(p_key.name) and snake.get_did_last_moviment():
                snake.set_direction(p_key.name)
                snake.set_did_last_moviment(False)


    # Method to execute rabbit's logical movement
    def __run_rabbit(self):
        rabbit = self._rabbit
        stdscr = self._stdscr
        snake = self._snake

        # Get rabbits first position
        # set in its class
        xr, yr = rabbit.get_position()

        # Initiate loop for execute rabbit's movement
        while True:
            # Check if rabbit is dead
            # If so set a delay to its respawn
            if not rabbit.is_dead():
                # Remove old rabbit's position
                build_ground(stdscr, xr, yr)

                # Check new position to avoid shock with snake
                # If it detects a shock with snake's body
                # it is calculated a new coordinate for rabbit's movement
                did_it_shocked = True
                while did_it_shocked:
                    choose_direction = choice_direction()
                    xr, yr = move(rabbit.get_position(), choose_direction)
                    did_it_shocked = calculate_shock_line((xr, yr), snake.get_body())

                # After get new coordinates
                # it is set on rabbit's position
                # and rendered on the user's screen
                rabbit.set_position((xr, yr))
                stdscr.addstr(yr, xr, "o", curses.color_pair(9))
                stdscr.refresh()
                timer(get_level_speed(False, self._level))
            else:
                timer(3)
                rabbit.respawn(new_coord_respawn())


    # Method to execute snake's movement
    # * It is not totally efficient because the input key listener
    # * and the snake's runner threads are being executed separately.
    # * So in the game's early levels the controller could be delayed
    def __run_snake(self):
        stdscr = self._stdscr
        snake = self._snake

        # Build snake in screen at starting
        for x, y in snake.get_body():
            stdscr.addstr(y, x, "x", curses.color_pair(10))
            stdscr.refresh()

        # Start loop for run snake
        while True:
            # Check at first if the snake's condition status
            # is normal (just sliding) or if it is growing up after catching a rabbit
            if snake.get_status() == Status.NORMAL:
                # To create a sensation of movement,
                # it is taking the first array position value (tail)
                # and remove it
                # also rendered a ground in the tail's last position
                xst, yst = snake.get_tail()
                build_ground(stdscr, xst, yst)
                stdscr.refresh()
                snake.remove_tail()

            elif snake.get_status() == Status.GROW_UP:
                snake.set_status(Status.NORMAL)

            # After removing, or not, snakes tail
            # is necessary to replace its head accordingly last direction value
            xsh, ysh = move(snake.get_head(), snake.get_last_direction())
            snake.get_body().append((xsh, ysh))
            stdscr.addstr(ysh, xsh, "x", curses.color_pair(10))
            stdscr.refresh()

            # After all is checked, if the new heads position
            # shocks with snakes or rabbit bodies,
            # If shocked by its own body,
            # the snake dies and the thread is stopped
            if self.__snake_shock():
                break

            # To conclude, it is set that snakes did its last movement
            # to release another direction input key
            snake.set_did_last_moviment(True)
            # This timer controlling the game's difficult level
            timer(get_level_speed(True, self._level))


    # This method checks possibles snakes shocks
    def __snake_shock(self):
        snake = self._snake
        rabbit = self._rabbit
        stdscr = self._stdscr

        # Check if snakes head hit the rabbit
        # if so, the rabbit is killed,
        # is added one more rabbit to the counter
        # and increases the game's level by 1
        if calculate_shock(snake.get_head(), rabbit.get_position()):
            rabbit.kill()
            snake.add_rabbit()
            self._level += 1 if snake.get_rabbits() % 3 == 0 else 0

        # If snakes head hit its body,
        # the game is over
        elif calculate_shock_line(snake.get_head(), snake.get_body()[0:-2]):
            curses.flash()
            return True

        stdscr.addstr(0, 0, "Kills: {0}".format(snake.get_rabbits()))
        return False

