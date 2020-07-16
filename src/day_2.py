from copy import copy


ADD = 1
MULTIPLY = 2
EXIT = 99

def execute(memory, position):
    op, r1, r2, out = memory[position:position+4]
    if op == EXIT:
        return

    v1, v2 = memory[r1], memory[r2]

    if op == ADD:
        memory[out] = v1 + v2
    elif op == MULTIPLY:
        memory[out] = v1 * v2
    else:
        raise Exception(f'Invalid ops code {op}, position {position}')

    execute(memory, position + 4)


def run_program(program, noun, verb):
    memory = copy(program)
    memory[1] = noun
    memory[2] = verb
    execute(memory, 0)
    return memory[0]

if __name__ == "__main__":
    with open('../input/day_2.in') as f:
        program = list(map(int, f.readline().split(',')))

    print(run_program(program, 12, 2))

    for noun in range(0, 100):
        for verb in range(0, 100):
            try:
                result = run_program(program, noun, verb)
                if result == 19690720:
                    print('SUCCESS!', 100 * noun + verb)
            except:
                print(f'{noun}, {verb}: Exception')
                pass
