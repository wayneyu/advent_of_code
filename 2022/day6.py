from util import read_input

lines = read_input("inputs/day6.txt")


def first_marker(data, distinct_count):
    for i in range(distinct_count, len(data)):
        if len(set(data[i-distinct_count:i])) == distinct_count:
            return i
    return -1


for l in lines:
    print(first_marker(l, 4))
    print(first_marker(l, 14))
