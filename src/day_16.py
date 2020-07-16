BASE_PATTERN = [0, 1, 0, -1]

def pattern(n):
    while True:
        for x in BASE_PATTERN:
            for i in range(n + 1):
                yield x


def skip_first(generator):
    next(generator)
    while True:
        yield next(generator)


def apply_fft(digits):
    results = []
    for index, digit in enumerate(digits):
        pattern_gen = skip_first(pattern(index))
        s = sum(d * t for d, t in zip(digits, pattern_gen))
        results.append(abs(s) % 10)
    return results


if __name__ == "__main__":
    with open('../input/day_16.in') as f:
        digits = list(map(int, list(f.readline().strip())))

    for i in range(100):
        print(f'Transform {i}')
        digits = apply_fft(digits)

    print(digits[:8])
