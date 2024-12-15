from util import read_input, print_matrix
import copy

lines = read_input("./inputs/day6")
# lines = read_input("./inputs/day6_test")

map = [list(l) for l in lines]
m, n = len(map), len(map[0])
init_ij = (0, 0)
for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == '^':
            init_ij = (i, j)
            break
print(init_ij)
print_matrix(map)
print('\n')

# up, right, down, left
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def part1(_map, init_ij, check_loop=False):
    m, n = len(_map), len(_map[0])
    map = copy.deepcopy(_map)
    i, j = init_ij
    # i, j and dir_idx
    visited = {(i, j, 0)}
    dir_idx = 0
    dx, dy = dirs[dir_idx]
    while True:
        i, j = i + dx, j + dy
        if not (0 <= i < m and 0 <= j < n):
            break

        if map[i][j] == '#' or map[i][j] == 'O':
            i, j = i - dx, j - dy
            dir_idx = (dir_idx + 1) % 4
            dx, dy = dirs[dir_idx]
        else:
            if check_loop and (i,j,dir_idx) in visited:
                return -1
            visited.add((i, j, dir_idx))
            map[i][j] = 'X'

    map[init_ij[0]][init_ij[1]] = '^'
    # print_matrix(map)
    return len(set([(i,j) for i, j, _ in visited]))


def part2(_map, init_ij):
    m, n = len(_map), len(_map[0])
    loops = 0
    for i in range(m):
        for j in range(n):
            if (i,j) != init_ij and _map[i][j] != '#':
                map = copy.deepcopy(_map)
                map[i][j] = 'O'
                if part1(map, init_ij, True) == -1:
                    # print_matrix(map)
                    print("found loop by placing obstacle at", i, j)
                    loops += 1

    return loops


print(part1(map, init_ij, False))
print(part2(map, init_ij))