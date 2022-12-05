from util import read_input
import re

lines = read_input("inputs/day5.txt")

#     [D]
# [N] [C]
# [Z] [M] [P]
# 1   2   3
#
# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2

def pivot(rows):
    ncol = max([len(r) for r in rows])
    columns = [[] for _ in range(0, ncol)]
    for row in rows[::-1]:
        for j in range(0, len(row)):
            if row[j]:
                columns[j].append(row[j])
    return columns


is_parsing_stack = True
rows = []
moves = []
for l in lines:
    if l:
        if is_parsing_stack:
            if '[' in l:
                # extract crate by using indexing into the row, only works if number of stacks is below 10
                row = []
                for i in range(1, len(l), 4):
                    if i < len(l):
                        if l[i] != ' ':
                            row.append(l[i])
                        else:
                            row.append(None)
                rows.append(row)
        else:
            result = re.match(r"move (\d+) from (\d+) to (\d+)", l)
            if result:
                ncrates, a, b = int(result.group(1)), int(result.group(2)), int(result.group(3))
                moves.append((ncrates, a, b))
            else:
                print("No match found")

    else:
        is_parsing_stack = False


# part 1
stacks = pivot(rows)
for move in moves:
    ncrates, a, b = move
    to_move = list(reversed(stacks[a-1][-ncrates:]))
    stacks[a-1] = stacks[a-1][:-ncrates]
    stacks[b-1] += to_move
    # print("after moving {ncrates} crates from {a} to {b}:")
    # print(stacks)

print(''.join([stack[-1] for stack in stacks]))


# part 2
stacks = pivot(rows)
for move in moves:
    ncrates, a, b = move
    to_move = stacks[a-1][-ncrates:]
    stacks[a-1] = stacks[a-1][:-ncrates]
    stacks[b-1] += to_move
    # print("after moving {ncrates} crates from {a} to {b}:")
    # print(stacks)

print(''.join([stack[-1] for stack in stacks]))
