from util import read_input

lines = read_input("./inputs/day1")

l1, l2 = [],[]
for l in lines:
    x,y = l.split()
    l1.append(x)
    l2.append(y)

# Part 1
sum = 0
l1_sorted = sorted(l1)
l2_sorted = sorted(l2)
for i in range(len(l1_sorted)):
    sum += abs(int(l1_sorted[i]) - int(l2_sorted[i]))

print(sum)

# Part 2
freq = {}
for i in range(len(l2)):
    y = int(l2[i])
    if y in freq:
        freq[y] += 1
    else:
        freq[y] = 1

sum = 0
for i in range(len(l1)):
    x = int(l1[i])
    sum += x * freq.get(x, 0)
print(sum)