from enum import Enum


class MapElements(Enum):
    WALL = '#'
    PATH = ' '
    BLOCK = '@'
    GHOST = '^'
    HERO = '*'
    COOKIE = '.'
