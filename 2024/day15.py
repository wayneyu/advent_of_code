from util import read_input, print_matrix

lines = read_input("./inputs/day15")
# lines = read_input("./inputs/day15_test")

map = []
is_map = True
moves = []
for l in lines:
    if is_map:
        if l:
            map.append(list(l))
    else:
        moves.append(l)
    if l == '':
        is_map = False

moves = list(''.join(moves))
move_to_dir = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}


def part1(map, moves):
    m, n = len(map), len(map[0])
    bot = (0,0)
    for i in range(m):
        for j in range(n):
            if map[i][j] == '@':
                bot = (i, j)

    # print_matrix(map)
    x, y = bot
    for mov in moves:
        dx, dy = move_to_dir[mov]
        nx, ny = x + dx, y + dy
        if map[nx][ny] == '.':
            map[nx][ny] = '@'
            map[x][y] = '.'
            x, y = nx, ny
        elif map[nx][ny] == 'O':
            for k in range(1, max(m, n)):
                ox, oy = nx + k*dx, ny + k*dy
                # print(ox, oy, map[ox][oy])
                if 0 <= ox < m and 0 <= oy < n:
                    if map[ox][oy] == '#':
                        break
                    elif map[ox][oy] == '.':
                        map[nx][ny] = '@'
                        map[ox][oy] = 'O'
                        map[x][y] = '.'
                        x, y = nx, ny
                        break


        # print(mov)
        # print_matrix(map)

    res = 0
    for i in range(m):
        for j in range(n):
            if map[i][j] == 'O':
                res += 100 * i + j

    return res


def move_2d_box(map, i, j, dx, dy):
    if dy == 0 and map[i][j] in ['[',']']:
        map[i+dx][j] = map[i][j]
        if map[i][j] == '[':
            map[i+dx][j+1] = map[i][j+1]
            map[i][j+1] = '.'
        else:
            map[i+dx][j-1] = map[i][j-1]
            map[i][j-1] = '.'
        map[i][j] = '.'
    return

def can_move_x(map, box, dx):
    x, y = box
    # if not (0 <= x < len(map) and 0 <= y < len(map[0])) and
    offset = 0 if map[x][y] == '[' else -1
    if map[x][y] in ['[',']']:
        y_to_check = [0, 1 if map[x][y] == '[' else -1]
        if any([map[x+dx][y+k] == '#' for k in y_to_check]):
            return False
        if all([map[x+dx][y+k] == '.' for k in y_to_check]):
            return True
        for k in range(-1 + offset, 2 + offset):
            if map[x + dx][y + k] == '[':
                if not can_move_x(map, (x + dx, y + k), dx):
                    return False
        return True
    else:
        return False

def child_boxes(map, pos, dx):
    def _rec(map, pos, dir, res):
        x, y = pos
        # print('child_box', pos, dx, ''.join(map[x][y:y+2]))
        if map[x][y] not in ['[', ']']:
            return res

        offset = 0 if map[x][y] == '[' else -1
        res.add((x, y + offset))
        for k in range(-1 + offset, 2 + offset):
            if map[x + dx][y + k] == '[':
                _rec(map, (x + dx, y + k), dir, res)

        return res

    return _rec(map, pos, dx, set())

def part2(map, moves):
    new_map = []
    m, n = len(map), len(map[0])
    for i in range(m):
        new_map.append([])
        for j in range(n):
            if map[i][j] == '#':
                new_map[-1].append('#')
                new_map[-1].append('#')
            elif map[i][j] == '.':
                new_map[-1].append('.')
                new_map[-1].append('.')
            elif map[i][j] == 'O':
                new_map[-1].append('[')
                new_map[-1].append(']')
            elif map[i][j] == '@':
                new_map[-1].append('@')
                new_map[-1].append('.')

    map = new_map
    m, n = len(map), len(map[0])
    bot = (0,0)
    for i in range(m):
        for j in range(n):
            if map[i][j] == '@':
                bot = (i, j)

    # print_matrix(map)
    x, y = bot
    for i, mov in enumerate(moves):
        dx, dy = move_to_dir[mov]
        nx, ny = x + dx, y + dy
        if map[nx][ny] == '.':
            map[nx][ny] = '@'
            map[x][y] = '.'
            x, y = nx, ny
        elif dx == 0 and map[nx][ny] in ['[',']']:
            for k in range(0, max(m, n)):
                ox, oy = nx + k*dx, ny + k*dy
                # print(ox, oy, map[ox][oy])
                if map[ox][oy] == '#':
                    break
                elif map[ox][oy] == '.':
                    ny, ny+k*dy
                    ny, ny-k*dy
                    offset = 0 if dy > 0 else 1
                    # print(ny, k, dy, ''.join(map[nx][min(ny + offset, ny+k*dy + offset):max(ny + offset, ny+k*dy + offset)]))
                    map[nx][min(ny + offset + dy, ny+k*dy + offset + dy) : max(ny + offset + dy, ny+k*dy + offset + dy)] = map[nx][min(ny + offset, ny+k*dy + offset):max(ny + offset, ny+k*dy + offset)]

                    map[nx][ny] = '@'
                    map[x][y] = '.'
                    x, y = nx, ny
                    break
        elif dy == 0 and map[nx][ny] in ['[',']']:

            can_move = can_move_x(map, (nx, ny), dx)
            if can_move:
                boxes_to_move = sorted(child_boxes(map, (nx, ny), dx), key=lambda x: abs(x[0] - nx), reverse=True)
                for bx, by in boxes_to_move:
                    move_2d_box(map, bx, by, dx, dy)
                map[nx][ny] = '@'
                map[x][y] = '.'
                x, y = nx, ny

        # print('mov', i, mov)
        # print_matrix(map)

    res = 0
    for i in range(m):
        for j in range(n):
            if map[i][j] == '[':
                res += 100 * i + j

    return res


print(part1(map, moves))
print(part2(map, moves[:]))