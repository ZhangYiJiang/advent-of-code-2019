from copy import copy
from operator import add, mul, eq, lt
from dataclasses import dataclass
from itertools import permutations
from collections import defaultdict

ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
EXIT = 99

POSITION_MODE = 0
IMMEDIATE_MODE = 1


NO_PARAM = {EXIT}
ONE_PARAM = {INPUT, OUTPUT}
TWO_PARAM = {JUMP_IF_TRUE, JUMP_IF_FALSE}
THREE_PARAM = {ADD, MULTIPLY, LESS_THAN, EQUALS}


@dataclass
class Param:
    value: int
    mode: int


class Program:
    def __init__(self, memory, input):
        self.memory = copy(memory)
        self.position = 0
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
        raise Exception(f'Do not know how to interprete mode {param.mode}')
    

    def write(self, param, value):
        if param.mode == IMMEDIATE_MODE:
            raise Exception(f'Tried to write to {param}')
        self.memory[param.value] = value


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


def execute_part_1(memory):
    results = []
    for phases in permutations([0, 1, 2, 3, 4]):
        current = 0
        def set_input(new_value):
            nonlocal current
            current = new_value

        for phase in phases:
            program = Program(memory, generate_input(phase, current), set_input)
            program.execute()

        results.append((current, phases))

    print(max(results))


if __name__ == "__main__":
    with open('../input/day_7.in') as f:
        memory = parse_program(f.readline())
    
    results = (0, ())

    for phases in permutations([5, 6, 7, 8, 9]):
        amps = []
        queued_output = [0]
        def input_generator(index, phase):
            yield phase
            while True:
                if index == 0:
                    yield queued_output.pop()
                else:
                    yield next(amps[index - 1])

        for i, phase in enumerate(phases):
            p = Program(memory, input_generator(i, phase))
            amps.append(p.execute())

        for output in amps[4]:
            queued_output.append(output)
        results = max(results, (output, phases))
    print(results)
