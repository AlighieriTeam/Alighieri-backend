import random
import time

from games import MapElements as me

class MapGenerator():
    def __init__(self):
        self.__width = 15
        self.__height = 29
        self.__board = [[me.MapElements.WALL.value for _ in range(self.__width)] for _ in range(self.__height)]
        self.__total_tiles = self.__width * self.__height // 5

    def __roll_new_start(self):
        self.__board = [[me.MapElements.WALL.value for _ in range(self.__width)] for _ in range(self.__height)]
        while True:
            xx = random.randint(1, self.__width - 2)
            yy = random.randint(1, self.__height - 2)
            if self.__board[yy][xx] == me.MapElements.WALL.value:
                self.__board[yy][xx] = me.MapElements.PATH.value
                self.__total_tiles -= 1
                return yy, xx


    def __clear_tile(self, xx, yy, direction):
        global board
        if self.__board[yy][xx] == me.MapElements.WALL.value:
            self.__total_tiles -= 1
            self.__board[yy][xx] = me.MapElements.PATH.value
            match direction:
                case 1:
                    self.__board[yy][xx+1] = me.MapElements.PATH.value
                case 2:
                    self.__board[yy][xx-1] = me.MapElements.PATH.value
                case 3:
                    self.__board[yy+1][xx] = me.MapElements.PATH.value
                case 4:
                    self.__board[yy-1][xx] = me.MapElements.PATH.value

    def __add_ghosts(self):
        ghosts_to_generate = 2
        while True:
            x = random.randint(1, self.__width - 2)
            y = random.randint(1, self.__height - 2)
            if self.__board[y][x] == me.MapElements.PATH.value:
                ghosts_to_generate -= 1
                self.__board[y][x] = me.MapElements.GHOST.value
                if ghosts_to_generate == 0: break

    def save_map_to_file(self):
        # TODO: repair infinite loop
        y, x = self.__roll_new_start()
        while self.__total_tiles > 0:
            possibilities = [x for x in range(1, 5)]
            while possibilities:
                next_tile = random.choice(possibilities)
                possibilities.remove(next_tile)
                match next_tile:
                    case 1:
                        if x >= 3:
                            x -= 2
                            self.__clear_tile(x, y, 1)
                            break
                    case 2:
                        if x + 4 <= self.__width:
                            x += 2
                            self.__clear_tile(x, y, 2)
                            break
                    case 3:
                        if y >= 3:
                            y -= 2
                            self.__clear_tile(x, y, 3)
                            break
                    case 4:
                        if y + 4 <= self.__height:
                            y += 2
                            self.__clear_tile(x, y, 4)
                            break
                if not possibilities:
                    y, x = self.__roll_new_start()

        f = open("games/map-random.txt", "w")
        for row in self.__board:
            f.write(' '.join(row))
            f.write('\n')
        f.close()
