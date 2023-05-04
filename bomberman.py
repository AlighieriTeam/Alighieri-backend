import gameBase as Base


class Block(Base.GameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(0, 0, 125)):
        super().__init__(in_surface, x, y, in_size, in_color)


class Bomb(Base.GameObject):
    def __init__(self, in_surface, x, y):
        super().__init__(in_surface, x, y, 4, (255, 255, 0))
        self.timer = 3

    def tick(self):
        self.timer -= 1
        if self.timer == 0:
            self.boom()

    def boom(self):
        pass


class Bomber(Base.Hero):

    def __init__(self, in_surface, x, y, in_size: int):
        super().__init__(in_surface, x, y, in_size)

    def tick(self):
        super().tick()

    def plant_bomb(self):
        pass


if __name__ == "__main__":
    unified_size = 32
    game_renderer = Base.GameController('bomberman')
    game_renderer.tick()
