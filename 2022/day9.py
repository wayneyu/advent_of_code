from util import read_input

moves = read_input("inputs/day9.txt")


def print_rope(rope, m=None, n=None, visited=None):
    if not m:
        m = max([xy[0] for xy in visited])
    if not n:
        n = max([xy[1] for xy in visited])
    grid = [['.'] * (n + 1) for _ in range(m + 1)]
    offset_x, offset_y = m // 2 - 1, n // 2 - 1
    grid[offset_x][offset_y] = 's'
    if visited:
        for x, y in visited:
            grid[x + offset_x][y + offset_y] = '#'
    else:
        for i in range(len(rope))[::-1]:
            # print(i, rope[i][0] + offset_x, rope[i][1] + offset_y)
            grid[rope[i][0] + offset_x][rope[i][1] + offset_y] = str(i)

    print("\n".join(["".join(row) for row in reversed(grid)]) + "\n")


def next_rope_step(lead, follow):
    dx, dy = lead[0] - follow[0], lead[1] - follow[1]
    sign_dx = dx // abs(dx) if dx else 0
    sign_dy = dy // abs(dy) if dy else 0

    if abs(dx) > 1 or abs(dy) > 1:
        return [sign_dx, sign_dy]
    else:
        return [0, 0]


def solve(moves, rope_length):
    dxy = {'D': [-1, 0], 'U': [1, 0], 'L': [0, -1], 'R': [0, 1]}
    visited = {(0, 0)}
    rope = [[0, 0] for _ in range(rope_length)]
    for move in moves:
        direction, steps = move.split(" ")
        steps = int(steps)
        head_dx, head_dy = dxy[direction]
        for s in range(steps):
            rope[0][0] += head_dx
            rope[0][1] += head_dy
            for r in range(1, rope_length):
                visited.add(tuple(rope[-1]))
                dx, dy = next_rope_step(rope[r - 1], rope[r])
                # print("moving", r, rope[r-1], rope[r], dx, dy)
                if abs(dx) + abs(dy) > 2:
                    raise Exception("illegal move")
                rope[r][0] += dx
                rope[r][1] += dy
        visited.add(tuple(rope[-1]))
        # print_rope(rope, 30, 30, visited)
        # print(direction, s, rope, head_dx, head_dy)

    return len(visited)


# part 1
print(solve(moves, 2))

# part 2
print(solve(moves, 10))
