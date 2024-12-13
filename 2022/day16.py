from util import read_input
import heapq
import re

lines = read_input("inputs/day16_test.txt")


edges = {}
rates = {}
pattern = "Valve ([A-Z]+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([A-Z,\s]+)"
for l in lines:
    match = re.match(pattern, l)
    valve, rate, neighbors = match.groups()
    edges[valve] = [s.strip() for s in neighbors.split(",")]
    rates[valve] = int(rate)


def most_pressure_relived(valve_edges, rates):
    max_minutes = 30

    def cost_function(dist, valve):
        return - ((max_minutes-dist-1) * rates[valve])

    start = 'AA'
    costs = {start: cost_function(0, start)}
    q = [(start, costs[start], [start])]
    visited = {(start, None)}  # set of tuples with (valve, came_from_valve)
    opened = {start}
    while q:
        node, cost, path = heapq.heappop(q)
        for neighbor in valve_edges[node]:




print(most_pressure_relived(edges, rates))