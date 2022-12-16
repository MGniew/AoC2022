import copy
import heapq
from itertools import permutations
from itertools import combinations
import math
import re


def dijkstra(valve_to_valves, source):
    dist = dict()
    prev = dict()

    for k in valve_to_valves.keys():
        dist[k] = math.inf
        prev[k] = k

    dist[source] = 0
    pq = [(0, source)]

    while pq:
        current_distance, u = heapq.heappop(pq)
        if current_distance < dist[u]:
            continue
        for neighbor in valve_to_valves[u]:
            alt = dist[u] + 1
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = alt
                heapq.heappush(pq, (alt, neighbor))
    return dist, prev


def load_data(filename):
    with open(filename) as f:
        data = f.read().splitlines()
    valve_to_rate = dict()
    valve_to_valves = dict()

    for line in data:
        valve = re.findall("Valve (.{2})", line)[0]
        rate = int(re.findall("=(\d+)", line)[0])
        targets = re.findall("valves? (.*)", line)[0].split(", ")
        valve_to_rate[valve] = rate
        valve_to_valves[valve] = targets
    
    valve_to_valves = {
        s: dijkstra(valve_to_valves, s)[0] for s in valve_to_rate.keys()
    }
    return valve_to_valves, valve_to_rate



def dfs(
    current_node,
    valve_to_valves,
    valve_to_rate,
    closed_valves,
    time,
    current_score
):

    if not closed_valves:
        return current_score
    scores = [current_score]
    for target in closed_valves:
        new_time = time - 1 - valve_to_valves[current_node][target]
        if new_time <= 0:
            continue
        new_closed = closed_valves.copy()
        new_closed.remove(target)
        score = dfs(
            target,
            valve_to_valves,
            valve_to_rate,
            new_closed,
            new_time,
            current_score = current_score + new_time * valve_to_rate[target]
        )
        scores.append(score)
    score = max(scores)
    return score


# could be easily improved, but fuck it
def upper_bound(
    current_score,
    nodes_left,
    time_left,
    valve_to_rate
):
    left_rates = sorted(
        [valve_to_rate.get(v, 0) for v in nodes_left], reverse=True
    )
    bound = 0
    for i, lr in enumerate(left_rates):
        if i % 2 == 0:
            time_left -= 1
        if time_left < 0:
            time_left = 0
        bound += lr * time_left
    return current_score + bound


def dfs_with_elephant(
    current_node_h,
    current_node_e,
    valve_to_valves,
    valve_to_rate,
    closed_valves,
    time_h,
    time_e,
    current_score_h,
    current_score_e,
    current_best=0
):
    current_score = current_score_h + current_score_e
    if not closed_valves:
        return current_score
    bound = upper_bound(
        current_score,
        closed_valves,
        max(time_h, time_e),
        valve_to_rate
    )
    if bound <= current_best:
        return current_best

    scores = [current_score]
    if len(closed_valves) == 1:
        closed_valves.add("")
    if current_node_h == current_node_e:
        closed_valves_pairs = combinations(closed_valves, 2)
    else:
        closed_valves_pairs = permutations(closed_valves, 2)

    for target_h, target_e in closed_valves_pairs:
        new_closed = closed_valves - set([target_h, target_e])
        new_time_h = time_h - 1 - valve_to_valves[current_node_h].get(target_h, math.inf)
        new_time_e = time_e - 1 - valve_to_valves[current_node_e].get(target_e, math.inf)
        score_e = current_score_e
        score_h = current_score_h
        tmp_score_h = current_score_h
        tmp_score_e = current_score_e

        if new_time_h <= 0 and new_time_e <= 0:
            continue
        if new_time_h > 0:
            tmp_score_h = (
                current_score_h + new_time_h * valve_to_rate.get(target_h, 0)
            )
        if new_time_e > 0:
            tmp_score_e = (
                current_score_e + new_time_e * valve_to_rate.get(target_e, 0)
            )

        score = dfs_with_elephant(
            current_node_h=target_h,
            current_node_e=target_e,
            valve_to_valves=valve_to_valves,
            valve_to_rate=valve_to_rate,
            closed_valves=new_closed,
            time_h=new_time_h,
            time_e=new_time_e,
            current_score_h=tmp_score_h,
            current_score_e=tmp_score_e,
            current_best=current_best,
        )
        if score > current_best:
            current_best = score
        scores.append(score)

    return max(scores)


def solve_1(filename):
    valve_to_valves, valve_to_rate = load_data(filename)
    valve_to_rate = {
        k: v for k, v in valve_to_rate.items() if v > 0
    }
    closed_valves = set(valve_to_rate.keys())
    result = dfs("AA", valve_to_valves, valve_to_rate, closed_valves, 30, 0)
    return result

def solve_2(filename):
    valve_to_valves, valve_to_rate = load_data(filename)
    valve_to_rate = {
        k: v for k, v in valve_to_rate.items() if v > 0
    }
    closed_valves = set(valve_to_rate.keys())
    result = dfs_with_elephant(
        "AA", "AA", 
        valve_to_valves, valve_to_rate,
        closed_valves,
        26, 26,
        0, 0
    )
    print()
    return result

if __name__ == "__main__":
    print("Star 1 (example),", solve_1("example.txt"))
    print("Star 1 (input),", solve_1("input.txt"))
    print("Star 2 (example),", solve_2("example.txt"))
    print("Star 2 (input),", solve_2("input.txt"))


