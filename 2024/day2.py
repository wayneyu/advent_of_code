from util import read_input

lines = read_input("./inputs/day2")

# part 1
def is_safe(l):
    if l[0] == l[1]:
        return False
    dir = (l[1] - l[0])/abs(l[1] - l[0])
    for i in range(1, len(l)):

        if l[i] == l[i-1] or ((l[i] - l[i-1])/abs(l[i]-l[i-1]) != dir) or not (1 <= abs(l[i] - l[i-1]) <= 3):
            return False
    return True

def part1(lines):
    cnt = 0
    for l in lines:
        l = [int(x) for x in l.split()]
        # print(l, is_safe(l))
        cnt += 1 if is_safe(l) else 0

    return cnt

def part2(lines):
    cnt = 0
    for l in lines:
        l = [int(x) for x in l.split()]
        if is_safe(l):
            cnt += 1
            continue

        for i in range(len(l)):
            if is_safe(l[:i] + l[i+1:]):
                cnt += 1
                break
    return cnt

print(part1(lines))
print(part2(lines))