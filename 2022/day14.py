from util import read_input
import re
from functools import reduce
from collections import defaultdict
import heapq

lines = read_input("inputs/day14.txt")


def print_cave(cave):
    print("\n".join(["".join(c) for c in cave]))
    print("\n")


def add_line(cave, offset, start, end):
    offset_x, offset_y = offset

    for i in range(min(start[0], end[0]), max(start[0], end[0])+1):
        cave[i-offset_x][end[1]-offset_y] = "#"
    for j in range(min(start[1], end[1]), max(start[1], end[1])+1):
        cave[end[0]-offset_x][j-offset_y] = "#"


def fill_sand(cave, offset, source, stopping_x):
    offset_x, offset_y = offset
    sand_filled = 0
    while True:
        curr = source
        while True:
            down = (curr[0]+1, curr[1])
            down_left = (curr[0]+1, curr[1]-1)
            down_right = (curr[0]+1, curr[1]+1)
            if down[0]-offset_x == stopping_x or cave[source[0]-offset_x+1][source[1]-offset_y+1] == 'o':
                return sand_filled
            # print(down, down_left, down_right)
            if cave[down[0]-offset_x][down[1]-offset_y] == ".":
                curr = down
            elif cave[down_left[0]-offset_x][down_left[1]-offset_y] == ".":
                curr = down_left
            elif cave[down_right[0]-offset_x][down_right[1]-offset_y] == ".":
                curr = down_right
            else:
                cave[curr[0]-offset_x][curr[1]-offset_y] = "o"
                sand_filled += 1
                break


def get_cave(inputs, m, n, offset, source):
    cave = [['.' for _ in range(n)] for _ in range(m)]
    cave[source[0] - offset[0]][source[1] - offset[1]] = "+"
    max_x = float('-inf')
    for l in inputs:
        rock_line_points = [tuple([int(z) for z in reversed(xy.split(","))]) for xy in l.split(" -> ")]
        for i in range(len(rock_line_points)-1):
            add_line(cave, offset, rock_line_points[i], rock_line_points[i + 1])
            max_x = max(max(max_x, rock_line_points[i][0]), rock_line_points[i+1][0])

    return cave, max_x


# part 1
m, n = 200, 250
offset = (0, 400)
source = (0, 500)
cave, max_x = get_cave(lines, m, n, offset, source)
print(fill_sand(cave, offset, source, len(cave)-1))
# print_cave(cave)

# part 2
m, n = 200, 1000
offset = (0, 700)
source = (0, 500)
cave, max_x = get_cave(lines, m, n, offset, source)
floor = max_x + 2
for j in range(len(cave[0])):
    cave[floor-offset[0]][j] = "#"

print(fill_sand(cave, offset, source, 0)+1)
# print_cave(cave)
