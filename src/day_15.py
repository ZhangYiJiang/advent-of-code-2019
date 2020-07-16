from copy import copy
from operator import add, mul, eq, lt
from dataclasses import dataclass
from itertools import permutations
from collections import defaultdict, namedtuple, deque
import os

ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
MODE_SWITCH = 9
EXIT = 99

POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2


NO_PARAM = {EXIT}
ONE_PARAM = {INPUT, OUTPUT, MODE_SWITCH}
TWO_PARAM = {JUMP_IF_TRUE, JUMP_IF_FALSE}
THREE_PARAM = {ADD, MULTIPLY, LESS_THAN, EQUALS}


@dataclass
class Param:
    value: int
    mode: int


class Program:
    def __init__(self, memory, input):
        self.memory = defaultdict(lambda: 0, enumerate(memory))
        self.position = 0
        self.relative_base = 0
        self.input = input


    def _read_memory(self):
        result = self.memory[self.position]
        self.position += 1
        return result


    def consume(self):
        raw_op = self._read_memory()

        op = raw_op % 100
        if op in THREE_PARAM:
            param_count = 3
        elif op in TWO_PARAM:
            param_count = 2
        elif op in ONE_PARAM:
            param_count = 1
        elif op in NO_PARAM:
            param_count = 0
        else:
            raise Exception(f'Do not know how many params for {op}')
        
        values = [self._read_memory() for _ in range(param_count)]
        modes = reversed(list(map(int, str(raw_op // 100).zfill(param_count))))

        params = [Param(param, mode) for (param, mode) in zip(values, modes)]
        return (op, params)


    def read(self, param):
        if param.mode == IMMEDIATE_MODE:
            return param.value
        if param.mode == POSITION_MODE:
            return self.memory[param.value]
        if param.mode == RELATIVE_MODE:
            return self.memory[self.relative_base + param.value]
        raise Exception(f'Do not know how to read {param}')
    

    def write(self, param, value):
        if param.mode == POSITION_MODE:
            self.memory[param.value] = value
        elif param.mode == RELATIVE_MODE:
            self.memory[self.relative_base + param.value] = value
        else:
            raise Exception(f'Do not know how to write to {param}')


    def execute(self):
        op, params = self.consume()
        while op != EXIT:
            if op == ADD or op == MULTIPLY or op == LESS_THAN or op == EQUALS:
                r1, r2, out = params
                if op == ADD:
                    ex = add
                elif op == MULTIPLY:
                    ex = mul
                elif op == LESS_THAN:
                    ex = lt
                elif op == EQUALS:
                    ex = eq
                else:
                    raise Exception(f'Cannot find operator for {op}')
                v1, v2 = map(self.read, [r1, r2])
                self.write(out, int(ex(v1, v2)))

            elif op == JUMP_IF_FALSE or op == JUMP_IF_TRUE:
                v, jmp = params
                value = self.read(v)
                if op == JUMP_IF_FALSE:
                    should_jump = value == 0
                elif op == JUMP_IF_TRUE:
                    should_jump = value != 0
                
                if should_jump:
                    self.position = self.read(jmp)
            
            elif op == MODE_SWITCH:
                self.relative_base += self.read(params[0])

            elif op == INPUT:
                self.write(params[0], next(self.input))

            elif op == OUTPUT:
                value = self.read(params[0])
                yield value
            
            else:
                raise Exception(f'Invalid ops code {op}, position {self.position}')

            op, params = self.consume()


def parse_program(input_str):
    return list(map(int, input_str.split(',')))


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
DELTA = {
    NORTH: ( 1, 0),
    SOUTH: (-1, 0),
    EAST:  (0,  1),
    WEST:  (0, -1),
}
# All directions 90 degrees from each other
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

BLOCKED = 0
MOVED = 1
FOUND_OXYGEN = 2

UNKNOWN = '?'
WALL = '█'
FLOOR = ' '
SELF = 'X'
OXYGEN = 'O'
START = 'S'


Frontier = namedtuple('Frontier', ['frontier', 'moves', 'visited'])
Neighbor = namedtuple('Neighbor', ['direction', 'coords'])


def print_screen(screen, location):
    xs = list(map(lambda p: p[0], screen.keys()))
    ys = list(map(lambda p: p[1], screen.keys()))

    output = []
    for y in range(min(ys), max(ys) + 1):
        row = []
        for x in range(min(xs), max(xs) + 1):
            coords = (x, y)
            if coords == (0, 0):
                row.append(START)
            elif coords == location:
                row.append(SELF)
            else:
                row.append(screen[coords])
        output.append(''.join(row))
    print('\n'.join(output))


def get_opposite(direction):
    return DIRECTIONS[(DIRECTIONS.index(direction) - 2) % 4]


def get_neighbours(coords):
    x, y = coords
    return [Neighbor(direction, (x + dx, y + dy)) for direction, (dx, dy) in DELTA.items()]


def enqueue(coords, moves, visited):
    frontiers = []
    for direction, next_coords in get_neighbours(coords):
        if next_coords not in visited:
            new_visited = set(visited)
            new_visited.add(next_coords)
            frontiers.append(
                Frontier(next_coords, moves + (direction,), new_visited)
            )
    return frontiers


def find_nearest(screen, coords, target):
    movements = deque(enqueue(coords, (), ()))
    
    while movements:
        coords, moves, visited = movements.popleft()
        tile = screen[coords]

        if tile == target:
            return moves
        
        elif tile == FLOOR or tile == OXYGEN:
            movements.extend(enqueue(coords, moves, visited))

    return None


def flood_oxygen(screen):
    time = 0
    oxygen_tiles = set(coords for coords, tile in screen.items() if tile == OXYGEN)
    floor_tiles = set(coords for coords, tile in screen.items() if tile == FLOOR)

    while floor_tiles:
        time += 1
        new_oxygen = set()
        for coords in oxygen_tiles:
            for _, neighbour in get_neighbours(coords):
                if neighbour in floor_tiles:
                    new_oxygen.add(neighbour)
                    floor_tiles.remove(neighbour)
                    screen[neighbour] = OXYGEN

        oxygen_tiles |= new_oxygen
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print_screen(screen, location)
        print('Time:', time)

    return time

if __name__ == "__main__":
    with open('../input/day_15.in') as f:
        memory = parse_program(f.readline())

    screen = defaultdict(lambda: UNKNOWN)

    # State
    last_input = None
    location = (0, 0)
    turns = 0
    screen[location] = FLOOR

    def input_generator():
        global turns
        global last_input

        while turns < 1_000_000:
            turns += 1

            # Try to probe an unknown location
            moves = find_nearest(screen, location, UNKNOWN)
            print(f'Moves: {moves}')
            if not moves:
                to_oxygen = find_nearest(screen, (0, 0), OXYGEN)
                
                print('Path:', len(to_oxygen))
                print('Flood time:', flood_oxygen(screen))
                return
            
            for move in moves:
                last_input = move
                yield move

    p = Program(memory, input_generator())
    for result in p.execute():
        x, y = location
        dx, dy = DELTA[last_input]
        next_location = (x + dx, y + dy)

        if result == BLOCKED:
            screen[next_location] = WALL
        else:
            location = next_location
            if result == FOUND_OXYGEN:
                screen[next_location] = OXYGEN
            else:
                screen[next_location] = FLOOR
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print_screen(screen, location)
