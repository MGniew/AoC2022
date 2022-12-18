import copy


def load_data(filename):
    with open(filename) as f:
        data = f.read().splitlines()

    return [tuple(map(int, l.split(','))) for l in data]



def get_no_neigbours(x, y, z, data):
    max_x = len(data) - 1
    max_y = len(data[0]) - 1
    max_z = len(data[0][0]) - 1 
    no_neigbourds = 0
    for dx, dy, dz in [
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    ]:
        if (
            0 <= x + dx <= max_x and 
            0 <= y + dy <= max_y and 
            0 <= z + dz <= max_z
        ):
            no_neigbourds += int(data[x+dx][y+dy][z+dz])
    return no_neigbourds



def solve_1(data):
    max_x = max(c[0] for c in data)
    max_y = max(c[1] for c in data)
    max_z = max(c[2] for c in data)

    grid = [
        [
            [False] * max_z 
            for y in range(max_y)
        ]
        for x in range(max_x)
    ]

    for x, y, z in data:
        grid[x-1][y-1][z-1] = True

    sides = 0
    for x, y, z in data:
        visible_sides = 6 - get_no_neigbours(x-1, y-1, z-1, grid)
        sides += visible_sides

    return sides



def cluster(data):
    max_x = len(data) - 1
    max_y = len(data[0]) - 1
    max_z = len(data[0][0]) - 1
    grid = copy.deepcopy(data)

    points_to_consider = set()
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            for z in range(max_z + 1):
                if grid[x][y][z]:
                    grid[x][y][z] = 0
                else:
                    grid[x][y][z] = -1
                if (
                    x == 0 or y == 0 or z == 0 or 
                    x == max_x or y == max_y or z == max_z
                ): 
                    points_to_consider.add((x, y, z))
                
    class_id = 0
    while points_to_consider:
        class_id += 1
        x, y, z = points_to_consider.pop()
        if grid[x][y][z] != -1:
            continue
        neigbours = set([(x, y, z)])
        while neigbours:
            x, y, z = neigbours.pop()
            grid[x][y][z] = class_id
            for dx, dy, dz in [
                (1, 0, 0), (-1, 0, 0),
                (0, 1, 0), (0, -1, 0),
                (0, 0, 1), (0, 0, -1),
            ]:
                if (
                    0 <= x + dx <= max_x and 
                    0 <= y + dy <= max_y and 
                    0 <= z + dz <= max_z
                ):
                    nx = x + dx
                    ny = y + dy
                    nz = z + dz
                    if grid[nx][ny][nz] == -1:
                        neigbours.add((nx, ny, nz))
                    points_to_consider.discard((nx, ny, nz))

    return grid



def solve_2(data):
    max_x = max(c[0] for c in data)
    max_y = max(c[1] for c in data)
    max_z = max(c[2] for c in data)

    grid = [
        [
            [False] * max_z 
            for y in range(max_y)
        ]
        for x in range(max_x)
    ]
    for x, y, z in data:
        grid[x-1][y-1][z-1] = True

    grid = cluster(grid)
    data = list()
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for z in range(len(grid[0][0])):
                if grid[x][y][z] <= 0:
                    grid[x][y][z] = True
                    data.append((x, y, z))
                else:
                    grid[x][y][z] = False

    sides = 0
    for x, y, z in data:
        visible_sides = 6 - get_no_neigbours(x, y, z, grid)
        sides += visible_sides

    return sides


if __name__ == "__main__":
    data = load_data("example.txt")
    print("Star 1 (example):", solve_1(data))
    print("Star 2 (example):", solve_2(data))

    data = load_data("input.txt")
    print("Star 1 (input):", solve_1(data))
    print("Star 2 (input):", solve_2(data))

