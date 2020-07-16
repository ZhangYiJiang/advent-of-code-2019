from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class Move:
    direction: str
    distance: int


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError


def moves_to_cartesian(moves):
    last_position = Point(0, 0)
    positions = [last_position]

    for move in moves:
        x, y = last_position

        if move.direction == 'U':
            y += move.distance
        if move.direction == 'D':
            y -= move.distance
        if move.direction == 'R':
            x += move.distance
        if move.direction == 'L':
            x -= move.distance
        
        last_position = Point(x, y)
        positions.append(last_position)

    return positions


def get_line_components(line):
    for i in range(len(line) - 1):
        yield line[i], line[i+1]


def minmax(a, b):
    return min(a, b), max(a, b)


def find_intersections(line_a, line_b):
    intersections = []

    for (start_a, end_a) in get_line_components(line_a):
        dx_a, dy_a = end_a - start_a
        for (start_b, end_b) in get_line_components(line_b):
            if dx_a == 0: # a is vertical
                left, right = minmax(start_b.x, end_b.x)
                if left < start_a.x < right:
                    intersections.append(Point(start_a.x, start_b.y))
            else:
                bottom, top = minmax(start_b.y, end_b.y)
                if bottom < start_a.y < top:
                    intersections.append(Point(start_b.x, start_a.y))
    
    return intersections


def parse_lines(line):
    moves = line.split(',')
    return moves_to_cartesian(map(lambda m: Move(m[0], int(m[1:])), moves))


def parse_moves(line):
    moves = line.split(',')
    return list(map(lambda m: Move(m[0], int(m[1:])), moves))


def draw(board, moves, id):
    position = (0, 0)
    distance = 0

    def draw_at(x, y):
        if board[(x, y)] != '0' and board[(x, y)] != id:
            board[(x, y)] = 'x'
        else:
            board[(x, y)] = id
    
    for move in moves:
        x, y = position
        if move.direction == 'R':
            for nx in range(x + 1, x + move.distance + 1):
                draw_at(nx, y)
            x += move.distance
        if move.direction == 'L':
            for nx in range(x - 1, x - move.distance - 1, -1):
                draw_at(nx, y)
            x -= move.distance
        if move.direction == 'U':
            for ny in range(y + 1, y + move.distance + 1):
                draw_at(x, ny)
            y += move.distance
        if move.direction == 'D':
            for ny in range(y - 1, y - move.distance - 1, -1):
                draw_at(x, ny)
            y -= move.distance
        position = (x, y)


def find_board_intersection(board):
    intersections = []
    for key, value in board.items():
        if value == 'x':
            intersections.append(key)
    return intersections


if __name__ == "__main__":
    with open('../input/day_3.in') as f:
        line_1, line_2 = map(parse_moves, f.readlines())
    
    board = defaultdict(lambda: '0')
    draw(board, line_1, '1')
    draw(board, line_2, '2')
    intersections = find_board_intersection(board)

    print(list(sorted(intersections, key=lambda p: abs(p[0]) + abs(p[1])))[:5])
