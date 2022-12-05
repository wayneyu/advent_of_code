from util import read_input

lines = read_input("inputs/day4.txt")

res1 = 0
res2 = 0
for l in lines:
    p1, p2 = l.split(',')
    a1, a2 = p1.split('-')
    b1, b2 = p2.split('-')
    a1, a2, b1, b2 = int(a1), int(a2), int(b1), int(b2)

    res1 += a1 <= b1 <= b2 <= a2 or b1 <= a1 <= a2 <= b2
    res2 += max(a1, b1) <= min(a2, b2)

print(res1)
print(res2)
