from util import read_input
from functools import reduce

lines = read_input("inputs/day8.txt")


def print_matrix(matrix):
    print("\n".join([str(row) for row in matrix]) + "\n")


trees = []
for l in lines:
    trees.append([int(ch) for ch in l])

# part 1
m, n = len(trees), len(trees[0])
# matrix to keep track of visibility of each square, 0 for not visible, 1 for visible
visibility = [[0]*n for i in range(0, m)]

# find visible trees from left and from right
for i in range(0, m):
    left_max, right_max = float('-inf'), float('-inf')
    for j in range(0, n):
        if left_max < trees[i][j]:
            visibility[i][j] = 1
            left_max = trees[i][j]
        if right_max < trees[i][n - j - 1]:
            visibility[i][n-j-1] = 1
            right_max = trees[i][n - j - 1]

# find visible trees from top and from bottom
for j in range(0, n):
    top_max, bottom_max = float('-inf'), float('-inf')
    for i in range(0, m):
        if top_max < trees[i][j]:
            visibility[i][j] = 1
            top_max = trees[i][j]
        if bottom_max < trees[m - i - 1][j]:
            visibility[m-i-1][j] = 1
            bottom_max = trees[m - i - 1][j]

print(sum([sum(row) for row in visibility]))

# part 2
tallest_tree = 9
# scenic score of each tree, each tuple represents the scenic score in left,right,top,bottom direction in that order
scenic_score = [[[0,0,0,0] for _ in range(n)] for _ in range(m)]
for i in range(m):
    last_seen_from_left = [0] * (tallest_tree + 1)
    last_seen_from_right = [n-1] * (tallest_tree + 1)
    for j in range(n):
        left_pointer, right_pointer = j, n-j-1
        height_at_left_pointer = trees[i][left_pointer]
        height_at_right_pointer = trees[i][right_pointer]
        scenic_score[i][left_pointer][0] = left_pointer - last_seen_from_left[height_at_left_pointer]
        scenic_score[i][right_pointer][1] = last_seen_from_right[height_at_right_pointer] - right_pointer
        # print(i,j, height_at_left_pointer, height_at_right_pointer, scenic_score[2][0])
        for h in range(height_at_left_pointer + 1):
            last_seen_from_left[h] = max(left_pointer, last_seen_from_left[h])
        for h in range(height_at_right_pointer + 1):
            last_seen_from_right[h] = min(right_pointer, last_seen_from_right[h])
        # print(last_seen_from_left)
        # print(last_seen_from_right)

for j in range(n):
    last_seen_from_top = [0] * (tallest_tree + 1)
    last_seen_from_bottom = [m-1] * (tallest_tree + 1)
    for i in range(m):
        top_pointer, bottom_pointer = i, m-i-1
        height_at_top_pointer = trees[top_pointer][j]
        height_at_bottom_pointer = trees[bottom_pointer][j]
        scenic_score[top_pointer][j][2] = top_pointer - last_seen_from_top[height_at_top_pointer]
        scenic_score[bottom_pointer][j][3] = last_seen_from_bottom[height_at_bottom_pointer] - bottom_pointer
        for h in range(height_at_top_pointer + 1):
            last_seen_from_top[h] = max(top_pointer, last_seen_from_top[h])
        for h in range(height_at_bottom_pointer + 1):
            last_seen_from_bottom[h] = min(bottom_pointer, last_seen_from_bottom[h])

print(max(max([reduce(lambda a, b: a*b, scores, 1) for scores in row]) for row in scenic_score))

