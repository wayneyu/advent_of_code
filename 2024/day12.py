from util import read_input

lines = read_input("./inputs/day12")
# lines = read_input("./inputs/day12_test")

map = [list(l) for l in lines]

def find_perimeter(plots):
    plot_and_neighbors = {}
    for p in plots:
        px, py = p
        ns = set([(px+dx, py+dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]])
        plot_and_neighbors[p] = ns & plots

    perimeter = 0
    for p, ns in plot_and_neighbors.items():
        perimeter += 4 - len(ns)

    return perimeter

def find_region(map):
    def _rec(map, pos, region_id, plots, visited):
        x, y = pos
        m, n = len(map), len(map[0])
        steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # print(pos, plots)
        for step in steps:
            dx, dy = step
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and map[nx][ny] == region_id and (nx, ny) not in visited:
                visited.add((nx, ny))
                plots.add((nx, ny))
                _rec(map, (nx, ny), region_id, plots, visited)
        return plots

    m, n = len(map), len(map[0])
    regions = {}
    visited = set()
    for i in range(m):
        for j in range(n):
            plots = set()
            if (i,j) not in visited:
                plots.add((i, j))
                visited.add((i, j))
                _rec(map, (i, j), map[i][j], plots, visited)
                if map[i][j] not in regions:
                    regions[map[i][j]] = [plots]
                else:
                    regions[map[i][j]].append(plots)
    return regions

def part1(map):
    regions = find_region(map)
    res = 0
    # print(regions)
    for id, plot_sets in regions.items():
        for plots in plot_sets:
            # print(id, len(plots), find_perimeter(plots))
            res += find_perimeter(plots) * len(plots)

    return res

def bounding_box(plots):
    min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
    for p in plots:
        x, y = p
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x+1)
        max_y = max(max_y, y+1)

    return min_x, min_y, max_x, max_y

def find_sides(plots):
    def _plot_lines(i, j):
        return [(i, j, i+1, j), (i, j+1, i+1, j+1), (i, j, i, j+1), (i+1, j, i+1, j+1)]

    min_x, min_y, max_x, max_y = bounding_box(plots)

    horizontals = {}
    verticals = {}
    north_south_neighbors = [(-1, 0), (1, 0)]
    west_east_neighbors = [(0, -1), (0, 1)]
    horizontals = {}
    verticals = {}
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            if (i, j) in plots:
                north_south_visible = [((i + dx, j + dy) not in plots) for dx, dy in north_south_neighbors]
                for ii in range(len(north_south_visible)):
                    if north_south_visible[ii]:
                        if (i, ii) in horizontals:
                            horizontals[(i, ii)].append(j)
                        else:
                            horizontals[(i, ii)] = [j]
                west_east_visible = [((i + dx, j + dy) not in plots) for dx, dy in west_east_neighbors]
                for jj in range(len(west_east_visible)):
                    if west_east_visible[jj]:
                        if (jj, j) in verticals:
                            verticals[(jj, j)].append(i)
                        else:
                            verticals[(jj, j)] = [i]

    sides = 0
    for x, ys in horizontals.items():
        ys = sorted(ys)
        sides += 1
        for j in range(len(ys)-1):
            if ys[j+1] - ys[j] > 1:
                sides += 1
    for y, xs in verticals.items():
        xs = sorted(xs)
        sides += 1
        for i in range(len(xs)-1):
            if xs[i+1] - xs[i] > 1:
                sides += 1

    # print("verticals")
    # print(verticals)
    # print('horizontals')
    # print(horizontals)
    # print('sides')
    # print(sides)

    return sides

def part2(map):
    regions = find_region(map)
    res = 0

    for id, plot_sets in regions.items():
        for plots in plot_sets:
            n = len(plots)
            sides = find_sides(plots)
            print(f"id: {id}, n: {n}, sides: {sides}")
            print('-----')
            res += n * sides

    return res


print(part1(map))
print(part2(map))