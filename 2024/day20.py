from util import read_input, print_matrix

lines = read_input("./inputs/day20")
# lines = read_input("./inputs/day20_test")

map = [list(line) for line in lines]
m,n = len(map), len(map[0])
start, end = None, None
for i in range(m):
    for j in range(n):
        if map[i][j] == 'S':
            start = (i,j)
        elif map[i][j] == 'E':
            end = (i,j)
print(start, end)

def solve(map, start, end):
    path = [start]
    st = [(start, path)]
    visited = {}
    while st:
        ij, path = st.pop()
        i,j = ij
        visited[(i,j)] = path
        if (i,j) == end:
            return path
        for x,y in [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]:
            if 0 <= x < m and 0 <= y < n and map[x][y] != '#' and (x,y) not in visited:
                st.append(( (x,y), path + [(x,y)]))
    return []

def part1(map, start, end):
    path = solve(map, start, end)
    cheats = {}
    path_idx = {path[i]: i for i in range(len(path))}
    dxy = [(0,1), (0,-1), (1,0), (-1,0)]
    for x, y in path:
        for dx, dy in dxy:
            nx, ny = x + 2*dx , y + 2*dy
            if 0 < nx < m and 0 < ny < n and map[nx][ny] != '#' and (nx,ny) in path_idx:
                saves = path_idx[(nx, ny)] - path_idx[(x,y)] - 2
                if saves > 0:
                    cheats[saves] = cheats.get(saves, 0) + 1
    return sum([c for s,c in cheats.items() if s >= 100])

def part2(map, start, end, min_saves=100):
    path = solve(map, start, end)
    cheats = {}
    cheat_secs = 20
    for i in range(len(path)-4):
        x, y = path[i]
        for j in range(i+3, len(path)):
            px, py = path[j]
            dist = abs(px - x) + abs(py - y)
            if dist <= cheat_secs and dist < j - i:
                saves = j - i - dist
                cheats[saves] = cheats.get(saves, 0) + 1

    return sum([c for s,c in cheats.items() if s >= min_saves])

print(part1(map, start, end))
print(part2(map, start, end, 100))