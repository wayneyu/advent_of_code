from util import read_input

lines = read_input("./inputs/day5")

rules = []
updates = []
for l in lines:
    if '|' in l:
        rules.append([int(a) for a in l.split('|')])
    elif '---' in l:
        break
    elif l:
        updates.append([int(a) for a in l.split(',')])

def check_valid(rules, update):
    for rule in rules:
        a, b = rule[0], rule[1]
        if a in update and b in update and update.index(a) > update.index(b):
            # print(a, b, update)
            return False
    return True

def part1(rules, updates):
    sum = 0
    for update in updates:
        if check_valid(rules, update):
            # print(update[len(update)//2])
            sum += update[len(update)//2]
    return sum

def part2(rules, updates):
    sum = 0
    rules_map = {}
    for rule in rules:
        a, b = rule[0], rule[1]
        if a in rules_map:
            rules_map[a].append(b)
        else:
            rules_map[a] = [b]
    print(rules_map)
    for update in updates:
        l = len(update)
        print(update)
        if not check_valid(rules, update):
            rules_map_for_update = {}
            for u in update:
                rules_map_for_update[u] = set(rules_map.get(u, [])) & set(update)
                print(u, rules_map_for_update.get(u, []))
            update = sorted(update, key=lambda x: len(rules_map_for_update.get(x, [])), reverse=True)

            print(update)
            if len(update) % 2 == 0 or l != len(update):
                raise Exception(f'update changed to {update}')
            sum += update[len(update)//2]
    return sum

print(part1(rules, updates))
print(part2(rules, updates))