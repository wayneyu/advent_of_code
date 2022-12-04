from util import read_input

lines = read_input("inputs/day4.txt")

res1 = 0
res2 = 0
for l in lines:
    p1, p2 = l.split(',')
    p1s, p1e = p1.split('-')
    p2s, p2e = p2.split('-')
    p1s, p1e, p2s, p2e = int(p1s), int(p1e), int(p2s), int(p2e)

    res1 += bool(p1s <= p2s <= p2e <= p1e or p2s <= p1s <= p1e <= p2e)
    res2 += bool(max(p1s, p2s) <= min(p1e, p2e))

print(res1)
print(res2)
