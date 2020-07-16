from copy import copy
from operator import add, mul, eq, lt
from dataclasses import dataclass
from itertools import permutations
from collections import defaultdict
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
        self.memory = defaultdict(int, enumerate(memory))
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
                self.write(out, ex(v1, v2))

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


def get_triple(gen):
    while True:
        try:
            yield next(gen), next(gen), next(gen)
        except StopIteration:
            return


def cmp(a, b):
    return (a > b) - (a < b)


EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

def print_screen(screen):
    xs = list(map(lambda p: p[0], screen.keys()))
    ys = list(map(lambda p: p[1], screen.keys()))

    output = []
    for y in range(min(ys), max(ys) + 1):
        row = []
        for x in range(min(xs), max(xs) + 1):
            tile = screen[(x, y)]
            if tile == WALL:
                row.append('█')
            elif tile == BLOCK:
                row.append('▒')
            elif tile == PADDLE:
                row.append('▁')
            elif tile == BALL:
                row.append('o')
            else:
                row.append(' ')
        output.append(''.join(row))
    print('\n'.join(output))


def find_position(screen, target):
    for coord, tile in screen.items():
        if tile == target:
            return coord


if __name__ == "__main__":
    with open('../input/day_13.in') as f:
        memory = parse_program(f.readline())

    screen = defaultdict(lambda: EMPTY)
    score = 0

    def input_generator():
        while True:
            # Find ball position
            px, py = find_position(screen, PADDLE)
            bx, by = find_position(screen, BALL)

            # os.system('cls' if os.name == 'nt' else 'clear')
            # print_screen(screen)
            # print(f'Score: {score}')
            
            yield int(cmp(bx, px))
    
    # Play the game!
    memory[0] = 2
    
    p = Program(memory, input_generator())
    for x, y, tile in get_triple(p.execute()):
        if x == -1:
            score = tile
        else:
            screen[(x, y)] = tile
    print(score)
