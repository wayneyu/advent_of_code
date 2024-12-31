from util import read_input, print_matrix

lines = read_input("./inputs/day18")
# lines = read_input("./inputs/day18_test")

mem = [[int(a) for a in l.split(',')] for l in lines]

def part1(mem, bytes, size):
    map = [['.' for _ in range(size)] for _ in range(size)]
    for x,y in mem[:bytes]:
        map[y][x] = '#'
    # print_matrix(map)

    # bfs
    stack = []
    start = (0,0,0)
    end = (size-1, size-1)
    stack.append(start)
    while stack:
        x, y, lvl = stack.pop(0)
        if (x, y) == end:
            return lvl
        if x < 0 or y < 0 or x >= size or y >= size:
            continue
        if map[y][x] == '#':
            continue
        map[y][x] = '#'
        stack.append((x+1, y, lvl+1))
        stack.append((x-1, y, lvl+1))
        stack.append((x, y+1, lvl+1))
        stack.append((x, y-1, lvl+1))
    return -1

def part2(mem, size):
    for bytes in range(1025, len(mem)):
        res = part1(mem, bytes, size)
        if res == -1:
            return ','.join([str(a) for a in mem[:bytes][-1]])
    return -1

print(part1(mem, 1024, 71))
print(part2(mem, 71))