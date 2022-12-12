import math
import heapq


def load_map(filename):
    with open(filename) as f:
        data = f.read().splitlines()

    y_s = y_e = -1
    for x, row in enumerate(data):
        y = row.find("S")
        if y >= 0:
            y_s = y
            x_s = x

        y = row.find("E")
        if y >= 0:
            y_e = y
            x_e = x


    data = [[ord(e) - 96 for e in list(r)] for r in data]
    data[x_s][y_s] = ord("a") - 96
    data[x_e][y_e] = ord("z") - 96
        
    return data, (x_s, y_s), (x_e, y_e)


def dijkstra(data, source):

    dist = dict()
    prev = dict()
    for x in range(len(data)):
        for y in range(len(data[0])):
            dist[(x, y)] = math.inf
            prev[(x, y)] = (-1, -1)

    dist[source] = 0
    pq = [(0, source)]

    while pq:
        current_distance, u = heapq.heappop(pq)
        if current_distance < dist[u]:
            continue

        for neighbor in [
            (u[0] + 1, u[1]), (u[0] - 1, u[1]),
            (u[0], u[1] + 1), (u[0], u[1] - 1)
        ]:
            if neighbor[0] < 0 or neighbor[0] >= len(data):
                continue
            if neighbor[1] < 0 or neighbor[1] >= len(data[0]):
                continue
            if data[u[0]][u[1]] - data[neighbor[0]][neighbor[1]] > 1:
                continue

            alt = dist[u] + 1
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = alt
                heapq.heappush(pq, (alt, neighbor))

    return dist, prev


if __name__ == "__main__":
    data, s_pos, e_pos = load_map("input.txt")
    dist, prev = dijkstra(data, e_pos)
    print("Star 1:", dist[s_pos])

    result = list()
    for x, row in enumerate(data):
        for y, height in enumerate(row):
            if height == 1:
                result.append(dist[(x, y)])
    print("Star 2:", min(result))



