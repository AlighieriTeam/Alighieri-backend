import gameBase as Base


class Pacman(Base.Hero):
    def __init__(self, in_surface, x, y, in_size: int):
        super().__init__(in_surface, x, y, in_size)

    def tick(self):
        super().tick()
        self.eat_cookie()

    def eat_cookie(self):
        self._score += self._renderer.delete_cookie(self.board_position)


class PacmanRenderer(Base.GameRenderer):
    def new_hero(self):
        return Pacman(self, Base.UNIFIED_SIZE, Base.UNIFIED_SIZE, Base.UNIFIED_SIZE//3)


if __name__ == "__main__":
    game_renderer = PacmanRenderer('pacman')
    game_renderer.tick()
