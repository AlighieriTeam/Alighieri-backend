import random
import time

import numpy as np
from enum import Enum

STANDARD_SIZE = 1
NORMAL_SIZE = 0.9
SMALL_SIZE = 0.4


class GameObject:
    def __init__(self, in_renderer, x, y, in_size, in_color=(255, 0, 0), is_circle: bool = False, game_drawer=None):
        self._game_drawer = game_drawer
        self._controller: GameController = in_renderer
        self._color = in_color
        self._position = [x, y]
        self._size = in_size
        self._circle = is_circle

    def draw(self):
        if self._circle:
            self._game_drawer.draw_circle(self._position[0] + STANDARD_SIZE / 2, self._position[1] + STANDARD_SIZE / 2,
                                          self._color, self._size / 2)
        else:
            self._game_drawer.draw_rectangle(self._position[0] + STANDARD_SIZE / 2, self._position[1] + STANDARD_SIZE / 2,
                                             self._color, self._size, self._size)

    def undraw(self):
        self._game_drawer.draw_rectangle(self._position[0] + STANDARD_SIZE / 2, self._position[1] + STANDARD_SIZE / 2,
                                         'black', STANDARD_SIZE, STANDARD_SIZE)

    def tick(self):
        pass

    def set_position(self, in_position):
        temp = self._controller._board[self._position[0], self._position[1]]
        self._controller._board[self._position[0], self._position[1]] = MapElements.PATH.value
        self._position = in_position
        self._controller._board[self._position[0], self._position[1]] = temp


class Wall(GameObject):
    def __init__(self, in_surface, x, y, in_size, in_color='blue', game_drawer=None):
        super().__init__(in_surface, x, y, in_size, in_color, game_drawer=game_drawer)


class Cookie(GameObject):
    def __init__(self, in_surface, x, y, game_drawer=None):
        super().__init__(in_surface, x, y, SMALL_SIZE, 'white', game_drawer=game_drawer)


class Direction(Enum):
    STOP = [0, 0]
    UP = [0, -1]
    RIGHT = [1, 0]
    DOWN = [0, 1]
    LEFT = [-1, 0]


class MovableGameObject(GameObject):
    def __init__(self, in_surface, x, y, in_size, in_color, is_circle: bool = True, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, in_color, is_circle, game_drawer=game_drawer)
        self.current_direction = Direction.STOP
        self.last_direction = Direction.STOP

    def set_direction(self, new_direction):
        self.last_direction = self.current_direction
        self.current_direction = new_direction

    def move(self):
        if self.check_direction(self.current_direction):
            self.set_position([a + b for a, b in zip(self._position, self.current_direction.value)])

    def check_direction(self, direction):
        new_position = [a + b for a, b in zip(self._position, direction.value)]
        if new_position[0] < 0 or new_position[0] > self._controller._board.shape[0]:
            return False
        if new_position[1] < 1 or new_position[1] > self._controller._board.shape[1]:
            return False
        check = self._controller._board[new_position[0], new_position[1]]
        return check != MapElements.WALL.value and check != MapElements.BLOCK.value

    def get_possible_directions(self):
        possible_directions = []
        for direction in list(Direction):
            if self.check_direction(direction):
                possible_directions.append(direction)
        return possible_directions


class Ghost(MovableGameObject):
    def __init__(self, in_surface, x, y, in_size, in_color='red', game_drawer=None):
        super().__init__(in_surface, x, y, in_size, in_color, game_drawer=game_drawer)

    def tick(self):
        if bool(random.getrandbits(1)):
            possibilities = self.get_possible_directions()
            if possibilities:
                self.set_direction(random.choice(possibilities))
        self.move()


class Hero(MovableGameObject):
    def __init__(self, in_surface, x, y, in_size, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, 'yellow', game_drawer=game_drawer)
        self._score = 0
        self.bot = Bot()

    def tick(self):
        self.set_direction(self.bot.get_action(GameState(self.get_possible_directions())))
        self.move()


class GameState:
    def __init__(self, possibilities):
        self.possibilities = possibilities


class Bot:
    def get_action(self, gameState: GameState):
        if gameState.possibilities:
            return random.choice(gameState.possibilities)
        return Direction.STOP


class GameController:
    def __init__(self, name, game_drawer):
        self._game_drawer = game_drawer
        self._game_objects = {}
        self._board = self.import_map(name)
        self._finished = False
        self._game_updater = None
        self._players = None

    def set_updater(self, game_updater):
        self._game_updater = game_updater

    def set_players(self, players: list):
        self._players = players

    def import_map(self, name):
        file = open('games/map-' + name + '.txt')
        start = file.tell()
        width = len(file.readline())
        board = np.zeros((1, width-1))
        file.seek(start)

        map_elements = [element.value for element in list(MapElements)]
        walls = []
        cookies = []
        ghosts = []
        heroes = []

        for x, line in enumerate(file):
            board_line = []
            for y, mark in enumerate(line):
                if mark in map_elements:
                    match mark:
                        case MapElements.WALL.value:
                            wall = Wall(self, x, y, NORMAL_SIZE, game_drawer=self._game_drawer)
                            walls.append(wall)
                        case MapElements.PATH.value:
                            cookie = Cookie(self, x, y, game_drawer=self._game_drawer)
                            cookies.append(cookie)
                            mark = MapElements.COOKIE.value
                        case MapElements.GHOST.value:
                            ghost = Ghost(self, x, y, NORMAL_SIZE, game_drawer=self._game_drawer)
                            ghosts.append(ghost)
                        case MapElements.HERO.value:
                            heroes.append(self.new_hero(x, y))
                        case _:
                            pass
                    board_line.append(mark)
            board = np.append(board, [board_line], axis=0)
        board = np.delete(board, 0, axis=0)
        self._game_objects = {
            'walls': walls,
            'cookies': cookies,
            'ghosts': ghosts,
            'heroes': heroes
        }
        return board

    def new_hero(self, x, y):
        return Hero(self, x, y, NORMAL_SIZE)

    def tick(self):
        self._game_drawer.clear_all()
        while not self._finished:
            self._render_all_objects()
            self._update_scores()
            self._handle_events()
            self.check_collisions()
            self.is_over()
            time.sleep(0.25)   # TODO only for developing
            self._finished = True  # to test popup
        print("Game over")

        self._game_updater.show_popup(self._players)
        time.sleep(0.25)  # little delay to give a chance for signal delivery to every player in room before room will be deleted

    def _update_scores(self):
        for i, hero in enumerate(self._game_objects['heroes']):
            # TODO displaying under screen
            self._game_drawer.draw_text(i, 0, hero._score)

    def _render_all_objects(self):
        for key, values in self._game_objects.items():
            if isinstance(values, list):
                for value in values:
                    value.undraw()
                    value.tick()
                    value.draw()
            else:
                values.undraw()
                values.tick()
                values.draw()

    def _handle_events(self):
        pass

    def delete_cookie(self, board_position):
        cookies = [c for c in self._game_objects['cookies'] if c._position != board_position]
        if len(cookies) != len(self._game_objects['cookies']):
            self._game_objects['cookies'] = cookies
            return 1
        return 0

    def check_collisions(self):
        ghosts_positions = [g._position for g in self._game_objects['ghosts']]
        heroes = [h for h in self._game_objects['heroes'] if h._position not in ghosts_positions]
        self._game_objects['heroes'] = heroes

    def is_over(self):
        if not self._game_objects['heroes'] or not self._game_objects['cookies']:
            self._finished = True

    def stop_game(self):
        self._finished = True

    # TODO send to js
    def get_map_shape(self):
        return self._board.shape

class MapElements(Enum):
    WALL = '#'
    PATH = ' '
    BLOCK = '@'
    GHOST = '^'
    HERO = '*'
    COOKIE = '.'


if __name__ == "__main__":
    game_controller = GameController('pacman')
    game_controller.tick()
