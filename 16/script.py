import copy
import heapq
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


def dfs_with_elephant(
    current_node_h,
    current_node_e,
    valve_to_valves,
    valve_to_rate,
    closed_valves,
    time,
    current_score,
):

    if not closed_valves:
        return current_score

    scores = [current_score]
    closed_valves_pairs = combinations(closed_valves, 2)
    for target_h, target_e in closed_valves_pairs:
        new_time_h = time - 1 - valve_to_valves[current_node_h][target_h]
        new_time_e = time - 1 - valve_to_valves[current_node_e][target_e]
        new_closed = closed_valves.copy() - set([target_h, target_e])
        score_e = score_h = 0
        if new_time_e > 0:
            score_e = dfs_with_elephant(
                target_h,
                target_e,
                valve_to_valves,
                valve_to_rate,
                new_closed,
                new_time_e,
                current_score = (
                    current_score + new_time_e * valve_to_rate[target_e]
                )
            )
        if new_time_h > 0:
            score_h = dfs_with_elephant(
                target_h,
                target_e,
                valve_to_valves,
                valve_to_rate,
                new_closed,
                new_time_h,
                current_score = (
                    current_score + new_time_h * valve_to_rate[target_h]
                )
            )
        scores.append(score_e + score_h)

    score = max(scores)
    return score


def solve_1(filename):
    valve_to_valves, valve_to_rate = load_data(filename)
    valve_to_rate = {
        k: v for k, v in valve_to_rate.items() if v > 0
    }
    closed_valves = set(valve_to_rate.keys())

    result = dfs("AA", valve_to_valves, valve_to_rate, closed_valves, 30, 0)
    print(result)

def solve_2(filename):
    valve_to_valves, valve_to_rate = load_data(filename)
    valve_to_rate = {
        k: v for k, v in valve_to_rate.items() if v > 0
    }
    closed_valves = set(valve_to_rate.keys())

    result = dfs_with_elephant(
        "AA", "AA", valve_to_valves, valve_to_rate, closed_valves, 26, 0
    )
    print(result)

if __name__ == "__main__":
    solve_1("example.txt")
    solve_1("input.txt")
    solve_2("example.txt")
    solve_2("input.txt")


