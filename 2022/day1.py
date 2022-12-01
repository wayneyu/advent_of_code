from util import read_input

lines = read_input("inputs/day1.txt")

calories = [0]
for l in lines:
    if not l:
        calories.append(0)
    else:
        calories[-1] += int(l)

print(max(calories))

print(sum(sorted(calories, reverse=True)[:3]))
