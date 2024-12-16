from util import read_input

lines = read_input("./inputs/day9")
# lines = read_input("./inputs/day9_test")

disk_map = [int(c) for c in lines[0]]

def part1(disk_map):
    file_blocks = []
    free_blocks = []
    for i in range(len(disk_map)):
        if i % 2 == 0:
            file_blocks.append(disk_map[i])
        else:
            free_blocks.append(disk_map[i])
    # print(file_blocks)
    # print(free_blocks)

    pfile = len(file_blocks) - 1
    pfree = 0
    filled = [[] for _ in range(len(free_blocks))]
    while pfree < len(free_blocks):
        if file_blocks[pfile] < free_blocks[pfree]:
            filled[pfree].append((pfile, file_blocks[pfile]))
            free_blocks[pfree] -= file_blocks[pfile]
            pfile -= 1
            file_blocks.pop()
            free_blocks.pop()
            filled.pop()
        elif file_blocks[pfile] == free_blocks[pfree]:
            filled[pfree].append((pfile, file_blocks[pfile]))
            pfile -= 1
            file_blocks.pop()
            free_blocks.pop()
            filled.pop()
            pfree += 1
        else:
            filled[pfree].append((pfile, free_blocks[pfree]))
            file_blocks[pfile] -= free_blocks[pfree]
            pfree += 1

    checksum = 0
    p = 0
    disk = []
    for i in range(len(file_blocks)):
        for fi in range(file_blocks[i]):
            checksum += p * i
            disk.append(i)
            p += 1
        if i < len(filled):
            for idx, nbytes in filled[i]:
                for bi in range(nbytes):
                    checksum += p * idx
                    disk.append(idx)
                    p += 1
    # print(''.join([str(b) for b in disk]))
    return checksum


def part2(disk_map):
    file_blocks = []
    free_blocks = []
    for i in range(len(disk_map)):
        if i % 2 == 0:
            file_blocks.append(disk_map[i])
        else:
            free_blocks.append(disk_map[i])
    # print(file_blocks)
    # print(free_blocks)
    filled = [[] for _ in range(len(free_blocks))]
    exists = [1 for _ in range(len(file_blocks))]
    for pfile in range(len(file_blocks) - 1, 0, -1):
        for pfree in range(pfile):
            if file_blocks[pfile] <= free_blocks[pfree]:
                free_blocks[pfree] -= file_blocks[pfile]
                exists[pfile] = 0
                filled[pfree].append(pfile)
                break

    # print(file_blocks)
    # print(exists)
    # print(free_blocks)
    # print(filled)

    check_sum = 0
    p = 0
    disk = []
    for i in range(len(file_blocks)):
        for k in range(file_blocks[i]):
            check_sum += p * exists[i] * i
            disk.append(i if exists[i] else '.')
            p += 1

        if i < len(free_blocks):
            for j in filled[i]:
                for k in range(file_blocks[j]):
                    disk.append(j)
                    check_sum += p * j
                    p += 1
            for f in range(free_blocks[i]):
                disk.append('.')
                p += 1

    # print(disk)
    return check_sum

print(part1(disk_map))
print(part2(disk_map))