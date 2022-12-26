from util import read_input
import re
from functools import reduce
from collections import defaultdict
import heapq

lines = read_input("inputs/day13.txt")


def parse_packet(packet, start):
    # str = [[1],[2,3,4]]
    st = []
    for c in packet:
        if c == '[':
            st.append([])
        elif c != ',' and c != "]":
            if isinstance(st[-1], str):
                st[-1] += c
            else:
                st.append(c)
        else:
            d = st.pop()
            if len(st) >= 1:
                if isinstance(d, str):
                    st[-1].append(int(d))
                else:
                    st[-1].append(d)
            else:
                st.append(d)

    return st[0]


def compare(left, right):
    # print(left, right)
    if isinstance(left, int) and isinstance(right, int):
        return 0 if left == right else (-1 if left < right else 1)
    elif isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            res = compare(l, r)
            if res != 0:
                return res
        return compare(len(left), len(right))
    elif isinstance(left, list) or isinstance(right, list):
        return compare([left] if isinstance(right, list) else left, [right] if isinstance(left, list) else right)
    else:
        raise Exception(f"{left} or {right} are not of valid types" )


def sort(packets):
    # bubble sort
    for i in range(len(packets)):
        for j in range(i, len(packets)):
            if compare(packets[i], packets[j]) == 1:
                packets[i], packets[j] = packets[j], packets[i]
    # print("\n".join([str(p) for p in packets]))
    return packets


pairs = [[]]
for l in lines:
    if l:
        pairs[-1].append(parse_packet(l, 0))
    else:
        pairs.append([])

# part 1
res = 0
for i, lr in enumerate(pairs):
    left, right = lr
    if compare(left, right) == -1:
        res += i+1
print(res)

# part 2
divider1, divider2 = [[2]], [[6]]
packets = [divider1, divider2] + [p[0] for p in pairs] + [p[1] for p in pairs]
sort(packets)
print((packets.index(divider1)+1) * (packets.index(divider2) + 1))
