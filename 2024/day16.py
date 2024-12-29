from util import read_input, print_matrix
import heapq

lines = read_input("./inputs/day16")
# lines = read_input("./inputs/day16_test")

map = [list(l) for l in lines]

def route_score(route):
    if not route:
        return 0
    score = 0
    for i in range(1, len(route)):
        pos = route[i]
        px, py, pd = pos
        lx, ly, ld = route[i-1]
        dx, dy, dd = px - lx, py - ly, abs(pd - ld)
        # print(pos, dx, dy, dd)
        if abs(dd) > 0:
            # print(pos, "+1000")
            score += 1000
        elif abs(dx) == 1 or abs(dy) == 1:
            # print(pos, "+1")
            score += 1
        else:
            raise Exception(f"Invalid move: {pos}")
        # print('calc_route', len(route), score)
    return score


def part1(map):
    m, n = len(map), len(map[0])
    sx, sy, sd = m-2, 1, 0
    ex, ey = 1, n-2
    print(map[sx][sy], map[ex][ey])
    # ex, ey = m-3, 1
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    def find_min(map, sx, sy, ex, ey):
        min_queue = []
        heapq.heapify(min_queue)
        route = [(sx, sy, sd)]
        heapq.heappush(min_queue, (0, (sx, sy, sd, route)))
        visited = {}
        while min_queue:
            # print('queue', min_queue)
            score, state = heapq.heappop(min_queue)
            # print('state', score, state)
            x, y, dir_idx, route = state

            if (x, y, dir_idx) in visited:
                vscore, vroutes = visited[(x, y, dir_idx)]
                if score < vscore:
                    visited[(x, y, dir_idx)] = (score, [route])
                elif score == vscore:
                    vroutes.append(route)
                continue
            else:
                visited[(x, y, dir_idx)] = (score, [route])

            # visited[(x, y, dir_idx)] = (score, [route])

            dx, dy = dirs[dir_idx]
            next_states_and_score = {
                (x + dx, y + dy, dir_idx): (score + 1, route + [(x + dx, y + dy, dir_idx)]),
                (x, y, (dir_idx - 1) % 4): (score + 1000, route + [(x, y, (dir_idx - 1)%4)]),
                (x, y, (dir_idx + 1) % 4): (score + 1000, route + [(x, y, (dir_idx + 1)%4)]),
            }
            for next_state, next_score_route in next_states_and_score.items():
                next_score, nroute = next_score_route
                nx, ny, ndir = next_state
                if map[nx][ny] != '#':
                    heapq.heappush(min_queue, (next_score, (nx, ny, ndir, nroute)))

        min_score = float('inf')
        for d in range(4):
            if (ex, ey, d) in visited:
                score, routes = visited[(ex, ey, d)]
                min_score = min(min_score, score)
        min_routes = []
        for d in range(4):
            if (ex, ey, d) in visited:
                score, routes = visited[(ex, ey, d)]
                if score == min_score:
                    min_routes += routes

        min_route_tiles = set()
        print(len(min_routes[0]))
        paths = set(min_routes[0])
        while paths:
            x, y, d = paths.pop()
            min_route_tiles.add((x, y))
            map[x][y] = 'O'
            for _path in visited[(x, y, d)][1]:
                for _x, _y, _d in _path:
                    if (_x, _y) not in min_route_tiles:
                        paths.add((_x, _y, _d))


        print_matrix(map)

        return min_score, len(min_route_tiles)

    return find_min(map, sx, sy, ex, ey)

print(part1(map))
