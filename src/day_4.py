def pairs(lst):
    for i in range(len(lst) - 1):
        yield lst[i], lst[i+1]


def check_number_part_1(n):
    digits = list(map(int, str(n)))

    has_pair = False
    for first, second in pairs(digits):
        # Digits never decrease
        if second < first:
            return False
        if first == second:
            has_pair = True
    
    return has_pair


def check_number_part_2(n):
    digits = list(map(int, str(n)))

    # Group consecutive digits
    groups = []
    current = [digits[0]]
    for digit in digits[1:]:
        if digit == current[-1]:
            current.append(digit)
        else:
            groups.append(current)
            current = [digit]
    groups.append(current)

    if not any(len(group) == 2 for group in groups):
        return False
    for first, second in pairs(groups):
        if second[0] < first[0]:
            return False
    return True


def count(start, end, fn):
    return list(map(fn, range(start, end))).count(True)

if __name__ == "__main__":
    start, end = 387638, 919123

    print(count(start, end, check_number_part_1))
    print(count(start, end, check_number_part_2))
