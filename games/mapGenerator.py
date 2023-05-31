import random

from games import MapElements as me

width = 15
height = 29
board = [[me.MapElements.WALL.value for _ in range(width)] for _ in range(height)]
total_tiles = width * height // 5


def roll_new_start():
    while True:
        xx = random.randint(1, width - 2)
        yy = random.randint(1, height - 2)
        global board
        if board[yy][xx] == me.MapElements.WALL.value:
            board[yy][xx] = me.MapElements.PATH.value
            global total_tiles
            total_tiles -= 1
            return yy, xx


def clear_tile(xx, yy, direction):
    global board
    if board[yy][xx] == me.MapElements.WALL.value:
        global total_tiles
        total_tiles -= 1
        board[yy][xx] = me.MapElements.PATH.value
        match direction:
            case 1:
                board[yy][xx+1] = me.MapElements.PATH.value
            case 2:
                board[yy][xx-1] = me.MapElements.PATH.value
            case 3:
                board[yy+1][xx] = me.MapElements.PATH.value
            case 4:
                board[yy-1][xx] = me.MapElements.PATH.value


y, x = roll_new_start()
while total_tiles > 0:
    possibilities = [x for x in range(1, 5)]
    while possibilities:
        next_tile = random.choice(possibilities)
        possibilities.remove(next_tile)
        match next_tile:
            case 1:
                if x >= 3:
                    x -= 2
                    clear_tile(x, y, 1)
                    break
            case 2:
                if x + 4 <= width:
                    x += 2
                    clear_tile(x, y, 2)
                    break
            case 3:
                if y >= 3:
                    y -= 2
                    clear_tile(x, y, 3)
                    break
            case 4:
                if y + 4 <= height:
                    y += 2
                    clear_tile(x, y, 4)
                    break
        if not possibilities:
            y, x = roll_new_start()

f = open("map-random.txt", "w")
for row in board:
    f.write(' '.join(row))
    f.write('\n')
f.close()
