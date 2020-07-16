from collections import defaultdict, deque


def bfs(tree):
    distances = {}
    queue = deque([
        ('COM', ())
    ])
    visited = set()

    while len(queue) > 0:
        current, parents = queue.pop()
        visited.add(current)
        distances[current] = parents

        for child in tree[current]:
            if child not in visited:
                queue.append((child, (*parents, current)))

    return distances


def remove_common_ancestor(left, right):
    while left and right and left[0] == right[0]:
        left = left[1:]
        right = right[1:]
    return left, right


if __name__ == "__main__":
    orbits = defaultdict(list)
    with open('../input/day_6.in') as f:
        for line in f.readlines():
            if not line:
                continue
            
            parent, child = line.strip().split(')')
            orbits[parent].append(child)

    distances = bfs(orbits)
    print(sum([len(parents) for parents in distances.values()]))

    left, right = remove_common_ancestor(distances['SAN'], distances['YOU'])
    print(len(left) + len(right))
