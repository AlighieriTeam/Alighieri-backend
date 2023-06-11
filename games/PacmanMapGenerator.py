import random

from games import MapElements as me
from games.MapGenerator import MapGenerator

class PacmanMapGenerator(MapGenerator):
    def __init__(self, width: int = 8, height: int = 15, pacman_no: int = 4, ghost_no: int = 4):
        super().__init__(width=width, height=height)
        self._pacman_no = pacman_no
        self._ghost_no = ghost_no

    def _add_ghosts(self):
        ghosts_to_generate = self._ghost_no
        while True:
            x = random.randint(1, self._width - 2)
            y = random.randint(1, self._height - 2)
            if self._board[y][x] == me.MapElements.PATH.value:
                ghosts_to_generate -= 1
                self._board[y][x] = me.MapElements.GHOST.value
                if ghosts_to_generate == 0: break

    def _add_pacmans(self):
        pacmans_to_generate = self._pacman_no
        while True:
            x = random.randint(1, self._width - 2)
            y = random.randint(1, self._height - 2)
            if self._board[y][x] == me.MapElements.PATH.value:
                pacmans_to_generate -= 1
                self._board[y][x] = me.MapElements.HERO.value
                if pacmans_to_generate == 0: break

    def generate_map(self):
        super().generate_paths()
        self._add_ghosts()
        self._add_pacmans()
        super().save_map_to_file()
