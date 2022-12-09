class Vector():

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def normalize_elements(self):
        x, y = self.x, self.y
        if x != 0:
            x /= abs(x)
        if y != 0:
            y /= abs(y)
        return Vector(x, y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def copy(self):
        return Vector(self.x, self.y)

    def length(self):
        return (self.x**2 + self.y**2)**(1/2)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"



def get_tail_direction(head, tail):
    diff = head - tail
    if round(diff.length()) < 2:
        return Vector(0, 0)
    return diff.normalize_elements()


def solve_rope(rope, steps):
    tail_visited = set([Vector(0, 0)])
    for step in steps:
        directions = {
            "U": Vector(0, 1),
            "D": Vector(0, -1),
            "L": Vector(-1, 0),
            "R": Vector(1, 0),
        }
        direction = directions[step[0]]
        distance = step[1]

        while distance > 0:
            rope[0] += direction
            distance -= 1

            for knot_a in range(len(rope) - 1):
                knot_b = knot_a + 1
                t_dir = get_tail_direction(
                    rope[knot_a],
                    rope[knot_b],
                )
                if t_dir.length() == 0:
                    break
                rope[knot_b] += t_dir
            tail_visited.add(rope[-1].copy())

    return len(tail_visited)


def load_data(filename):
    with open(filename) as f:
        steps = f.read().splitlines()
        steps = [row.split() for row in steps]
        steps = [(r[0], int(r[1])) for r in steps]
    return steps


steps = load_data("input.txt")

rope = [Vector(0, 0) for i in range(2)]
print("Star 1:", solve_rope(rope, steps))

rope = [Vector(0, 0) for i in range(10)]
print("Star 2:", solve_rope(rope, steps))
