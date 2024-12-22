from util import read_input, print_matrix
import re
import time

lines = read_input("./inputs/day14")
# lines = read_input("./inputs/day14_test")

robots = []
for l in lines:
    # p=44,68 v=-28,46
    pattern = r"p=(-?\d+),(-?\d+)\sv=(-?\d+),(-?\d+)"
    m = re.match(pattern, l)
    robots.append([int(k) for k in [m[1], m[2], m[3], m[4]]])


def part1(robots, m, n, secs, calc_sec_factor=True):
    for sec in range(1, secs+1):
        mat = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(len(robots)):
            y, x, vy, vx = robots[i]
            x = (x + vx) % m
            y = (y + vy) % n
            robots[i] = [y, x, vy, vx]

            mat[x][y] += 1
            # system sleep 2 sec

        if calc_sec_factor:
            quad_count = [0, 0, 0, 0]
            for x in range(m):
                for y in range(n):
                    if x < m//2 and y < n//2:
                        quad_count[0] += mat[x][y]
                    elif x < m//2 and y > n//2:
                        quad_count[1] += mat[x][y]
                    elif x > m//2 and y < n//2:
                        quad_count[2] += mat[x][y]
                    elif x > m//2 and y > n//2:
                        quad_count[3] += mat[x][y]
            sec_factor = 1
            for i in range(4):
                sec_factor *= quad_count[i]

        n_mat = [['-' if k == 0 else 'X' for k in mat[i]] for i in range(30, len(mat)-30) if i % 1 == 0]

        # mirror_pair_count = 0
        # for x in range(m//2):
        #     for y in range(n):
        #         if y < n//2 and n_mat[x][y] == 'X' and n_mat[x][n-y-1] == 'X':
        #             mirror_pair_count += 1

        avg = len(robots)/4
        threshold = 1*avg
        if calc_sec_factor:
            if any([abs(k - avg) > threshold for k in quad_count]):
                print("after sec", sec, "deviation is higher than ", threshold, "quad_count", quad_count)
                print_matrix(n_mat)
                return

    return sec_factor

print(part1(robots, 103, 101, 100, True))
# print(part1(robots, 7, 11, 100))
print(part1(robots, 103, 101, 10000))