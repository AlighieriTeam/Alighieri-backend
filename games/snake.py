import copy

from games import GameController as gc


class Segment(gc.MovableGameObject):
    def __init__(self, in_surface, x, y, in_size, color, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, color, game_drawer=game_drawer)
        self.last_position = copy.deepcopy(self.position)

    def set_position(self, in_position):
        self.last_position = copy.deepcopy(self.position)
        super().set_position(in_position)


class Snake(gc.Hero):
    def __init__(self, in_surface, x, y, in_size: int, color: str, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, color=color, game_drawer=game_drawer)
        self.segments = []
        self.segments.append(Segment(in_surface, x, y, in_size, color=color, game_drawer=game_drawer))

    def tick(self):
        super().tick()
        self.eat_cookie()
        print("running")

    def move(self):
        if not self.check_direction(self.current_direction):
            return
        self.position = [a + b for a, b in zip(self.segments[0].position, self.current_direction.value)]
        self.segments[0].set_position(self.position)
        for i in range(1, len(self.segments)):
            self.segments[i].set_position(self.segments[i - 1].last_position)

    def get_possible_directions(self):
        possible_directions = super().get_possible_directions()
        possible_directions.remove(gc.Direction.STOP)
        direction = gc.Direction.STOP
        match self.current_direction:
            case gc.Direction.LEFT: direction = gc.Direction.RIGHT
            case gc.Direction.RIGHT: direction = gc.Direction.LEFT
            case gc.Direction.UP: direction = gc.Direction.DOWN
            case gc.Direction.DOWN:  direction = gc.Direction.UP
        if direction in possible_directions:
            possible_directions.remove(direction)
        return possible_directions

    def draw(self):
        for segment in self.segments:
            segment.draw()

    def undraw(self):
        for segment in self.segments:
            segment.undraw()

    def eat_cookie(self):
        eaten = self.controller.delete_cookie(self.segments[0].position)
        if eaten == 1:
            self.score[0] += 1
            self.add_segment()

    def add_segment(self):
        x = self.segments[-1].last_position[0]
        y = self.segments[-1].last_position[1]
        new_segment = Segment(self.controller, x, y, self.size, color=self.color+'-light', game_drawer=self.game_drawer)
        self.segments.append(new_segment)


class SnakeController(gc.GameController):
    def __init__(self, name, game_drawer, generateRandomMap):
        super().__init__(name, game_drawer, generateRandomMap)
        self.init_game()

    def new_hero(self, x, y, color: str):
        return Snake(self, x, y, gc.NORMAL_SIZE, color=color, game_drawer=self.game_drawer)

    def check_collisions(self):
        heads = [snake for snake in self.game_objects['heroes']]
        for snake in self.game_objects['heroes']:
            for tail in snake.segments[1:]:
                for head in heads:
                    if tail.position == head.segments[0].position:
                        heads.remove(head)
                        head.undraw()
            for head in heads:
                if snake != head:
                    if snake.segments[0].position == head.segments[0].position:
                        heads.remove(head)
                        head.undraw()
                        heads.remove(snake)
                        snake.undraw()
        self.game_objects['heroes'] = heads

