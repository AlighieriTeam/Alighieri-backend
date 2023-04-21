import random

import numpy as np
import pygame
from enum import Enum
import bot

UNIFIED_SIZE = 32


class GameObject:
    def __init__(self, in_renderer, x, y, in_size: int, in_color=(255, 0, 0), is_circle: bool = False):
        self._renderer: GameRenderer = in_renderer
        self._color = in_color
        self.board_position = translate_screen_to_board([x, y])
        self.screen_position = [x, y]
        self._size = in_size
        self._circle = is_circle

    def draw(self):
        if self._circle:
            pygame.draw.circle(self._renderer._screen, self._color, (self.screen_position[0] + UNIFIED_SIZE/2, self.screen_position[1] + UNIFIED_SIZE/2), self._size)
        else:
            pygame.draw.rect(self._renderer._screen, self._color,
                             pygame.Rect(self.screen_position[0], self.screen_position[1], self._size, self._size), border_radius=3)

    def tick(self):
        pass

    def set_position(self, in_position):
        temp = self._renderer._board[self.board_position[0], self.board_position[1]]
        self._renderer._board[self.board_position[0], self.board_position[1]] = MapElements.PATH.value
        self.board_position = in_position
        self.screen_position = translate_board_to_screen(in_position)
        self._renderer._board[self.board_position[0], self.board_position[1]] = temp


class Wall(GameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(0, 0, 255)):
        super().__init__(in_surface, x, y, in_size, in_color)


class Cookie(GameObject):
    def __init__(self, in_surface, x, y):
        super().__init__(in_surface, x, y, 4, (255, 255, 0))


class Direction(Enum):
    STOP = [0, 0]
    UP = [0, -1]
    RIGHT = [1, 0]
    DOWN = [0, 1]
    LEFT = [-1, 0]


class MovableGameObject(GameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(255, 0, 0), is_circle: bool = True):
        super().__init__(in_surface, x, y, in_size, in_color, is_circle)
        self.current_direction = Direction.STOP
        self.last_direction = Direction.STOP

    def set_direction(self, new_direction):
        self.last_direction = self.current_direction
        self.current_direction = new_direction

    def move(self):
        if self.check_direction(self.current_direction):
            self.set_position([a + b for a, b in zip(self.board_position, self.current_direction.value)])

    def check_direction(self, direction):
        new_position = [a + b for a, b in zip(self.board_position, direction.value)]
        if new_position[0] < 0 or new_position[0] > self._renderer._board.shape[0]:
            return False
        if new_position[1] < 1 or new_position[1] > self._renderer._board.shape[1]:
            return False
        check = self._renderer._board[new_position[0], new_position[1]]
        return check != MapElements.WALL.value and check != MapElements.BLOCK.value

    def get_possible_directions(self):
        possible_directions = []
        for direction in list(Direction):
            if self.check_direction(direction):
                possible_directions.append(direction)
        return possible_directions


class Ghost(MovableGameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(255, 0, 0)):
        super().__init__(in_surface, x, y, in_size, in_color)

    def tick(self):
        if bool(random.getrandbits(1)):
            possibilities = self.get_possible_directions()
            if possibilities:
                self.set_direction(random.choice(possibilities))
        self.move()


class Hero(MovableGameObject):
    def __init__(self, in_surface, x, y, in_size: int):
        super().__init__(in_surface, x, y, in_size, (255, 255, 0))
        self._score_display = pygame.font.Font(None, 32)
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


class GameRenderer:
    def __init__(self, name):
        pygame.init()
        pygame.font.init()
        self._game_objects = {}
        self._board = self.import_map(name)
        shape = self._board.shape
        self._width = shape[0] * UNIFIED_SIZE
        self._height = shape[1] * UNIFIED_SIZE
        self._screen = pygame.display.set_mode((self._width, self._height))
        #self._score_display = pygame.font.Font(None, 32)
        pygame.display.set_caption(name)
        self._finished = False

    def import_map(self, name):
        file = open('map-' + name + '.txt')
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
                    translated = translate_board_to_screen((x, y))
                    match mark:
                        case MapElements.WALL.value:
                            wall = Wall(self, translated[0], translated[1], UNIFIED_SIZE)
                            walls.append(wall)
                        case MapElements.PATH.value:
                            cookie = Cookie(self, translated[0] + UNIFIED_SIZE // 2, translated[1] + UNIFIED_SIZE // 2)
                            cookies.append(cookie)
                            mark = MapElements.COOKIE.value
                        case MapElements.GHOST.value:
                            ghost = Ghost(self, translated[0] + UNIFIED_SIZE // 2, translated[1] + UNIFIED_SIZE // 2, UNIFIED_SIZE // 3)
                            ghosts.append(ghost)
                        case MapElements.HERO.value:
                            heroes.append(self.new_hero(translated[0] + UNIFIED_SIZE // 2, translated[1] + UNIFIED_SIZE // 2))
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
        return Hero(self, x, y, UNIFIED_SIZE//3)

    def tick(self):
        while not self._finished:
            self._render_all_objects()
            self._update_scores()
            self._handle_events()
            self.check_collisions()
            self.is_over()
        print("Game over")

    def _update_scores(self):
        for i, hero in enumerate(self._game_objects['heroes']):
            print(hero._score)

    def _render_all_objects(self):
        self._screen.fill((0, 0, 0))
        for key, values in self._game_objects.items():
            if isinstance(values, list):
                for value in values:
                    value.tick()
                    value.draw()
            else:
                values.tick()
                values.draw()
        pygame.display.flip()

    def _handle_events(self):
        while True:
            event = pygame.event.wait(1000)
            if event.type == pygame.NOEVENT:
                return
            if event.type == pygame.QUIT:
                self._done = True
            pygame.event.clear()

    def delete_cookie(self, board_position):
        cookies = [c for c in self._game_objects['cookies'] if c.board_position != board_position]
        if len(cookies) != len(self._game_objects['cookies']):
            self._game_objects['cookies'] = cookies
            return 1
        return 0

    def check_collisions(self):
        ghosts_positions = [g.board_position for g in self._game_objects['ghosts']]
        heroes = [h for h in self._game_objects['heroes'] if h.board_position not in ghosts_positions]
        self._game_objects['heroes'] = heroes

    def is_over(self):
        if not self._game_objects['heroes'] or not self._game_objects['cookies']:
            self._finished = True


class MapElements(Enum):
    WALL = '#'
    PATH = ' '
    BLOCK = '@'
    GHOST = '^'
    HERO = '*'
    COOKIE = '.'


def translate_screen_to_board(in_coords):
    return [int(in_coords[0] // UNIFIED_SIZE), int(in_coords[1] // UNIFIED_SIZE)]


def translate_board_to_screen(in_coords):
    return [in_coords[0] * UNIFIED_SIZE, in_coords[1] * UNIFIED_SIZE]


if __name__ == "__main__":
    game_renderer = GameRenderer('pacman')
    game_renderer.tick()
