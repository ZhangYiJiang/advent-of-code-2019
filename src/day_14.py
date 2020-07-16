import math
from collections import defaultdict
from pprint import pprint


def parse_recipe(line):
    reactents, results = line.strip().split(' => ')
    ingredients = []
    for reactent in reactents.split(', '):
        count, ingredient = reactent.split(' ')
        ingredients.append((ingredient, int(count)))
    
    count, result = results.split(' ')
    return result, int(count), ingredients


def calculate_ore(tree, fuel_required):
    prereqs = defaultdict(set)
    for result, value in tree.items():
        ingredients, count = value
        for ingredient, count in ingredients:
            prereqs[ingredient].add(result)
    
    stack = {'FUEL'}
    counts = defaultdict(lambda: 0, (('FUEL', fuel_required),))

    while stack != {'ORE'}:
        next_item = stack.pop()
        prereqs.pop(next_item, None)

        required_count = counts.pop(next_item)
        ingredients, count = tree[next_item]
        ratio = math.ceil(required_count / count)
        # ratio = required_count / count
        for ingredient, count in ingredients:
            counts[ingredient] += count * ratio
        
        for key, prereq in prereqs.items():
            prereq.discard(next_item)
            if not prereq:
                stack.add(key)

    return counts['ORE']


if __name__ == "__main__":
    tree = defaultdict(list)
    with open('../input/day_14.in') as f:
        for line in f.readlines():
            result, count, ingredients = parse_recipe(line)
            tree[result] = ingredients, count
    
    fuel = 1
    ore_required = calculate_ore(tree, fuel)
    print(ore_required)

    # Obtained from using // and / in the ratio line above
    lo = 3817376
    hi = 4366186

    # Binary search for the correct fuel requirement
    target = 1000000000000
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        mid_ore = calculate_ore(tree, mid)

        if mid_ore < target:
            lo = mid
        else:
            hi = mid
    
    print(hi)
    print(calculate_ore(tree, hi + 1))
    print(calculate_ore(tree, hi))