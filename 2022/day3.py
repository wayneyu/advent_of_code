from util import read_input

rucksacks = read_input("inputs/day3.txt")


def priority(type):
    if type.islower():
        return ord(type) - ord('a') + 1
    else:
        return ord(type) - ord('A') + 27

# part 1
ans = 0
for rucksack in rucksacks:
    size = len(rucksack)
    compartment1 = rucksack[:size // 2]
    compartment2 = rucksack[size // 2:]

    common = list(set(compartment1).intersection(set(compartment2)))[0]
    ans += priority(common)

print(ans)

# part 2
ans = 0
for i in range(0, len(rucksacks), 3):
    rucksack1 = rucksacks[i]
    rucksack2 = rucksacks[i + 1]
    rucksack3 = rucksacks[i + 2]

    badge = list(set(rucksack1).intersection(set(rucksack2)).intersection(set(rucksack3)))[0]
    ans += priority(badge)

print(ans)
