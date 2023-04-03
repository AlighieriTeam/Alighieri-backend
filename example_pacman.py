import random

import numpy as np
import pygame
from enum import Enum
from pygame.locals import *


class GameObject:
    def __init__(self, in_surface, x, y, in_size: int, in_color=(255, 0, 0), is_circle: bool = False):
        self._renderer: GameRenderer = in_surface
        self._surface = in_surface._screen
        self._color = in_color
        self.board_position = translate_screen_to_board([x, y])
        self.screen_position = [x, y]
        self._size = in_size
        self._circle = is_circle

    def draw(self):
        if self._circle:
            pygame.draw.circle(self._surface, self._color,
                               self.screen_position, self._size)
        else:
            pygame.draw.rect(self._surface, self._color,
                             pygame.Rect(self.screen_position[0], self.screen_position[1], self._size, self._size), border_radius=3)

    def tick(self):
        pass

    def set_position(self, in_position):
        temp = board[self.board_position[0], self.board_position[1]]
        board[self.board_position[0], self.board_position[1]] = MapElements.PATH.value
        self.board_position = in_position
        self.screen_position = translate_board_to_screen(in_position)
        board[self.board_position[0], self.board_position[1]] = temp


class Wall(GameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(0, 0, 255)):
        super().__init__(in_surface, x, y, in_size, in_color)


class Cookie(GameObject):
    def __init__(self, in_surface, x, y):
        super().__init__(in_surface, x, y, 4, (255, 255, 0), True)


class Direction(Enum):
    STOP = [0, 0]
    UP = [0, -1]
    RIGHT = [1, 0]
    DOWN = [0, 1]
    LEFT = [-1, 0]


class MovableGameObject(GameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(255, 0, 0), is_circle: bool = False):
        super().__init__(in_surface, x, y, in_size, in_color, is_circle)
        self.current_direction = Direction.STOP
        self.last_direction = Direction.STOP

    def set_direction(self, new_direction):
        self.last_direction = self.current_direction
        self.current_direction = new_direction

    # TODO: co jeżeli bot chce wejść w ścianę?
    def move(self):
        if self.check_direction(self.current_direction):
            self.set_position([a + b for a, b in zip(self.board_position, self.current_direction.value)])

    def check_direction(self, direction):
        new_position = [a + b for a, b in zip(self.board_position, direction.value)]
        if new_position[0] < 0 or new_position[0] > board.shape[0]:
            return False
        if new_position[1] < 1 or new_position[1] > board.shape[1]:
            return False
        return board[new_position[0], new_position[1]] != MapElements.WALL.value

    def get_possible_directions(self):
        possible_directions = []
        for direction in list(Direction):
            if self.check_direction(direction):
                possible_directions.append(direction)
        return possible_directions


class Ghost(MovableGameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(255, 0, 0)):
        super().__init__(in_surface, x, y, in_size, in_color, False)

    def tick(self):
        if bool(random.getrandbits(1)):
            possibilities = self.get_possible_directions()
            if possibilities:
                self.set_direction(random.choice(possibilities))
        self.move()


class Hero(MovableGameObject):
    def __init__(self, in_surface, x, y, in_size: int):
        super().__init__(in_surface, x, y, in_size, (255, 255, 0), False)
        self._renderer = in_surface
        self._score = 0
        self._score_display = pygame.font.Font(None, 32)

    def tick(self):
        self.move()
        self.eat_cookie()
        # TODO: zgiń jeżeli duch

    def draw(self):
        super().draw()
        score_text = self._score_display.render(f'{self._score}', True, (255, 255, 255))
        self._renderer._screen.blit(score_text, (10, 10))

    # TODO nie usuwa ciastek? dalej się pojawiają
    def eat_cookie(self):
        print(self.board_position)
        if board[self.board_position[0], self.board_position[1]] == MapElements.COOKIE.value:
            self._score += 1
            board[self.board_position[0], self.board_position[1]] = MapElements.PATH.value
            self._renderer.delete_object(self.board_position)


class GameRenderer:
    def __init__(self, width: int, height: int):
        pygame.init()
        pygame.font.init()
        self._width = width
        self._height = height
        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Pacman')
        self._finished = False
        self._game_objects = []
        self._ghosts = []
        self._hero: Hero = None

    def tick(self):
        while not self._finished:
            self._screen.fill((0, 0, 0))
            for game_object in self._game_objects:
                game_object.tick()
                game_object.draw()

            pygame.display.flip()
            self._handle_events()
        print("Game over")

    def add_game_object(self, obj: GameObject):
        self._game_objects.append(obj)

    def delete_object(self, position):
        self._game_objects = [obj for obj in self._game_objects if obj.board_position != position or isinstance(obj, MovableGameObject)]

    def add_ghost(self, obj: Ghost):
        self._game_objects.append(obj)
        self._ghosts.append(obj)

    def add_hero(self, in_hero):
        self.add_game_object(in_hero)
        self._hero = in_hero

    def _handle_events(self):
        while True :
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self._done = True
            elif event.type == KEYUP:
                if event.key == K_UP:
                    self._hero.set_direction(Direction.UP)
                    return
                elif event.key == K_LEFT:
                    self._hero.set_direction(Direction.LEFT)
                    return
                elif event.key == K_DOWN:
                    self._hero.set_direction(Direction.DOWN)
                    return
                elif event.key == K_RIGHT:
                    self._hero.set_direction(Direction.RIGHT)
                    return
            pygame.event.clear()


class MapElements(Enum):
    WALL = '#'
    PATH = ' '
    BLOCK = '@'
    GHOST = '^'
    HERO = '*'
    COOKIE = '.'


def import_map(name, width):
    board = np.zeros((1, width))
    with open('map-' + name + '.txt') as file:
        map_elements = [element.value for element in list(MapElements)]
        for line in file:
            board_line = []
            for mark in line:
                if mark in map_elements:
                    board_line.append(mark)
            board = np.append(board, [board_line], axis=0)
    board = np.delete(board, 0, axis=0)
    return board


def translate_screen_to_board(in_coords, in_size=32):
    return [int(in_coords[0] // in_size), int(in_coords[1] // in_size)]


def translate_board_to_screen(in_coords, in_size=32):
    return [in_coords[0] * in_size, in_coords[1] * in_size]


if __name__ == "__main__":
    unified_size = 32
    board = import_map('pacman', 10)
    size = board.shape
    game_renderer = GameRenderer(size[0] * unified_size, size[1] * unified_size)

    for x, row in enumerate(board):
        for y, mark in enumerate(row):
            translated = translate_board_to_screen((x, y))
            match mark:
                case MapElements.WALL.value:
                    wall = Wall(game_renderer, translated[0], translated[1], unified_size)
                    game_renderer.add_game_object(wall)
                case MapElements.PATH.value:
                    cookie = Cookie(game_renderer, translated[0] + unified_size // 2, translated[1] + unified_size // 2)
                    game_renderer.add_game_object(cookie)
                    board[x, y] = MapElements.COOKIE.value
                case MapElements.GHOST.value:
                    ghost = Ghost(game_renderer, translated[0], translated[1], unified_size)
                    game_renderer.add_ghost(ghost)
                case MapElements.HERO.value:
                    pacman = Hero(game_renderer, unified_size, unified_size, unified_size)
                    game_renderer.add_hero(pacman)
                case _:
                    pass
    game_renderer.tick()
