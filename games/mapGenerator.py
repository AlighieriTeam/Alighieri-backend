import random

from games import MapElements as me

width = 8
height = 15
board = array = [[me.MapElements.WALL.value for _ in range(width)] for _ in range(height)]
total_tiles = width * height // 6


def roll_new_start():
    while True:
        x = random.randint(1, height - 2)
        y = random.randint(1, width - 2)
        global board
        if board[x][y] == me.MapElements.WALL.value:
            board[x][y] = me.MapElements.PATH.value
            global total_tiles
            total_tiles -= 1
            return x, y


def clear_tile(direction, xx, yy):
    global board
    if board[xx][yy] == me.MapElements.WALL.value:
        global total_tiles
        total_tiles -= 1
        board[xx][yy] = me.MapElements.PATH.value
        match direction:
            case 1:
                board[xx][yy+1] = me.MapElements.PATH.value
            case 2:
                board[xx][yy-1] = me.MapElements.PATH.value
            case 3:
                board[xx+1][yy] = me.MapElements.PATH.value
            case 4:
                board[xx-1][yy] = me.MapElements.PATH.value


x, y = roll_new_start()
while total_tiles > 0:
    possibilities = [x for x in range(4)]
    while possibilities:
        next_tile = random.choice(possibilities)
        possibilities.remove(next_tile)
        match next_tile:
            case 1:
                if y >= 3:
                    y -= 2
                    clear_tile(x, y, 1)
                    break
            case 2:
                if y + 4 <= height:
                    y += 2
                    clear_tile(x, y, 2)
                    break
            case 3:
                if x >= 3:
                    x -= 2
                    clear_tile(x, y, 3)
                    break
            case 4:
                if x + 4 <= width:
                    x += 2
                    clear_tile(x, y, 4)
                    break
        if not possibilities:
            x, y = roll_new_start()






for row in array:
    print(' '.join(row))
