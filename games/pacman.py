from games import gameBase as Base


class Pacman(Base.Hero):
    def __init__(self, in_surface, x, y, in_size: int, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, game_drawer=game_drawer)

    def tick(self):
        super().tick()
        self.eat_cookie()

    def eat_cookie(self):
        self._score += self._controller.delete_cookie(self.board_position)


class PacmanController(Base.GameController):
    def new_hero(self, x, y):
        return Pacman(self, x, y, Base.UNIFIED_SIZE//3, game_drawer=self._game_drawer)


if __name__ == "__main__":
    game_renderer = PacmanController('pacman')
    game_renderer.tick()
