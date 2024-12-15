from util import read_input, print_matrix

lines = read_input("./inputs/day8")
# lines = read_input("./inputs/day8_test")

map = [list(l) for l in lines]
antennas = {}
m, n = len(map), len(map[0])
for i in range(m):
    for j in range(n):
        if map[i][j] == '.':
            continue
        if map[i][j] not in antennas:
            antennas[map[i][j]] = [(i,j)]
        else:
            antennas[map[i][j]].append((i,j))
print(antennas)

def pair_idx_combos(n):
    def _rec(arr, start):
        if start == len(arr) - 1:
            return []
        return [(start, i) for i in range(start + 1, len(arr))] + _rec(arr, start + 1)

    return _rec(range(n), 0)

def solve(map, antennas, possible_antinodes = 1):
    m, n = len(map), len(map[0])
    antennas_pairs = []
    antinodes = set()
    for k, locs in antennas.items():
        for (id1, id2) in pair_idx_combos(len(locs)):
            antennas_pairs.append((locs[id1], locs[id2]))

    for (p1, p2) in antennas_pairs:
        p1x, p1y = p1
        p2x, p2y = p2
        dx, dy = p1x - p2x, p1y - p2y
        for x, y in [p1, p2]:
            for sign in [-1, 1]:
                for k in range(1, possible_antinodes + 1):
                    p1x_antinode, p1y_antinode = x + sign * k * dx, y + sign * k * dy
                    if 0 <= p1x_antinode < m and 0 <= p1y_antinode < n and (p1x_antinode, p1y_antinode) not in ([p1, p2] if possible_antinodes == 1 else []):
                        antinodes.add((p1x_antinode, p1y_antinode))

    for a1, a2 in antinodes:
        if map[a1][a2] == '.':
            map[a1][a2] = '#'
    print_matrix(map)

    return len(antinodes)

print(solve(map, antennas, 1))
print(solve(map, antennas, max(m, n)))