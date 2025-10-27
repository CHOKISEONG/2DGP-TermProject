from enum import Enum

# 게임의 6방향을 나타내는 용도 (0은 방향x, 오른쪽 = 1 부터 반시계 방향)
class DIRECTION(Enum):
    NONE = 0
    RIGHT = 1
    UP_RIGHT = 2
    UP_LEFT = 3
    LEFT = 4
    DOWN_LEFT = 5
    DOWN_RIGHT = 6

# 타일의 타입을 나타내는 용도
class Tile(Enum):
    EMPTY = 0
    UP_LEFT = 1
    UP_RIGHT = 2
    DOWN_LEFT = 3
    DOWN_RIGHT = 4
    LEFT = 5
    RIGHT = 6
    FALL = 7

def tile_to_direction(tile):
    if tile == Tile.UP_LEFT:
        return DIRECTION.UP_LEFT
    elif tile == Tile.UP_RIGHT:
        return DIRECTION.UP_RIGHT
    elif tile == Tile.DOWN_LEFT:
        return DIRECTION.DOWN_LEFT
    elif tile == Tile.DOWN_RIGHT:
        return DIRECTION.DOWN_RIGHT
    elif tile == Tile.LEFT:
        return DIRECTION.LEFT
    elif tile == Tile.RIGHT:
        return DIRECTION.RIGHT
    else:
        return DIRECTION.NONE