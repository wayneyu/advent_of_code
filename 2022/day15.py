from util import read_input
import re
from functools import reduce
from collections import defaultdict
import heapq
import re

lines = read_input("inputs/day15.txt")


def l1(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def interval_length(intervals):
    return sum([b - a + 1 for a, b in intervals])


def combined_intervals(intervals):
    if not intervals:
        return 0

    intervals.sort()
    # print("intervals", intervals)
    combined_intervals = [intervals[0]]
    for a, b in intervals[1:]:
        if a <= combined_intervals[-1][1] + 1:
            combined_intervals[-1] = (combined_intervals[-1][0], max(b, combined_intervals[-1][1]))
        else:
            combined_intervals.append((a, b))

    # print("combined_intervals", combined_intervals)
    return combined_intervals


def xranges_without_beacons_for_y(sensors_beacons, y, min_xy=float('-inf'), max_xy=float('inf'), exclude_beacon=True):
    def xrange_without_beacons_for_y(sensor, l1_dist, y):
        if abs(sensor[1] - y) <= l1_dist:
            return sensor[0] - (l1_dist - abs(sensor[1] - y)), sensor[0] + (l1_dist - abs(sensor[1] - y))
        else:
            return None

    intervals = []
    for sensor, beacon in sensors_beacons:
        xrange = xrange_without_beacons_for_y(sensor, l1(sensor, beacon), y)
        if exclude_beacon and beacon[1] == y:
            if xrange and xrange[0] != xrange[1]:
                xrange = (xrange[0] + 1 if xrange[0] == beacon[0] else xrange[0], xrange[1] - 1 if xrange[1] == beacon[0] else xrange[1])
            else:
                xrange = None
        if xrange:
            intervals.append((max(min_xy, xrange[0]), min(max_xy, xrange[1])))

    return combined_intervals(intervals)


def count_no_beacons_locations(sensors_beacons):
    def xys_within_dist(origin, l1_dist):
        res = []
        for x in range(origin[0] - l1_dist, origin[0] + l1_dist + 1):
            for y in range(origin[1] - l1_dist, origin[1] + l1_dist + 1):
                if l1(origin, (x, y)) <= l1_dist:
                    res.append((x, y))

        return res

    locations_without_beacons = set()
    for sensor, beacon in sensors_beacons:
        xys = xys_within_dist(sensor, l1(sensor, beacon))
        xys.remove(sensor)
        xys.remove(beacon)
        locations_without_beacons.update(xys)

    return locations_without_beacons


sensors_beacons = []
pattern = "Sensor at x=([+\-\d]+), y=([+\-\d]+): closest beacon is at x=([+\-\d]+), y=([+\-\d]+)"
for l in lines:
    match = re.match(pattern, l)
    sx, sy, bx, by = [int(x) for x in match.groups()]
    sensors_beacons.append(((sx, sy), (bx, by)))


# part 1
y = 2000000
print(interval_length(xranges_without_beacons_for_y(sensors_beacons, y)))

# part 2
max_xy = 4000000
for y in range(0, max_xy+1):
    xranges = xranges_without_beacons_for_y(sensors_beacons, y, 0, max_xy, False)
    if len(xranges) > 1:
        print(4000000 * (xranges[0][1] + 1) + y)
        break
