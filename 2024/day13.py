from util import read_input
import re

lines = read_input("./inputs/day13")
# lines = read_input("./inputs/day13_test")

# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

machines = []
for l in lines:
    if l.startswith("Button A"):
        machines.append([])
    if l.startswith("Button"):
        pattern = r"Button\s([A|B]):\sX\+(\d+),\sY\+(\d+)"
        m = re.match(pattern, l)
        machines[-1].append((int(m[2]), int(m[3])))
    elif l.startswith("Prize"):
        pattern = r"Prize:\sX=(\d+),\sY=(\d+)"
        m = re.match(pattern, l)
        machines[-1].append((int(m[1]), int(m[2])))

def part1(machines, offset=0):
    def _rec(a, b, p, curr, cost, visited):
        # print(a, b, p, curr, cost)
        if p[0] < curr[0] or p[1] < curr[1]:
            return float("inf")
        if curr == p:
            return cost
        if curr in visited:
            return visited[curr]

        ax, ay = a
        bx, by = b
        cx, cy = curr

        n = (cx + ax, cy + ay)
        cost_a = _rec(a, b, p, n, cost + 3, visited)
        visited[n] = cost_a

        n = (cx + bx, cy + by)
        cost_b = _rec(a, b, p, n, cost + 1, visited)
        visited[n] = cost_b

        visited[curr] = min(cost_a, cost_b)

        return visited[curr]

    res = 0
    for a, b, p in machines:
        cost = _rec(a, b, (p[0] + offset, p[1] + offset), (0, 0), 0, {})
        print(a, b, p, cost)
        if cost != float("inf"):
            res += cost

    return res


def part2(machines, offset=0):

    cost = 0
    for _a, _b, _p in machines:
        a, b, c, d = _a[0], _b[0], _a[1], _b[1]
        det = a*d - b*c
        inv = [d, -b, -c, a]
        x, y = _p
        step_a = (inv[0] * (x + offset) + inv[1] * (y + offset))/det
        step_b = (inv[2] * (x + offset) + inv[3] * (y + offset))/det
        print(_a, _b, _p, step_a, step_b)
        if step_a.is_integer() and step_b.is_integer():
            cost += int(step_a) * 3 + int(step_b)

    return cost

print(part1(machines, 0))
print(part2(machines, 10000000000000))