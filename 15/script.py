from typing import NamedTuple
import re


class Point(NamedTuple):
    x: int
    y: int


def load_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            m = re.findall("=(-?\d+)", line)
            m = [int(el) for el in m]
            data.append([Point(m[0], m[1]), Point(m[2], m[3])])
    return data


def distance(point_a, point_b):
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)


def is_point_beaconless(point, data):
    for sensor, beacon in data:
        if point == beacon:
            return False
        if distance(point, sensor) <= distance(sensor, beacon):
            return True
    return False


def ranges_overlaps(range_a, range_b):
    ranges = sorted([range_a, range_b], key=lambda x: x[0])
    ra = ranges[0]
    rb = ranges[1]
    if rb[0] <= ra[1]:
        return True
    return False


def solve_1(data, y, return_ranges=False, trim_ranges=None):

    # get overlapping ranges of x for given y
    positive_ranges = list()
    for sensor, beacon in data:
        sb_distance = distance(sensor, beacon)
        threshold = abs(y - sensor.y)
        if threshold > sb_distance:
            continue
        diff = sb_distance - threshold
        start_x = sensor.x - diff
        stop_x = sensor.x + diff
        positive_ranges.append((start_x, stop_x))

    
    # trim ranges (for task 2)
    positive_ranges = sorted(positive_ranges, key=lambda x: x[0])
    tmp_ranges = list()
    if trim_ranges:
        for r in positive_ranges:
            r = list(r)
            if r[1] < trim_ranges[0]:
                continue
            if r[0] > trim_ranges[1]:
                continue
            if r[0] < trim_ranges[0]:
                r[0] = trim_ranges[0]
            if r[1] > trim_ranges[1]:
                r[1] = trim_ranges[1]
            tmp_ranges.append(tuple(r))
        positive_ranges = tmp_ranges

    # merge overlapping ranges (for task 2)
    start = 0
    while start < len(positive_ranges) - 1:
        for r_idx in range(start, len(positive_ranges) - 1):
            range_a = positive_ranges[r_idx]
            range_b = positive_ranges[r_idx+1]
            if ranges_overlaps(range_a, range_b):
                new_range = (
                    min(range_a[0], range_b[0]),
                    max(range_a[1], range_b[1])
                )
                break
        else:
            break
        positive_ranges[r_idx] = new_range
        positive_ranges.pop(r_idx+1)

    # count beaconless points
    result = 0
    beacons = set([b for s, b in data if b.y == y])
    for r in positive_ranges:
        result += r[1] - r[0] + 1
        for b in beacons:
            if ranges_overlaps(r, (b[0], b[0])):
                result -= 1

    if return_ranges:
        return result, positive_ranges
    return result


def solve_2(data, max_coord=4_000_000):
    # check all y
    for y in range(0, max_coord+1):
        print(y, end="\r")
        score, ranges = solve_1(
            data, y, return_ranges=True, trim_ranges=(0, max_coord)
        )
        if len(ranges) == 2:
            break
    x = ranges[0][1] + 1
    print("Coords:", x, y)
    result = x * 4000000 + y
    return result


def solve_1_naive(data, y):
    x_max = max(
        [p.x for record in data for p in record] +
        [record[0].x + distance(record[0], record[1]) for record in data]
    )
    x_min = min(
        [p.x for record in data for p in record] +
        [record[0].x - distance(record[0], record[1]) for record in data]
    )
    mask = []
    for x in range(x_min, x_max + 1):
        point = Point(x, y)
        mask.append(is_point_beaconless(point, data))

    return sum(mask)


if __name__ == "__main__":

    data = load_data("example.txt")
    y = 10
    print("Example 1 (naive):", solve_1_naive(data, y))
    print("Example 1:", solve_1(data, y))
    print("Example 2:", solve_2(data, max_coord=20))

    data = load_data("input.txt")
    y = 2_000_000
    print("Star 1:", solve_1(data, y))
    print("Star 2:", solve_2(data, max_coord=4_000_000))
