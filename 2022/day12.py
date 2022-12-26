from util import read_input
import re
from functools import reduce
from collections import defaultdict
import heapq

lines = read_input("inputs/day12.txt")

map = []
for l in lines:
    map.append(list(l))

def print_path(map, path):
    directions_symbols = [['', '^', ''], ['<', '', '>'], ['', 'v', '']]
    map = [['.']*len(map[0]) for _ in range(len(map))]

    for i in range(len(path)-1):
        x, y = path[i]
        dx, dy = path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]
        # print(dx, dy, x, y, map)
        map[x][y] = directions_symbols[dx+1][dy+1]

    print("\n".join(["".join(row) for row in map]))


def total_energy(map, path):
    return len(path) - 1


def shortest_path(map, max_energy, reversed=False):
    m, n = len(map), len(map[0])

    S, E = None, None
    for i in range(m):
        for j in range(n):
            if map[i][j] == 'S':
                S = (i, j)
            elif map[i][j] == 'E':
                E = (i, j)

    def neighbors(ij, m, n):
        i, j = ij
        return [(x, y) for x, y in [(i+1, j), (i, j+1), (i-1, j), (i, j-1)] if 0 <= x < m and 0 <= y < n]

    def elevation(map, coord):
        if coord == S:
            return ord('a')
        elif coord == E:
            return ord('z')
        else:
            return ord(map[coord[0]][coord[1]])

    if reversed:
        a, b = E, S
    else:
        a, b = S, E
    q = [(0, a)]
    pathTo = {a: [a]}
    while q:
        energy, node = heapq.heappop(q)
        # print(dist, node, visited)
        if (reversed and map[node[0]][node[1]] == 'a') or (not reversed and node == b):
            break
        for xy in neighbors(node, m, n):
            energy_needed = elevation(map, xy) - elevation(map, node)
            new_path_energy = energy + 1
            new_path = pathTo[node] + [xy]
            accessible = energy_needed <= max_energy if not reversed else energy_needed >= -1
            if accessible:
                if xy not in pathTo:
                    q.append((new_path_energy, xy))
                    pathTo[xy] = new_path
                elif new_path_energy < total_energy(map, pathTo[xy]):
                    pathTo[xy] = new_path

        # print_path(map, visited[node])
        # print(map, a, b)
        # print("\n")
    return pathTo[node] if reversed else pathTo[b]


# part 1
shortest_pathSE = shortest_path(map, 1)
print(total_energy(map, shortest_pathSE))
# print_path(map, shortest_pathSE)

# part 2
shortest_pathES = shortest_path(map, 1, True)
print(total_energy(map, shortest_pathES))
# print_path(map, shortest_pathES)
