from games import GameController as Base


class Pacman(Base.Hero):
    def __init__(self, in_surface, x, y, in_size: int, color: str,  game_drawer=None):
        super().__init__(in_surface, x, y, in_size, color=color, game_drawer=game_drawer)

    def tick(self):
        super().tick()
        self.eat_cookie()
        print("running")

    def eat_cookie(self):
        self.score[0] += self.controller.delete_cookie(self.position)


class PacmanController(Base.GameController):
    def new_hero(self, x, y, color: str):
        return Pacman(self, x, y, Base.NORMAL_SIZE, color=color, game_drawer=self.game_drawer)


if __name__ == "__main__":
    game_renderer = PacmanController('pacman')
    game_renderer.tick()
