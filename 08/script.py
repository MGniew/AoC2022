from functools import reduce

    
def is_forest_edge(
    new_x, new_y,
    step_x, step_y,
    x_size, y_size,
):
    if step_x == 1:
        return new_x < x_size - 1
    if step_x == -1:
        return new_x > 0
    if step_y == 1:
        return new_y < y_size - 1
    if step_y == -1:
        return new_y > 0


def calculate_direction_score(data, x, y, step_x, step_y):

    x_size = len(data)
    y_size = len(data[0])

    tree_size = data[x][y]
    new_x = x
    new_y = y
    while is_forest_edge(new_x, new_y, step_x, step_y, x_size, y_size):
        new_x += step_x
        new_y += step_y
        if data[new_x][new_y] >= tree_size:
            break

    if step_x:
        return abs(x - new_x)
    return abs(y - new_y)


def is_tree_visible_from_direction(data, x, y, step_x, step_y):

    x_size = len(data)
    y_size = len(data[0])

    tree_size = data[x][y]
    new_x = x
    new_y = y
    while is_forest_edge(new_x, new_y, step_x, step_y, x_size, y_size):
        new_x += step_x
        new_y += step_y
        if data[new_x][new_y] >= tree_size:
            return False
    return True


def generate_tree_score(data, x, y):
    scores = [
        calculate_direction_score(
            data, x, y, step_x=step_x, step_y=step_y
        )
        for step_x, step_y in [(0, -1), (0, 1), (-1, 0), (1, 0)]
    ]
    return reduce(lambda a, b: a * b, scores)


def is_tree_visible(data, x, y):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for tree_vis in (
        is_tree_visible_from_direction(data, x, y, step_x, step_y)
        for step_x, step_y in directions
    ):
        if tree_vis:
            return True
    return False


def map_forest(data, tree_function):
    x_size = len(data)
    y_size = len(data[0])
    result = []
    for x in range(x_size):
        row = list()
        for y in range(y_size):
            row.append(tree_function(data, x, y))
        result.append(row)
    return result


with open("input.txt") as f:
    data = f.read().splitlines()
data = [[int(a) for a in list(d)] for d in data]

visibility_mask = map_forest(data, is_tree_visible)
result = sum([t for row in visibility_mask for t in row])
print("Star 1:", result)

score_grid = map_forest(data, generate_tree_score)
result = max([t for row in score_grid for t in row])
print("Star 2:", result)
