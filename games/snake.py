import copy

from games import GameController as gc


class Segment(gc.MovableGameObject):
    def __init__(self, in_surface, x, y, in_size, color, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, color, game_drawer=game_drawer)
        self.last_position = self.position

    def set_position(self, in_position):
        self.last_position = copy.deepcopy(self.position)
        if in_position[0] > self.controller.board.shape[0]:
            in_position[0] = 0
        if in_position[1] > self.controller.board.shape[1]:
            in_position[1] = 0
        super().set_position(in_position)


class Snake(gc.Hero):
    def __init__(self, in_surface, x, y, in_size: int, color: str, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, color=color, game_drawer=game_drawer)
        self.segments = []
        self.segments.append(Segment(in_surface, x, y, in_size, color=color, game_drawer=game_drawer))

    def tick(self):
        super().tick()
        self.eat_cookie()
        self.move()
        print("running")

    def move(self):
        for i in range(len(self.segments)):
            if i == 0:
                if self.check_direction(self.current_direction):
                    self.set_position([a + b for a, b in zip(self.position, self.current_direction.value)])
            else:
                self.segments[i].set_position(self.segments[i - 1].last_position)

    def get_possible_directions(self):
        possible_directions = super().get_possible_directions()
        possible_directions.remove(gc.Direction.STOP)
        return possible_directions

    def draw(self):
        for segment in self.segments:
            segment.draw()

    def eat_cookie(self):
        eaten = self.controller.delete_cookie(self.position)
        if eaten == 1:
            self.score[0] += 1
            new_segment = Segment(self.controller, 0, 0, self.size, color=self.color, game_drawer=self.game_drawer)
            new_segment.position = copy.deepcopy(self.segments[-1].position)
            self.segments.append(new_segment)


class SnakeController(gc.GameController):
    def new_hero(self, x, y, color: str):
        return Snake(self, x, y, gc.NORMAL_SIZE, color=color, game_drawer=self.game_drawer)

    def check_collisions(self):
        heads = [snake.segments[0].position for snake in self.game_objects['heroes']]
        for snake in self.game_objects['heroes']:
            for i in range(1, len(snake.segments)):
                for head in heads:
                    if snake.segments[i].position:
                        heads.remove(head)
        heads = list(dict.fromkeys(heads))
        new_heroes = []
        for snake in self.game_objects['heroes']:
            if snake.segments[0] in heads:
                new_heroes.append(snake)
        self.game_objects['heroes'] = new_heroes


if __name__ == "__main__":
    game_renderer = SnakeController('snake')
    game_renderer.tick()
