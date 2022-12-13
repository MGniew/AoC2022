import json
import copy
import functools


def read_data(filename):
    with open(filename) as f:
        data = f.read().split("\n\n")
        data = [[json.loads(p) for p in d.strip().split("\n")] for d in data]
    return data


def cmp_list(a, b):
    a = copy.deepcopy(a)
    b = copy.deepcopy(b)

    comparators = {
        (int, int): cmp_int,
        (list, list): cmp_list
    }
    while a and b:
        el_a = a.pop(0)
        el_b = b.pop(0)
        right_order = comparators.get(
            (type(el_a), type(el_b)), cmp_int_list
        )(el_a, el_b)
        if right_order != 0:
            return right_order

    if a and not b:
        return -1
    if b and not a:
        return 1

    return 0


def cmp_int(a, b):
    if a == b:
        return 0
    if a > b:
        return -1
    if a < b:
        return 1


def cmp_int_list(a, b):
    if type(a) == int:
        return cmp_list([a], b)
    return cmp_list(a, [b])


if __name__ == "__main__":
    data = read_data("input.txt")

    result = [(i, cmp_list(*pair)) for i, pair in enumerate(data)]
    print("Star 1:", sum([i+1 for i, r in result if r > 0]))

    flatten_data = [[[2]], [[6]]]
    for i, r in result:
        flatten_data.append(data[i][0])
        flatten_data.append(data[i][1])
    ordered_packets = sorted(
        flatten_data, key=functools.cmp_to_key(cmp_list), reverse=True
    )

    result = 1
    for i, row in enumerate(ordered_packets):
        if row in ([[2]], [[6]]):
            result *= (i + 1)

    print("Star 2:", result)
