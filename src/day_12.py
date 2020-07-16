from itertools import combinations


def cmp(a, b):
    return (a > b) - (a < b)


class Moon:
    def __init__(self, x, y, z):
        self.position = (x, y, z)
        self.velocity = (0, 0, 0)
    
    def total_energy(self):
        kinetic = sum(map(abs, self.velocity))
        potential = sum(map(abs, self.position))
        return kinetic * potential

    def apply_gravity(self, other):
        x, y, z = self.position
        x1, y1, z1 = other.position

        dx = cmp(x1, x)
        dy = cmp(y1, y)
        dz = cmp(z1, z)

        vx, vy, vz = self.velocity
        self.velocity = (vx + dx, vy + dy, vz + dz)
    
    def apply_velocity(self):
        x, y, z = self.position
        vx, vy, vz = self.velocity
        self.position = (x + vx, y + vy, z + vz)


if __name__ == "__main__":
    moons = [
        # Moon(x=-1, y=0, z=2),
        # Moon(x=2, y=-10, z=-7),
        # Moon(x=4, y=-8, z=8),
        # Moon(x=3, y=5, z=-1),
        Moon(13, 9, 5),
        Moon(8, 14, -2),
        Moon(-5, 4, 11),
        Moon(2, -6, 1),
    ]

    for i in range(1000):
        for m1, m2 in combinations(moons, 2):
            m1.apply_gravity(m2)
            m2.apply_gravity(m1)

        for m in moons:
            m.apply_velocity()
        
    print(sum(m.total_energy() for m in moons))

