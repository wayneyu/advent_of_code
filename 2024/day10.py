from util import read_input

lines = read_input("./inputs/day10")
# lines = read_input("./inputs/day10_test")

map = [[int(s) for s in l] for l in lines]

def score(map, trail_head_xy, count_visited = True):
    def _rec(map, pos, curr_lvl, visited, paths):
        x, y = pos
        if map[x][y] == 9:
            paths.append(9)

        m, n = len(map), len(map[0])
        steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for step in steps:
            dx, dy = step
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and map[nx][ny] == curr_lvl + 1 and (nx, ny) not in visited:
                if count_visited:
                    visited.add((nx, ny))
                _rec(map, (nx, ny), curr_lvl + 1, visited, paths)

    paths = []
    _rec(map, trail_head_xy, 0, set(), paths)
    return len(paths)

def part1(map, count_visited = True):
    res = 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 0:
                # print((i, j), score(map, (i, j)))
                res += score(map, (i, j), count_visited)

    return res

print(part1(map))
print(part1(map, False))