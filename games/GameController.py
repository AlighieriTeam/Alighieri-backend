import random
import time

import numpy as np
from enum import Enum

from games import MapElements as me
from games.PacmanMapGenerator import PacmanMapGenerator

STANDARD_SIZE = 1
NORMAL_SIZE = 0.9
SMALL_SIZE = 0.4


class Shape(Enum):
    RECTANGLE = 0
    CIRCLE = 1
    GHOST = 2


class GameObject:
    def __init__(self, in_renderer, x, y, in_size, in_color="background", in_shape: Shape = Shape.RECTANGLE, game_drawer=None):
        self.game_drawer = game_drawer
        self.controller: GameController = in_renderer
        self.color = in_color
        self.position = [x, y]
        self.size = in_size
        self.shape = in_shape

    def draw(self):
        match self.shape:
            case Shape.RECTANGLE:
                self.game_drawer.draw_rectangle(self.position[0] + STANDARD_SIZE / 2,
                                                self.position[1] + STANDARD_SIZE / 2,
                                                self.color, self.size, self.size)
            case Shape.CIRCLE:
                self.game_drawer.draw_circle(self.position[0] + STANDARD_SIZE / 2,
                                             self.position[1] + STANDARD_SIZE / 2,
                                             self.color, self.size / 2)
            case Shape.GHOST:
                self.game_drawer.draw_ghost(self.position[0] + STANDARD_SIZE / 2,
                                            self.position[1] + STANDARD_SIZE / 2,
                                            self.color, self.size, self.size)

    def undraw(self):
        self.game_drawer.draw_rectangle(self.position[0] + STANDARD_SIZE / 2, self.position[1] + STANDARD_SIZE / 2,
                                         'background', STANDARD_SIZE, STANDARD_SIZE)

    def tick(self):
        pass

    def set_position(self, in_position):
        temp = self.controller.board[self.position[0], self.position[1]]
        self.controller.board[self.position[0], self.position[1]] = me.MapElements.PATH.value
        self.position = in_position
        self.controller.board[self.position[0], self.position[1]] = temp


class Wall(GameObject):
    def __init__(self, in_surface, x, y, in_size, in_color='wall', game_drawer=None):
        super().__init__(in_surface, x, y, in_size, in_color, game_drawer=game_drawer)


class Cookie(GameObject):
    def __init__(self, in_surface, x, y, game_drawer=None):
        super().__init__(in_surface, x, y, SMALL_SIZE, 'cookie', game_drawer=game_drawer)


class Direction(Enum):
    STOP = [0, 0]
    UP = [0, -1]
    RIGHT = [1, 0]
    DOWN = [0, 1]
    LEFT = [-1, 0]


class MovableGameObject(GameObject):
    def __init__(self, in_surface, x, y, in_size, in_color, in_shape: Shape = Shape.CIRCLE, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, in_color, in_shape, game_drawer=game_drawer)
        self.current_direction = Direction.STOP
        self.last_direction = Direction.STOP

    def set_direction(self, new_direction):
        self.last_direction = self.current_direction
        self.current_direction = new_direction

    def move(self):
        if self.check_direction(self.current_direction):
            self.set_position([a + b for a, b in zip(self.position, self.current_direction.value)])

    def check_direction(self, direction):
        new_position = [a + b for a, b in zip(self.position, direction.value)]
        if new_position[0] < 0 or new_position[0] > self.controller.board.shape[0]:
            return False
        if new_position[1] < 1 or new_position[1] > self.controller.board.shape[1]:
            return False
        check = self.controller.board[new_position[0], new_position[1]]
        return check != me.MapElements.WALL.value and check != me.MapElements.BLOCK.value

    def get_possible_directions(self):
        possible_directions = []
        for direction in list(Direction):
            if self.check_direction(direction):
                possible_directions.append(direction)
        return possible_directions


class Ghost(MovableGameObject):
    def __init__(self, in_surface, x, y, in_size, in_color='ghost', in_shape: Shape = Shape.GHOST, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, in_color, in_shape, game_drawer=game_drawer)

    def tick(self):
        self.set_direction(self.look_for_heroes())
        self.move()

    def look_for_heroes(self):
        direction = Direction.STOP
        possibilities = self.get_possible_directions()
        heroes_positions = [h.position for h in self.controller.game_objects['heroes']]
        while possibilities:
            if self.last_direction in possibilities:
                direction = self.last_direction
            else:
                direction = random.choice(possibilities)
            possibilities.remove(direction)
            if direction == Direction.STOP:
                continue
            sigh = self.position.copy()
            while self.controller.board[sigh[0]][sigh[1]] != me.MapElements.WALL.value:
                if sigh in heroes_positions:
                    return direction
                sigh[0] += direction.value[0]
                sigh[1] += direction.value[1]
        return direction

class Hero(MovableGameObject):
    def __init__(self, in_surface, x, y, in_size, color: str, game_drawer=None):
        super().__init__(in_surface, x, y, in_size, in_color=color, game_drawer=game_drawer)
        self.score = [0]  # to make score mutable
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


class GameController:
    def __init__(self, name, game_drawer, generateRandomMap: bool = False):
        if generateRandomMap:
            PacmanMapGenerator().generate_map()
            name = "random"
        self.game_drawer = game_drawer
        self.game_objects = {}
        self.spawns = []
        self.board = self.import_map(name)
        self.finished = False
        self.game_updater = None
        self.players: list = []

    def set_updater(self, game_updater):
        self.game_updater = game_updater

    # TODO: count points for this players
    def set_players(self, players: list):
        self.players = players
        self.__connect_players_and_heroes()

    def __connect_players_and_heroes(self):
        print(self.spawns)
        for player in self.players:
            random_position = random.choice(self.spawns)
            self.spawns.remove(random_position)
            print(random_position)
            self.game_objects["heroes"].append(self.new_hero(random_position[0], random_position[1], color=str(player["color"][0])))
            #player["hero"] = self.game_objects["heroes"][-1]
            player["points"] = self.game_objects["heroes"][-1].score

    def __set_location(self) -> tuple:
        x, y = 0, 0
        while self.board[x][y] != me.MapElements.COOKIE.value:
            x = random.randint(1, self.board.shape[0] - 1)
            y = random.randint(1, self.board.shape[1] - 1)
        self.board[x][y] = me.MapElements.HERO.value
        return x, y

    def import_map(self, name):
        file = open('games/map-' + name + '.txt')
        start = file.tell()
        width = len(file.readline())
        board = np.zeros((1, width - 1))
        file.seek(start)
        map_elements = [element.value for element in list(me.MapElements)]
        walls = []
        cookies = []
        ghosts = []
        heroes = []

        for x, line in enumerate(file):
            board_line = []
            for y, mark in enumerate(line):
                if mark in map_elements:
                    match mark:
                        case me.MapElements.WALL.value:
                            wall = Wall(self, x, y, NORMAL_SIZE, game_drawer=self.game_drawer)
                            walls.append(wall)
                        case me.MapElements.PATH.value:
                            cookie = Cookie(self, x, y, game_drawer=self.game_drawer)
                            cookies.append(cookie)
                            mark = me.MapElements.COOKIE.value
                        case me.MapElements.GHOST.value:
                            ghost = Ghost(self, x, y, NORMAL_SIZE, game_drawer=self.game_drawer)
                            ghosts.append(ghost)
                        case me.MapElements.HERO.value:
                            self.spawns.append((x, y))
                        case _:
                            pass
                    board_line.append(mark)
            board = np.append(board, [board_line], axis=0)
        board = np.delete(board, 0, axis=0)
        print(board)
        self.game_objects = {
            'walls': walls,
            'cookies': cookies,
            'ghosts': ghosts,
            'heroes': heroes
        }
        return board

    def new_hero(self, x, y, color: str):
        return Hero(self, x, y, NORMAL_SIZE, color=color)

    def tick(self):
        self.game_drawer.clear_all()
        while not self.finished:
            self.render_all_objects()
            self.game_updater.update_scores(self.players)
            self.handle_events()
            self.is_over()
            time.sleep(0.25)  # TODO only for developing
            # self._finished = True  # to test popup
        print("Game over")

        #self.__disconnect_players_and_heroes()
        time.sleep(0.1)  # little delay to give a chance for signal delivery to update scores (left bottom corner in game)
        self.game_updater.show_popup(self.players)
        time.sleep(0.1)  # little delay to give a chance for signal delivery to every player in room before room will be deleted


    def render_all_objects(self):
        for wall in self.game_objects['walls']:
            wall.draw()
        for cookie in self.game_objects['cookies']:
            cookie.draw()

    def handle_events(self):
        for hero in self.game_objects['heroes']:
            hero.undraw()
            hero.tick()
            hero.draw()
        self.check_collisions()
        for ghost in self.game_objects['ghosts']:
            ghost.undraw()
            ghost.tick()
            ghost.draw()
        self.check_collisions()

    def delete_cookie(self, board_position):
        cookies = [c for c in self.game_objects['cookies'] if c.position != board_position]
        if len(cookies) != len(self.game_objects['cookies']):
            self.game_objects['cookies'] = cookies
            return 1
        return 0

    def check_collisions(self):
        ghosts_positions = [g.position for g in self.game_objects['ghosts']]
        heroes = [h for h in self.game_objects['heroes'] if h.position not in ghosts_positions]
        self.game_objects['heroes'] = heroes

    def is_over(self):
        if not self.game_objects['heroes'] or not self.game_objects['cookies']:
            self.finished = True

    def stop_game(self):
        self.finished = True

    # TODO send to js
    def get_map_shape(self):
        return self.board.shape


if __name__ == "__main__":
    game_controller = GameController('pacman')
    game_controller.tick()
