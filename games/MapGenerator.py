import random

from games import MapElements as me

class MapGenerator():
    def __init__(self, width: int = 8, height: int = 15):
        self._width = width
        self._height = height
        self._board = [[me.MapElements.WALL.value for _ in range(self._width)] for _ in range(self._height)]
        self._total_tiles = self._width * self._height // 6

    def _roll_new_start(self):
        self._board = [[me.MapElements.WALL.value for _ in range(self._width)] for _ in range(self._height)]
        while True:
            xx = random.randint(1, self._width - 2)
            yy = random.randint(1, self._height - 2)
            if self._board[yy][xx] == me.MapElements.WALL.value:
                self._board[yy][xx] = me.MapElements.PATH.value
                self._total_tiles -= 1
                return yy, xx


    def _clear_tile(self, xx, yy, direction):
        if self._board[yy][xx] == me.MapElements.WALL.value:
            self._total_tiles -= 1
            self._board[yy][xx] = me.MapElements.PATH.value
            match direction:
                case 1:
                    self._board[yy][xx+1] = me.MapElements.PATH.value
                case 2:
                    self._board[yy][xx-1] = me.MapElements.PATH.value
                case 3:
                    self._board[yy+1][xx] = me.MapElements.PATH.value
                case 4:
                    self._board[yy-1][xx] = me.MapElements.PATH.value

    def generate_paths(self):
        # TODO: repair infinite loop
        y, x = self._roll_new_start()
        while self._total_tiles > 0:
            possibilities = [x for x in range(1, 5)]
            while possibilities:
                next_tile = random.choice(possibilities)
                possibilities.remove(next_tile)
                match next_tile:
                    case 1:
                        if x >= 3:
                            x -= 2
                            self._clear_tile(x, y, 1)
                            break
                    case 2:
                        if x + 4 <= self._width:
                            x += 2
                            self._clear_tile(x, y, 2)
                            break
                    case 3:
                        if y >= 3:
                            y -= 2
                            self._clear_tile(x, y, 3)
                            break
                    case 4:
                        if y + 4 <= self._height:
                            y += 2
                            self._clear_tile(x, y, 4)
                            break
                if not possibilities:
                    y, x = self._roll_new_start()

    def save_map_to_file(self):
        f = open("games/map-random.txt", "w")
        for row in self._board:
            f.write(''.join(row))
            f.write('\n')
        f.close()
        print("map saved")
