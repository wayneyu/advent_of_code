# https://adventofcode.com/2021
from collections import deque, defaultdict
import heapq
import string
from copy import copy

class Solve:

    def read_input(self, file):
        with open(f'inputs/{file}', 'r') as f:
            arr = [l.strip() for l in f.readlines()]
        return arr

    def day1(self):
        depths = [int(x) for x in self.read_input('day1')]
        cnt = 0
        for i in range(1, len(depths)):
            cnt += 1 if depths[i-1] < depths[i] else 0
        print(cnt)

        cnt = 0
        for i in range(1, len(depths)-2):
            cnt += 1 if sum(depths[i-1:i+2]) < sum(depths[i:i+3]) else 0
        print(cnt)

    def day2(self):
        cmds = self.read_input('day2')
        xe, de = 0, 0
        for c in cmds:
            cmd, x = c.split()
            x = int(x)
            if cmd == 'forward':
                xe += x
            elif cmd == 'up':
                de -= x
            elif cmd == 'down':
                de += x
        print(xe*de)

        xe, de, aim = 0, 0, 0
        for c in cmds:
            cmd, x = c.split()
            x = int(x)
            if cmd == 'forward':
                xe += x
                de += x*aim
            elif cmd == 'up':
                aim -= x
            elif cmd == 'down':
                aim += x
        print(xe*de)

    def day3(self):
        digits = self.read_input('day3')

        def count_ones(arr):
            ones_count = [0]*len(arr[0])
            for d in arr:
                for i in range(len(d)):
                    if d[i] == '1':
                        ones_count[i] += 1
            return ones_count

        e = int(''.join(['1' if c > len(digits)//2 else '0' for c in count_ones(digits)]), 2)
        g = int(''.join(['1' if c < len(digits)//2 else '0' for c in count_ones(digits)]), 2)

        print(e*g)

        ds = digits.copy()
        for i in range(len(digits)):
            ones_count = count_ones(ds)
            new_ds = []
            for d in ds:
                if d[i] == ('1' if ones_count[i] >= (len(ds)-ones_count[i]) else '0'):
                    new_ds.append(d)
            # print(ds, ones_count, new_ds)
            if len(new_ds) <= 1:
                ds = ds[-1:] if len(new_ds) == 0 else new_ds
                break
            else:
                ds = new_ds

        oxy = int(ds[0], 2)

        ds = digits.copy()
        for i in range(len(digits)):
            ones_count = count_ones(ds)
            new_ds = []
            for d in ds:
                if d[i] == ('0' if (len(ds) - ones_count[i]) <= ones_count[i] else '1'):
                    new_ds.append(d)
            # print(ds, ones_count, new_ds)

            if len(new_ds) <= 1:
                ds = ds[-1:] if len(new_ds) == 0 else new_ds
                break
            else:
                ds = new_ds

        co2 = int(ds[0], 2)

        print(oxy*co2)

    def day4(self):
        boards = []
        with open('inputs/day4') as f:
            nums = [int(x) for x in f.readline().strip('\n').split(',')]
            for l in f:
                if l.strip('\n') == '':
                    boards.append([])
                else:
                    boards[-1].append([int(x) for x in l.split()])
        # print(nums)
        # print(boards)

        bcombos = []
        for b in boards:
            bcombos.append([])
            for i in range(5):
                bcombos[-1].append(set(b[i]))
            for j in range(5):
                bcombos[-1].append(set([b[i][j] for i in range(5)]))

        for n in nums:
            new_bcombos = []
            for bcombo in bcombos:
                for c in bcombo:
                    if n in c:
                        c.remove(n)
                if any([len(c) == 0 for c in bcombo]):
                    if len(bcombos) == len(boards):
                        print('part1', sum([sum(list(c)) for c in bcombo])//2 * n)
                    elif len(bcombos) == 1:
                        print('part2', sum([sum(list(c)) for c in bcombo])//2 * n)
                else:
                    new_bcombos.append(bcombo)
            bcombos = new_bcombos

    def day5(self):
        line_start_end = []
        mx = 0
        with open('inputs/day5') as f:
            for l in f:
                l = l.strip("\n")
                line_start_end.append([(int(e.split(',')[0]), int(e.split(',')[1])) for e in l.split(' -> ')])
                mx = max(mx, max([max(xy) for xy in line_start_end[-1]]))
        # print(mx)
        # print(line_start_end)

        xlimit, ylimit = mx+1, mx+1
        landscape = [[0]*(ylimit+1) for x in range(xlimit+1)]
        cnt = 0
        for lse in line_start_end:
            s, e = lse
            sx, sy = s
            ex, ey = e
            # print(s, e, sx==ex, sy==ey)
            if sx == ex:
                for y in range(min(sy,ey), max(sy,ey)+1):
                    landscape[sx][y] += 1
                    if landscape[sx][y] == 2:
                        cnt += 1
            elif sy == ey:
                for x in range(min(sx,ex), max(sx,ex)+1):
                    landscape[x][sy] += 1
                    if landscape[x][sy] == 2:
                        cnt += 1
            else:
                steps = abs(sx-ex)
                xdir, ydir = (ex - sx)//abs(ex - sx), (ey - sy)//abs(ey - sy)
                for i in range(steps + 1):
                    landscape[sx + xdir*i][sy + ydir*i] += 1
                    if landscape[sx + xdir*i][sy + ydir*i] == 2:
                        cnt += 1
        # print('\n'.join([','.join([str(x) if x > 0 else '.' for x in l]) for l in landscape]))
        print(cnt)


    def day6(self):
        from collections import deque
        with open('inputs/day6') as f:
            nums = [int(x) for x in f.readline().split(',')]
        # print(nums)

        dp = {}
        def total_fishes(age, days_left):
            # print(age, days_left)
            if (age, days_left) in dp:
                return dp[(age, days_left)]

            if days_left <= 0:
                return 1

            if age == 0:
                dp[(age, days_left)] = total_fishes(6, days_left - 1) \
                                   + total_fishes(8, days_left - 1)
            else:
                dp[(age, days_left)] = total_fishes(age-1, days_left-1)

            # print(dp)
            return dp[(age, days_left)]

        cnt = 0
        days_left = 256
        # nums = [1]
        for age in nums:
            tf = total_fishes(age, days_left)
            print('---', age, tf)
            cnt += tf

        print(cnt)

    def day7(self):
        with open('inputs/day7') as f:
            ps = [int(x) for x in f.readline().split(',')]
        print(ps)

        cnts = [0] * (max(ps) + 1)
        for i in ps:
            cnts[i] += 1
        print(cnts)

        dp = [0]*(max(ps) + 1)
        for i in range(1, len(dp)):
            dp[i] = dp[i-1] + i
        print(dp)
        min_fuel = float('inf')
        for target in range(len(cnts)):
            fuel = 0
            for j in range(len(cnts)):
                fuel += cnts[j] * dp[abs(j-target)]

            min_fuel = min(min_fuel, fuel)
        print(min_fuel)

    def day8(self):
        samples = []
        with open('inputs/day8') as f:
            for l in f:
                input, output = l.strip('\n').split(" | ")
                input = input.split()
                output = output.split()
                samples.append((input, output))

        cnt = 0
        for s in samples:
            input, output = s
            for ss in output:
                if len(ss) in set([2,3,4,7]):
                    cnt += 1

        print(cnt)

        #  0000
        # 1    2
        # 1    2
        #  3333
        # 4    5
        # 4    5
        #  6666

        total = 0
        for s in samples:
            inputs, outputs = s
            lens = {}
            for inp in inputs:
                normalized = ''.join(sorted(inp))
                if len(inp) in lens:
                    lens[len(inp)].append(normalized)
                else:
                    lens[len(inp)] = [normalized]

            string_to_digit = {}
            for l, arr in lens.items():
                if l == 2:
                    string_to_digit[arr[0]] = 1
                elif l == 3:
                    string_to_digit[arr[0]] = 7
                elif l == 4:
                    string_to_digit[arr[0]] = 4
                elif l == 7:
                    string_to_digit[arr[0]] = 8

            # digit3: len(len_5_string intersect len_2_string) == 2
            digit3 = [s for s in lens[5] if len(set(s).intersection(set(lens[2][0]))) == 2][0]
            lens[5].remove(digit3)
            string_to_digit[digit3] = 3

            # 4: len_7_string diff digit3 diff len_4_string
            segment4 = set(lens[7][0]).difference(set(digit3)).difference(set(lens[4][0])).pop()

            # digit2: 4 in len_5_string
            digit2 = [s for s in lens[5] if segment4 in set(s)][0]
            lens[5].remove(digit2)
            string_to_digit[digit2] = 2

            # digit5: len_5_string not digit3 not digit2
            string_to_digit[lens[5][0]] = 5

            # digit9: 4 not in len_6_string
            digit9 = [s for s in lens[6] if segment4 not in s][0]
            lens[6].remove(digit9)
            string_to_digit[digit9] = 9

            # digit0: (len_6_string intersect len_2_string) == 2
            digit0 = [s for s in lens[6] if len(set(s).intersection(set(lens[2][0]))) == 2][0]
            lens[6].remove(digit0)
            string_to_digit[digit0] = 0

            # digit6: len_6_string not digit9 not digit0
            string_to_digit[lens[6][0]] = 6

            print(string_to_digit, len(string_to_digit))

            # print(outputs)
            for j in range(len(outputs)):
                total += string_to_digit[''.join(sorted(outputs[j]))] * 10 ** (len(outputs) - j - 1)
            # print(total)
        print(total)

    def day9(self):
        m = []
        with open('inputs/day9') as f:
            for l in f:
                m.append([int(c) for c in l.strip('\n')])

        risk = 0
        lx,ly = len(m), len(m[0])
        low_points = []
        for i in range(lx):
            for j in range(ly):
                u = m[i-1][j] if i-1 >= 0 else float('inf')
                d = m[i+1][j] if i+1 < lx else float('inf')
                l = m[i][j-1] if j-1 >= 0 else float('inf')
                r = m[i][j+1] if j+1 < ly else float('inf')
                if m[i][j] < u and m[i][j] < d and m[i][j] < l and m[i][j] < r:
                    risk += 1 + m[i][j]
                    low_points.append((i,j))

        print(risk)

        sizes = []
        for i,j in low_points[:]:
            size = 0
            q = deque([(i,j)])
            visited = set([])
            while q:
                x,y = q.popleft()
                print(x,y)
                size += 1
                for dx, dy in [(-1,0), (1,0), (0,-1),(0,1)]:
                    if 0 <= x+dx < lx and 0 <= y+dy < ly and m[x][y] < m[x+dx][y+dy] < 9 and (x+dx,y+dy) not in visited:
                        print('---', x+dx, y+dy)
                        visited.add((x+dx, y+dy))
                        q.append((x+dx, y+dy))

            sizes.append(size)

        sizes.sort()
        print(sizes[-1]*sizes[-2]*sizes[-3])


    def day10(self):
        with open('inputs/day10') as f:
            lines = [l.strip('\n') for l in f]

        m = {'{':'}','[':']','<':'>','(':')'}
        pts = {')':3,']':57,'>':25137,'}':1197}
        rm = {v:k for k,v in m.items()}
        p = 0
        incomplete = []
        for l in lines:
            h = deque([])
            broken = False
            for c in l:
                if c in m:
                    h.append(c)
                elif rm[c] == h[-1]:
                    h.pop()
                else:
                    p += pts[c]
                    broken = True
                    break

            if not broken:
                incomplete.append(l)

        print(p)
        # print('\n'.join(incomplete))

        pts = {')':1, ']':2, '}':3, '>':4 }
        total_score = []
        for l in incomplete:
            h = deque([])
            for c in l:
                if c in m:
                    h.append(c)
                elif rm[c] == h[-1]:
                    h.pop()
                else:
                    raise Exception("should not get here")

            score = 0
            while h:
                score = 5 * score + pts[m[h.pop()]]
            total_score.append(score)

        print(sorted(total_score)[len(total_score)//2])


    def day11(self):
        m = []
        with open('inputs/day11') as f:
            m = [[int(c) for c in l.strip('\n')] for l in f]

        print(m)

        # all i,j +1
        # any 9 's neighbors  +1 repeat for all >9s
        # record number of 9s, set all 9s to 0
        steps = 1000
        lx,ly = len(m), len(m[0])
        neighbors = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        total_flashes = 0
        for step in range(1, steps+1):
            q = deque()
            for i in range(lx):
                for j in range(ly):
                    q.append((i,j))

            flashed = [[False]*ly for j in range(ly)]
            flashes = 0
            while q:
                i,j = q.popleft()
                m[i][j] += 1
                if m[i][j] > 9 and not flashed[i][j]:
                    flashed[i][j] = True
                    flashes += 1
                    for di, dj in neighbors:
                        if 0 <= i + di < lx and 0 <= j + dj < ly:
                            q.append((i+di, j+dj))
            # print('\n'.join([','.join([str(i) for i in l]) for l in m]))
            for i in range(lx):
                for j in range(ly):
                    m[i][j] = 0 if m[i][j] > 9 else m[i][j]


            total_flashes += flashes
            print('\n'.join([''.join(['0' if b else '.' for b in l]) for l in flashed]))
            # print('\n'.join([','.join([str(i) for i in l]) for l in m]))
            print('-----------------', f'{step}', f'{flashes}', f'{total_flashes}')

            if flashes == lx*ly:
                break

        print(total_flashes)


    def day12(self):
        edges = []
        with open('inputs/day12') as f:
            for l in f:
                s, e = l.strip('\n').split('-')
                edges.append((s, e))
                edges.append((e, s))

        print(edges)
        neighbors = {}
        for s, e in edges:
            if s in neighbors:
                neighbors[s].add(e)
            else:
                neighbors[s] = set([e])

        print(neighbors)

        q = deque([('start', {'start'})])
        paths = 0
        while q:
            cave, visited = q.popleft()
            ns = neighbors[cave]
            for n in ns:
                if n == 'end':
                    # print('-- end reached through', new_visited)
                    paths += 1
                elif n.isupper() or (n.islower() and n not in visited):
                    new_visited = visited.copy()
                    if n.islower():
                        new_visited.add(n)
                    q.append((n, new_visited))
                    # print(cave, n, new_visited)


        print('part1', paths)

        q = deque([('start', {'start': 1})])
        paths = 0
        while q:
            cave, visited = q.popleft()
            ns = neighbors[cave]
            for n in ns:
                if n == 'end':
                    print('-- end reached through', visited)
                    paths += 1
                elif n != 'start' and (n.isupper() or (n.islower() and visited.get(n, 0) < 2)):
                    new_visited = visited.copy()
                    new_visited[n] = new_visited.get(n, 0) + 1
                    # print('---------', new_visited, len([3 for k, v in new_visited.items() if k.islower() and v >= 2]))
                    if len([3 for k, v in new_visited.items() if k.islower() and v >= 2]) <= 1:
                        # print(cave, n, new_visited)
                        q.append((n, new_visited))

        print('part2', paths)


    def day13(self):
        pts = []
        folds = []
        with open('inputs/day13') as f:
            for l in f:
                l = l.strip('\n')
                if ',' in l:
                    x,y = [int(x) for x in l.split(',')]
                    pts.append((x,y))
                elif 'fold' in l:
                    dim, pos = l.replace("fold along ", "").split('=')
                    folds.append((dim, int(pos)))

        print(pts, folds)

        size_x, size_y = max([x for x,y in pts]) + 1, max([y for x,y in pts]) + 1
        for fi in range(len(folds)):
            dim, pos = folds[fi]
            if dim == 'x':
                size_x = pos
            elif dim == 'y':
                size_y = pos

            for i in range(len(pts)):
                x, y = pts[i]
                pts[i] = (2*pos - x if dim == 'x' and x > pos else x, 2*pos - y if dim == 'y' and y > pos else y)

            pts = [(x,y) for x,y in pts if x < size_x and y < size_y]
            print(f'{len(set(pts))} points after {fi+1} fold')

        m = [['.']*size_x for i in range(size_y)]
        for x, y in pts:
            m[y][x] = '#'

        print(pts, len(set(pts)), len(pts), size_x, size_y)
        print('\n'.join([''.join(l) for l in m]))
        print('\n')


    def day14(self):
        with open('inputs/day14') as f:
            t = f.readline().strip('\n')
            f.readline()
            m = {l.strip('\n').split(' -> ')[0]: l.strip('\n').split(' -> ')[1] for l in f}

        print(t,m)
        steps = 40
        dp = {}
        def insert(t, steps_left):
            if (t, steps_left) in dp:
                return dp[(t, steps_left)]

            if steps_left <= 0:
                return {}

            new_c = m[t]
            cnts = {}
            cnts[new_c] = cnts.get(new_c, 0) + 1

            for ch,c in insert(''.join(t[0]+new_c), steps_left-1).items():
                cnts[ch] = cnts.get(ch, 0) + c

            for ch,c in insert(''.join(new_c + t[1:]), steps_left-1).items():
                cnts[ch] = cnts.get(ch, 0) + c

            dp[(t, steps_left)] = cnts

            return cnts

        cnts = {}
        for c in t:
            cnts[c] = cnts.get(c, 0) + 1
        for ci in range(len(t)-1):
            for ch, c in insert(''.join(t[ci:ci+2]), steps).items():
                cnts[ch] = cnts.get(ch, 0) + c

        print(cnts, dp)
        print(max(cnts.values()) - min(cnts.values()))

    def day15(self):
        with open('inputs/day15') as f:
            arr = [[int(x) for x in l.strip('\n')] for l in f]

        lx0, ly0 = len(arr), len(arr[0])
        print(lx0,ly0)


        def risk(x, y):
            ans = ((arr[x%lx0][y%ly0] + x//lx0 + y//ly0 - 1) % 9) + 1
            return ans

        multiplier = 5
        lx = lx0*multiplier
        ly = ly0*multiplier
        print(lx, ly)
        min_risk = {(0, 0): 0}
        visited = {(0, 0)}
        q = []
        heapq.heappush(q, (float('inf'), (0, 0)))
        while q:
            d, xy = heapq.heappop(q)
            x,y = xy
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                # print(x+dx, y+dy, lx, ly)
                if 0 <= (x + dx) < lx and 0 <= (y + dy) < ly: #and (x+dx,y+dy) != (0,0):
                    # print('---', min_risk.get((x+dx, y+dy), float('inf')))
                    # print(x,y, x+dx,y+dy)
                    min_risk[(x+dx, y+dy)] = min(min_risk.get((x+dx, y+dy), float('inf')), min_risk.get((x,y), float('inf')) + risk(x+dx, y+dy))
                    if (x + dx, y + dy) not in visited:
                        heapq.heappush(q, (min_risk[(x+dx,y+dy)], (x+dx, y+dy)))
                        visited.add((x+dx, y+dy))
            # print(visited)
            # print(min_risk.get((lx-1,ly-1), float('inf')))

        risks = [[0]*ly for i in range(lx)]
        for i in range(lx):
            for j in range(ly):
                risks[i][j] = min_risk[(i,j)]

        print('\n'.join([''.join([str(risk(i,j)) for j in range(ly)]) for i in range(lx)]))
        print('-------------------------')
        print('\n'.join([' '.join([str(c) for c in row]) for row in risks]))
        print('ans', min_risk[(lx-1,ly-1)])

    def day16(self):
        with open('inputs/day16') as f:
            hex = f.readline().strip('\n')

        def hex2bin(h):
            return [int(i) for i in bin(int(h, 16))[2:].zfill(4)]

        def bin2int(b):
            # print('bin2int', b)
            return int(''.join([str(x) for x in b]), 2)

        def literal(b, i):
            i_start = i
            acc = []
            while True:
                last_group = b[i] == 0
                # print('last_group', last_group)
                acc += b[i+1:i+5]
                i += 5
                if last_group:
                    break
            print('literal:', f"i_start:{i_start}", f"i={i}", f"literal:{bin2int(acc)}")
            return i, bin2int(acc)

        def op(b, i):
            length_type_id = b[i]
            i += 1
            v_sum = 0
            packet_vals = []
            if length_type_id == 0:
                length = bin2int(b[i:i+15])
                i += 15
                last_bit = i + length
                while i < last_bit:
                    i, v_subtotal, val = parse(b, i)
                    # print(i, v_subtotal, val)
                    v_sum += v_subtotal
                    packet_vals.append(val)
            else:
                length = bin2int(b[i:i+11])
                i += 11
                for j in range(length):
                    i, v_subtotal, val = parse(b, i)
                    v_sum += v_subtotal
                    packet_vals.append(val)
            # print('++op', i, length_type_id, length, f'v_sum:{v_sum}', f"packet_vals:{packet_vals}")

            return i, v_sum, packet_vals

        def parse(b, i):
            # print('parse', b[i:], len(b[i:]), i)
            v_sum = 0
            val = 0
            typ = None
            new_packet = True
            while True and i < 10000:
                if i+5 < len(b) and new_packet:
                    v = bin2int(b[i:i+3])
                    typ = bin2int(b[i+3:i+6])
                    print(f"version {v}, type {typ}")
                    v_sum += v
                    i += 6
                    new_packet = False
                elif typ == 4:
                    i, val = literal(b, i)
                    break
                elif typ != 4:
                    i, v_subtotal, packet_vals = op(b, i)
                    typ_to_op = {0:'sum', 1:'product', 2:'min', 3:'max', 5:'gt', 6:'lt', 7:'eq'}
                    if typ == 0:
                        val = sum(packet_vals)
                    elif typ == 1:
                        from functools import reduce
                        val = reduce((lambda x, y: x * y), [1] + packet_vals)
                    elif typ == 2:
                        val = min(packet_vals)
                    elif typ == 3:
                        val = max(packet_vals)
                    elif typ == 5:
                        if len(packet_vals) != 2:
                            raise Exception(f"wrong packet_vals: {packet_vals}")
                        val = 1 if packet_vals[0] > packet_vals[1] else 0
                    elif typ == 6:
                        if len(packet_vals) != 2:
                            raise Exception(f"wrong packet_vals: {packet_vals}")
                        val = 1 if packet_vals[0] < packet_vals[1] else 0
                    elif typ == 7:
                        if len(packet_vals) != 2:
                            raise Exception(f"wrong packet_vals: {packet_vals}")
                        val = 1 if packet_vals[0] == packet_vals[1] else 0
                    print(f'----typ: {typ}-{typ_to_op[typ]} , packet_vals: {packet_vals}, val: {val}')
                    v_sum += v_subtotal
                    break
                else:
                    break
            return i, v_sum, val


        b = []
        for c in hex:
            b += hex2bin(c)
        print(b, len(b))
        i, v_total, val = parse(b, 0)

        print('part1', v_total)
        print('part2', val)

    def day17(self):

        with open('inputs/day17') as f:
            # target area: x = 236..262, y = -78..- 58
            import re
            pattern = r"target area: x=(.*)\.\.(.*),\sy\=(.*)\.\.(.*)"
            match = re.match(pattern, f.readline())
            xmin, xmax, ymin, ymax = [int(x) for x in match.groups()]

        print(xmin, xmax, ymin, ymax)

        def step(vx0, vy0, xmin, xmax, ymin, ymax):
            print('---stepping for', vx0, vy0)
            step = 0
            max_step = 1000
            x, y = 0, 0
            vx, vy = vx0, vy0
            y_max = float('-inf')
            print(step, x, y, vx, vy)
            while step < max_step:
                x += vx
                y += vy
                y_max = max(y_max, y)
                if vx != 0:
                    vx += -1 if x > 0 else 1
                vy -= 1
                step += 1
                print(step, x, y, vx, vy)
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    return y_max
                elif x > xmax or y < ymin:
                    return float('-inf')

            return float('-inf')

        # vx0,vy0 = 20,-10
        # vx_max, vy_max = vx0, vy0
        vx0,vy0 = 0, ymin - 1
        vx_max, vy_max = xmax, 100
        max_y = float('-inf')
        num_within_target = 0
        for vx in range(vx0, vx_max + 1):
            for vy in range(vy0, vy_max + 1):
                curr_max_y = step(vx, vy, xmin, xmax, ymin, ymax)
                if curr_max_y != float('-inf'):
                    num_within_target += 1
                print('-- ', curr_max_y)
                max_y = max(max_y, curr_max_y)

        print('part1', max_y)
        print('part2', num_within_target)

    def day18(self):
        with open('inputs/day18') as f:
            lines = [x.strip('\n') for x in f.readlines()]

        def lvls_vals(line):
            lvls = []
            vals = []
            lvl = 0
            for c in line:
                if c == '[':
                    lvl += 1
                elif c == ']':
                    lvl -= 1
                elif c != ',':
                    lvls.append(lvl)
                    vals.append(int(c))
            return lvls, vals

        def add(lvls_left, vals_left, lvls_right, vals_right):
            return [l + 1 for l in lvls_left + lvls_right], vals_left + vals_right

        def explode(lvls, vals):
            l = len(lvls)
            new_lvls = []
            new_vals = []
            carry = 0
            for i in range(l):
                if new_lvls and new_lvls[-1] >= 5 and lvls[i] >= 5:
                    if len(new_vals) >= 2:
                        new_vals[-2] += new_vals[-1]
                    carry = vals[i]
                    new_lvls[-1] = lvls[i] - 1
                    new_vals[-1] = 0
                else:
                    new_lvls.append(lvls[i])
                    new_vals.append(vals[i] + carry)
                    carry = 0 if carry else carry

            return new_lvls, new_vals

        def split(lvls, vals):
            l = len(lvls)
            new_lvls = []
            new_vals = []
            applied = False
            for i in range(l):
                if vals[i] >= 10 and not applied:
                    new_lvls.append(lvls[i] + 1)
                    new_lvls.append(lvls[i] + 1)
                    new_vals.append(vals[i]//2)
                    new_vals.append((vals[i] + 1)//2 if vals[i] % 2 == 1 else vals[i]//2)
                    applied = True
                else:
                    new_lvls.append(lvls[i])
                    new_vals.append(vals[i])

            return new_lvls, new_vals

        def reduce(lvls, vals):
            while any([l >= 5 for l in lvls]) or any([v >= 10 for v in vals]):
                if any([l >= 5 for l in lvls]):
                    lvls, vals = explode(lvls, vals)
                else:
                    lvls, vals = split(lvls, vals)
                # print(lvls)
                # print(vals)
            return lvls, vals

        def magnitude(lvls, vals):
            for l in range(1, max(lvls)+1)[::-1]:
                # print('l=', l)
                new_lvls = []
                new_vals = []
                left = None
                for i in range(len(lvls)):
                    if lvls[i] == l:
                        if left is not None:
                            new_lvls.append(lvls[i] - 1)
                            new_vals.append(3*left + 2*vals[i])
                            left = None
                        else:
                            left = vals[i]
                    else:
                        new_lvls.append(lvls[i])
                        new_vals.append(vals[i])

                lvls = new_lvls
                vals = new_vals
                # print(lvls)
                # print(vals)

            return vals[0]

        lvls, vals = lvls_vals(lines[0])
        for line in lines[1:]:
            lvls, vals = reduce(*add(lvls, vals, *lvls_vals(line)))

        print(lvls)
        print(vals)
        print('part1', magnitude(lvls, vals))

        res = float('-inf')
        for i in range(len(lines)):
            for j in range(len(lines)):
                if i != j:
                    lvls_left, vals_left = lvls_vals(lines[i])
                    lvls_right, vals_right = lvls_vals(lines[j])
                    mag = magnitude(*reduce(*add(lvls_left, vals_left, lvls_right, vals_right)))
                    res = max(res, mag)

        print('part2', res)

    def day19(self):
        scanners = []
        beacons = []
        with open('inputs/day19') as f:
            for line in f:
                if 'scanner' in line:
                    if beacons:
                        scanners.append(beacons)
                        beacons = []
                elif line != '\n':
                    beacons.append([int(x) for x in line.strip('\n').split(',')])

        if beacons:
            scanners.append(beacons)
        # for i,s in enumerate(scanners):
        #     print(i,s)

        all_beacons = set([tuple(b) for b in scanners[0]])
        locs = [None]*len(scanners)
        locs[0] = [0,0,0]
        def pair(p, i):
            # print('pairing', p, i)
            beacons_p = scanners[p]
            beacons_i = scanners[i]
            dir_mapping = [-1,-1,-1]
            is_paired = False
            loc = [0,0,0]
            for dp in range(3):
                for di in range(3):
                    offsets_freq = {}
                    for bp in beacons_p:
                        for bi in beacons_i:
                            for facing in [1, -1]:
                                offset = bp[dp] - facing * bi[di]
                                offsets_freq[(offset, facing)] = offsets_freq.get((offset, facing), 0) + 1
                    mx_freq = max(offsets_freq.values())
                    if mx_freq >= 12:
                        # print(sorted(beacons_p))
                        # print(sorted(beacons_i))
                        is_paired = True
                        dir_mapping[dp] = di
                        offset, facing = [o for o,c in offsets_freq.items() if c == mx_freq][0]
                        for bi in beacons_i:
                            bi[di] = offset + facing * bi[di]
                        print(f'paired dir of scanner {i} relative to scanner {p}:', di, dp, offset, [(o,f) for o,f in offsets_freq.items() if f >= 10])
                        loc[di] = offset
                        break

            if is_paired:
                last_beacons_count = len(all_beacons)
                scanners[i] = [[bi[dir_mapping[0]], bi[dir_mapping[1]], bi[dir_mapping[2]]] for bi in beacons_i]
                loc0 = [loc[dir_mapping[0]], loc[dir_mapping[1]], loc[dir_mapping[2]]]
                locs[i] = loc0
                # print(f'{scanners[i]}')
                # print(f'{beacons_i}')
                all_beacons.update(set([tuple(s) for s in scanners[i]]))
                print(f"scanner {i} loc relative to 0: {loc0}")
                print('all_beacons count: ', len(all_beacons), f' added: {len(all_beacons) - last_beacons_count}')

            return is_paired


        paired = deque([0])
        while len(paired) < len(scanners):
            for i in range(len(scanners)):
                if i not in set(paired):
                    for p_idx in range(len(paired)):
                        p = paired[p_idx]
                        is_paired = pair(p, i)
                        if is_paired:
                            paired.append(i)
                            break

        print(sorted([l for l in locs if l]))
        print('part1', len(all_beacons))

        max_manhattan_dist = float('-inf')
        for i in range(len(locs)):
            for j in range(i + 1, len(locs)):
                manhattan_dist = sum([abs(locs[i][d]-locs[j][d]) for d in range(3)])
                max_manhattan_dist = max(max_manhattan_dist, manhattan_dist)
        print('part2', max_manhattan_dist)

    def day20(self):
        img = []
        with open('inputs/day20') as f:
            algo = f.readline().strip('\n')
            f.readline()
            for l in f.readlines():
                img.append(list(l.strip('\n')))

        print(algo)
        print(img)

        def str2int(s):
            bin = ''.join([('1' if c == '#' else '0') for c in s])

            return int(bin, 2)

        print(str2int('...#...#.'))

        padding = 100
        lx = len(img) + 2*padding
        ly = len(img[0]) + 2*padding
        padded_img = [['.']*ly for _ in range(padding)] \
                    + [['.']*padding + l + ['.']*padding for l in img] \
                    + [['.']*ly for _ in range(padding)]

        print('\n'.join([''.join(l) for l in padded_img]))

        steps = 50
        for s in range(steps):
            new_img = [l.copy() for l in padded_img]
            for i in range(0, lx):#lx):
                for j in range(0, ly):
                    idx_str = [algo[0]]*9
                    for di, dxdy in enumerate([(-1,-1), (-1, 0), (-1, 1), (0,-1), (0, 0), (0, 1), (1,-1), (1, 0), (1, 1)]):
                        dx, dy = dxdy
                        if 0 <= i + dx < lx and 0 <= j + dy < ly:
                            idx_str[di] = padded_img[i+dx][j+dy]
                    algo_idx = str2int(''.join(idx_str))
                    new_img[i][j] = algo[algo_idx]
                    # print(i,j, ''.join(idx_str), algo_idx, 'before', padded_img[i][j], 'after', new_img[i][j])
            padded_img = new_img

            print(f'after {s+1} steps')
            # print('\n'.join([''.join(l) for l in padded_img]))


        lit = 0
        for i in range(padding-steps, lx-(padding-steps)):
            for j in range(padding-steps, ly-(padding-steps)):
                lit += 1 if padded_img[i][j] == '#' else 0

        print('\n'.join([''.join(l) for l in padded_img]))
        print('part1', lit)

    def day21(self):
        with open('inputs/day21') as f:
            start_1 = int(f.readline().strip('\n').split(':')[1].strip(''))
            start_2 = int(f.readline().strip('\n').split(':')[1].strip(''))
        start_1-=1
        start_2-=1
        print(start_1, start_2)

        dice = list(range(1, 100+1))
        self.dice_idx = 0

        def roll_dice(n = 1):
            rolled = 0
            for _ in range(n):
                rolled += dice[self.dice_idx]
                self.dice_idx += 1
                self.dice_idx = self.dice_idx % len(dice)

            return rolled

        def jump_to(start, steps, board):
            return (start+steps) % len(board)

        score1 = 0
        score2 = 0
        max_score = 1000
        rolls = 3
        times_rolled = 0
        board = list(range(1, 11))
        s1 = start_1
        s2 = start_2
        while score1 < max_score and score2 < max_score:
            roll_sum = roll_dice(rolls)
            s1 = jump_to(s1, roll_sum, board)
            score1 += board[s1]
            times_rolled += rolls
            # print(f"score1: {score1}, roll_sum: {roll_sum}, s1: {board[s1]}")
            if score1 >= max_score:
                break

            roll_sum = roll_dice(rolls)
            s2 = jump_to(s2, roll_sum, board)
            score2 += board[s2]
            times_rolled += rolls
            # print(f"score2: {score2}, roll_sum: {roll_sum}, s2: {board[s2]}")
            if score2 >= max_score:
                break

        print('part1', times_rolled, min(score1, score2), times_rolled*min(score1, score2))

        def possible_rolls(dice, rolls_left, roll_sum, rolls_sum_freq):
            if rolls_left == 0:
                rolls_sum_freq[roll_sum] = rolls_sum_freq.get(roll_sum, 0) + 1
                return

            for d in dice:
                possible_rolls(dice, rolls_left - 1, roll_sum + d, rolls_sum_freq)

        rolls = 3
        dirac_dice = [1,2,3]
        rolls_sum_freq = {}
        possible_rolls(dirac_dice, rolls, 0, rolls_sum_freq)
        print(rolls_sum_freq)

        def probablisitic_game(s1, score1, s2, score2, player_to_start, board, max_score, dp):
            # print(dp)
            finger_print = (s1,score1,s2,score2, player_to_start)
            if finger_print in dp:
                return dp[finger_print]

            total_won1 = 0
            total_won2 = 0
            if player_to_start == 0:
                for roll_sum, freq in rolls_sum_freq.items():
                    new_s = jump_to(s1, roll_sum, board)
                    points = board[new_s]
                    if score1 + points >= max_score:
                        total_won1 += freq
                    else:
                        won1, won2 = probablisitic_game(new_s, score1 + points, s2, score2, 1, board, max_score, dp)
                        total_won1 += won1 * freq
                        total_won2 += won2 * freq

            elif player_to_start == 1:
                for roll_sum, freq in rolls_sum_freq.items():
                    new_s = jump_to(s2, roll_sum, board)
                    points = board[new_s]
                    if score2 + points >= max_score:
                        total_won2 += freq
                    else:
                        won1, won2 = probablisitic_game(s1, score1, new_s, score2 + points, 0, board, max_score, dp)
                        total_won1 += won1 * freq
                        total_won2 += won2 * freq

            dp[finger_print] = [total_won1, total_won2]

            return dp[finger_print]

        score1 = 0
        score2 = 0
        s1 = start_1
        s2 = start_2
        max_score = 21
        board = list(range(1, 11))
        dp = {}
        player_to_start = 0
        games_won1, games_won2 = probablisitic_game(s1, score1, s2, score2, player_to_start, board, max_score, dp)
        print('part2', games_won1, games_won2)
        # for i in range(11):
        #     print(jump_to(0, i, board), board[jump_to(0, i, board)])

    def day22(self):
        seq = []
        with open('inputs/day22') as f:
            # on x = -20..26, y = -36..17, z = -47..7
            for l in f:
                onoff, coords = l.strip('\n').split()
                x,y,z = coords.split(',')
                x_start, x_end = [int(a) for a in x.split('=')[1].split('..')]
                y_start, y_end = [int(a) for a in y.split('=')[1].split('..')]
                z_start, z_end = [int(a) for a in z.split('=')[1].split('..')]
                seq.append([[x_start, y_start, z_start], [x_end, y_end, z_end], onoff == 'on'])

        for s in seq:
            print(s)

        mn, mx = -50, 50
        ons = set([])
        for starts, ends, onoff in seq[:]:
            for i in range(max(mn, starts[0]), min(mx, ends[0]) + 1):
                for j in range(max(mn, starts[1]), min(mx, ends[1]) + 1):
                    for k in range(max(mn, starts[2]), min(mx, ends[2]) + 1):
                        ijk = (i, j, k)
                        if onoff and ijk not in ons:
                            ons.add(ijk)
                        elif not onoff and ijk in ons:
                            ons.remove(ijk)

        print('part1', len(ons))

        def overlaps_1d(start1, end1, start2, end2):
            return max(start1, start2) <= min(end1, end2)

        def overlaps(box1, box2):
            for i in range(len(box1[0])):
                if not overlaps_1d(box1[0][i], box1[1][i], box2[0][i], box2[1][i]):
                    return False
            return True

        def intersection_1d(start1,end1,start2,end2):
            return [max(start1, start2), min(end1, end2)]

        def intersection(box1, box2):
            intersect = ([0,0,0],[0,0,0])
            if overlaps(box1, box2):
                for i in range(3):
                    intersect[0][i], intersect[1][i] = intersection_1d(box1[0][i], box1[1][i], box2[0][i], box2[1][i])
                return intersect
            else:
                return None

        def size(box):
            if box is None:
                return 0
            res = 1
            for i in range(len(box[0])):
                res *= box[1][i] - box[0][i] + 1
            return res


        def combinations(start_i, values, combos):
            if start_i >= len(values):
                return

            new_combos = []
            for c in combos:
                n = c.copy()
                n.append(values[start_i])
                new_combos.append(n)

            combos += new_combos
            combinations(start_i + 1, values, combos)

        # inspired by https://www.reddit.com/r/adventofcode/comments/rlxhmg/comment/hqxczc4/?utm_source=share&utm_medium=web2x&context=3
        boxes = seq
        ons_count = 0
        all_intersections = []
        for i, box in enumerate(boxes):
            _, _, onoff = box
            new_interactions = []
            if onoff is True:
                new_interactions.append(box)
            for intersected in all_intersections:
                intersect = intersection(intersected, box)
                if intersect:
                    intersect = [intersect[0], intersect[1], not intersected[2]]
                    new_interactions.append(intersect)

            all_intersections += new_interactions

        print(len(all_intersections))
        for intersection in all_intersections:
            _, _, onoff = intersection
            ons_count += (1 if onoff else -1) * size(intersection)
        print('part2', ons_count)


    def day23(self):
        def get_board_from_file(path, additional_lines = []):
            with open(path) as f:
                lines = [l.strip('\n') for l in f.readlines()]
            lines = lines[:3] + additional_lines + lines[3:]

            hall_length = len(lines[0]) - 2
            room_length = (len(lines[0]) - 5)//2
            room_depth = len(lines) - 3
            halls = [BoardNode(i, 1, 'hall') for i in range(hall_length)]
            rooms = [BoardNode(i, room_depth, 'room') for i in range(room_length)]

            for i in range(len(halls)):
                if lines[1][i+1] != '.':
                    halls[i].append(Piece(lines[1][i+1]))

            for i in range(len(rooms)):
                for li in range(room_depth)[::-1]:
                    if lines[2 + li][3+2*i] != '.':
                        rooms[i].append(Piece(lines[2 + li][3+2*i]))
            return Board(rooms, halls)

        # print(board, board.is_final())
        # neighbors = list(board.neighbors())
        # print('board neighbors', '\n'.join([str(n) for n in neighbors]))
        # print('neighbors of ', neighbors[0], neighbors[0].energy_spent())
        # print('board neighbors', '\n'.join([str(n) + f'energy_spent: {n.energy_spent()}' for n in sorted(neighbors[0].neighbors(), key=lambda x: x.energy_spent())]))
        # print('neighbors of ', neighbors[0], neighbors[0].energy_spent())
        # print('neighbors of ', neighbors[0].neighbors()[0], neighbors[0].neighbors()[0].energy_spent())
        # print('board neighbors', '\n'.join([str(n) + f'energy_spent: {n.energy_spent()}' for n in sorted(neighbors[0].neighbors()[0].neighbors(), key=lambda x: x.energy_spent())]))

        def solve(board, final_board):
            # search for solution
            collision = 0
            heap = []
            heapq.heappush(heap, (float('inf'), 0, board))
            visited = {board: float('inf')}
            print('solving', board)
            while heap:
                energy_spent, moves, board = heapq.heappop(heap)
                # print(f"not visited neighbors of {board.finger_print}({board.energy_spent()}): {', '.join([f'{n.finger_print}({n.energy_spent()})' for n in board.neighbors() if n not in visited])}")
                # print(f'visiting: {board.finger_print}({board.energy_spent()})', 'visited count', len(visited), 'final' if board.is_final() else '', len(heap))
                if board.is_final():
                    print(f'found. spent {energy_spent} energy in {moves} moves')
                    # break

                neighbors = board.neighbors()
                for board_neighbor in neighbors:
                    if board_neighbor in visited:
                        collision += 1
                    if board_neighbor.energy_spent() < visited.get(board_neighbor, float('inf')):
                        # print(f'parent: {board.finger_print}({board.energy_spent()}), visiting: {board_neighbor.finger_print}({board_neighbor.energy_spent()})', 'visited count', len(visited), 'final' if board.is_final() else '')
                        heapq.heappush(heap, (board_neighbor.energy_spent(), moves + 1, board_neighbor))
                        visited[board_neighbor] = board_neighbor.energy_spent()

            print('collision', collision)
            return visited.get(final_board, float('inf'))

        final_board = get_board_from_file('inputs/day23_final')
        board = get_board_from_file('inputs/day23')
        print('part1', solve(board, final_board))

        additional_lines = ['  #D#C#B#A#  ', '  #D#B#A#C#  ']
        final_board_additional_lines = ['  #A#B#C#D#  ', '  #A#B#C#D#  ']
        # additional_lines = []
        board = get_board_from_file('inputs/day23', additional_lines)
        # board = get_board_from_file('inputs/day23_test4_part2', [])
        final_board = get_board_from_file('inputs/day23_final', final_board_additional_lines)
        print('\n'.join([str(r) for r in board.halls]))
        print('\n'.join([str(r) for r in board.rooms]))
        print('finger_print: ', board.finger_print, 'state: ', board.state())
        print(final_board.finger_print, final_board.is_final())
        print('part2', solve(board, final_board))

    def day24(self):
        def get_commands(path):
            with open(path) as f:
                commands = [l.strip('\n') for l in f.readlines()]
            return commands

        def run_program(inputs, commands, initial_state = {}, states_cache = {}):
            if initial_state:
                vars = initial_state
            else:
                vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

            input_i = 0
            for i, command in enumerate(commands):
                state = tuple([i] + list(vars.values()))
                if state in states_cache:
                    # print('cache hit')
                    return states_cache[state]

                op,v1,v2 = '', '', ''

                if command[:3] == 'inp':
                    op, v1 = command.split()
                else:
                    op, v1, v2 = command.split()
                    if v2 in vars:
                        v2 = vars[v2]
                    else:
                        v2 = int(v2)

                if op == 'inp':
                    vars[v1] = int(inputs[input_i])
                    input_i += 1
                elif op == 'add':
                    vars[v1] += v2
                elif op == 'mul':
                    vars[v1] *= v2
                elif op == 'div':
                    if v2 == 0:
                        raise Exception('dividing by zero')
                    vars[v1] //= v2
                elif op == 'mod':
                    if vars[v1] < 0 or v2 <= 0:
                        raise Exception(f'modding {vars[v1]} by {v2}')
                    vars[v1] = vars[v1] % v2
                elif op == 'eql':
                    vars[v1] = 1 if vars[v1] == v2 else 0

                # print(i, op, v1, v2, vars)
                states_cache[state] = vars

            return vars


        commands = get_commands('inputs/day24')
        ops_params = []
        command_partition_size = 18
        for i in range(14):
            params = []
            for offset in [4,5,15]:
                _, _, p1 = commands[offset + i* command_partition_size].split()
                p1 = int(p1)
                params.append(p1)
            ops_params.append(params)

        print(ops_params)

        def op(w, z, p1, p2, p3):
            e = ((((z % 26) + p2) == w) == 0)
            return ((z//p1) * ((25*e) + 1)) + ((w+p3)*e)

        # (((z % 26) + p2) == w) has to be zero?
        # ((z % 26) + p2) != w
        # w != [0-26] + p2

        def run_program2(ws, _start_op_i, _end_op_i, _zero_states, _zo=0, _state_cache={}):
            _z = _zo
            for _i in range(_start_op_i, _end_op_i, len(ops_params)):
                ops_param = ops_params[_i]
                _w = int(ws[_i])

                p1,p2,p3 = ops_param
                _e = ((((_z % 26) + p2) == w) == 0)
                _z = ((_z // p1) * ((25 * _e) + 1)) + ((_w + p3) * _e)

            return _z


        max_model_number = 99999999999999
        max_model_number_str = str(max_model_number)
        start_op_i = 0
        stop_op_i = 14
        zo_set = {0: ""}
        forward_zero_states = defaultdict(dict)
        for op_i in range(14)[0:stop_op_i]:
            new_zo_set = {}
            for i, kv in enumerate(zo_set.items()):
                zo, largest_w = kv
                for w in range(1, 10):
                    ws = largest_w + str(w) + max_model_number_str[op_i + 1:]
                    if i % 1000000 == 0:
                        print(f'validating w:{w}, i:{i}')
                    z = run_program2(ws, op_i, op_i+1, {}, zo, {})
                    new_zo_set[z] = max(new_zo_set.get(z, ""), largest_w + str(w))
                    if z == 0:
                        print(ws)

            forward_zero_states[op_i] = new_zo_set
            zo_set = new_zo_set
            print('op_i', op_i, 'zo_set_length', len(zo_set))

        print('part1', forward_zero_states[stop_op_i-1][0])

        max_model_number = 99999999999999
        max_model_number_str = str(max_model_number)
        start_op_i = 0
        stop_op_i = 14
        zo_set = {0: ""}
        forward_zero_states = defaultdict(dict)
        for op_i in range(14)[0:stop_op_i]:
            new_zo_set = {}
            for i, kv in enumerate(zo_set.items()):
                zo, smallest_w = kv
                for w in range(1, 10):
                    ws = smallest_w + str(w) + max_model_number_str[op_i + 1:]
                    if i % 1000000 == 0:
                        print(f'validating w:{w}, i:{i}')
                    z = run_program2(ws, op_i, op_i + 1, {}, zo, {})
                    new_zo_set[z] = min(new_zo_set.get(z, max_model_number_str), smallest_w + str(w))
                    if z == 0:
                        print(ws)

            forward_zero_states[op_i] = new_zo_set
            zo_set = new_zo_set
            print('op_i', op_i, 'zo_set_length', len(zo_set))
            # print(zo_set)
        print('part2', forward_zero_states[stop_op_i-1][0])

    def day25(self):
        with open('inputs/day25') as f:
            m = [list(l.strip('\n')) for l in f]

        def print_map(m):
            print('\n'.join([''.join(l) for l in m]))

        print_map(m)

        steps = 1000
        lx, ly = len(m), len(m[0])
        for s in range(1, steps + 1):
            moved = 0
            new_map = [row.copy() for row in m]
            for i, row in enumerate(m):
                for j, c in enumerate(row):
                    # print(i,j,c)
                    if c == '>' and m[i][(j+1) % ly] == '.':
                        new_map[i][j] = '.'
                        new_map[i][(j+1) % ly] = '>'
                        moved += 1
            m = new_map
            # print('--------------------------')
            # print_map(m)

            new_map = [row.copy() for row in m]
            for i, row in enumerate(m):
                for j, c in enumerate(row):
                    if c == 'v' and m[(i+1)%lx][j] == '.':
                        new_map[i][j] = '.'
                        new_map[(i + 1) % lx][j] = 'v'
                        moved += 1
            m = new_map
            print(s, '--------------------------')
            print_map(m)

            if moved == 0:
                print(s)
                break






class Board:
    def __init__(self, rooms, halls):
        self.rooms = rooms
        self.halls = halls
        hall_length = len(self.halls)
        for i, h in enumerate(self.halls):
            if 0 <= i - 1:
                h.neighbors.add(halls[i-1])
            if i + 1 < hall_length:
                h.neighbors.add(halls[i+1])
            if 2 <= i < hall_length - 2 and i % 2 == 0:
                h.neighbors.add(rooms[i//2-1])
        for i, r in enumerate(self.rooms):
            r.neighbors.add(halls[2+i*2])

        for i in range(len(self.halls)):
            if 2 <= i < len(self.halls) - 2 and i % 2 == 0:
                halls[i].can_stop_at = False

    @property
    def finger_print(self):
        room_depth = self.rooms[0].stack_limit
        return f"{''.join([h.stack[-1].id if h.stack else ('_' if 2 <= i < len(self.halls) - 2 and i % 2 == 0 else '.') for i,h in enumerate(self.halls)])}|" + \
               '|'.join([f"{''.join([r.stack[-depth + room_depth - len(r.stack)].id if (len(r.stack) >= room_depth-depth+1) else '.' for r in self.rooms])}" for depth in range(1, room_depth+1)])

    def is_final(self):
        species = string.ascii_uppercase
        for i, r in enumerate(self.rooms):
            if len(r.stack) < r.stack_limit:
                return False
            for s in r.stack:
                if s.id != species[i]:
                    return False
        return True

    def energy_spent(self):
        # print(['  '.join([f'{p.id} spent {p.energy_spent}' for p in n.stack]) for n in self.rooms])
        # print(['  '.join([f'{p.id} spent {p.energy_spent}' for p in n.stack]) for n in self.halls])
        return sum([sum([p.moves*p.energy() for p in n.stack]) for n in (self.rooms + self.halls)])

    def total_moves(self):
        return sum([sum([p.moves for p in n.stack]) for n in (self.rooms + self.halls)])

    def neighbors(self):
        res = []
        # room to hall
        for i, root in enumerate(self.rooms + self.halls):
            if not root.peek():
                continue
            if root.type == 'room' and (all([p.species_id == root.idx for p in root.stack]) or len(root.stack) == 1 and root.stack[-1].species_id == root.idx):
                continue
            root_piece = root.peek()
            if root_piece.moved:
                continue

            q = deque([(root, 0)])
            visited = {root.name}
            while q:
                destination, moves = q.pop()
                # add as destination if its a valid move
                # rule1: no final destination on h2, h4, h6, h8, node.can_stop_at = False
                # rule2: a piece can only enter a room that is occupied by same species
                # rule3: cannot move from hall to hall, only room -> hall or hall -> room
                # print(root_piece.id, destination.name, moves)
                if destination.can_stop_at \
                        and destination != root \
                        and (root.type == 'room' or root.type == 'hall' and destination.type != 'hall') \
                        and (destination.type == 'hall' or destination.type == 'room' and root_piece.species_id == destination.idx and all([p.species_id == root_piece.species_id for p in self.rooms[destination.idx].stack])):
                    new_board = copy(self)
                    piece = new_board.rooms[root.idx].pop() if root.type == 'room' else new_board.halls[root.idx].pop()
                    piece_previous_energy_spent = piece.energy_spent()
                    piece.moves += moves + \
                                   (root.stack_limit - len(root.stack) if root.type == 'room' else 0) + \
                                   ((destination.stack_limit - len(destination.stack) - 1) if destination.type == 'room' else 0)
                    # print('adding moves', f"current moves: {piece_previous_energy_spent}", f"new energy_spent: {piece.energy_spent()}")

                    if destination.type == 'room':
                        piece.moved = True

                    if destination.type == 'hall':
                        new_board.halls[destination.idx].append(piece)
                    else:
                        new_board.rooms[destination.idx].append(piece)

                    # print(f'{piece.id} with {piece.energy_spent() - piece_previous_energy_spent}, moves: {piece.moves}, energy_spent is going from {root.name} to {destination.name}, visited:{visited}')
                    if new_board.finger_print == 'B._._._._B.|AD..|CCDA':
                        print(new_board)

                    res.append(new_board)

                for board_node_neighbor in destination.neighbors:
                    if board_node_neighbor.name not in visited and not board_node_neighbor.is_stack_full: # stops travering once a node in the path is is_occupied
                        # print(f'adding neighbor of {board_node}: ', board_node_neighbor, board_node_neighbor.is_stack_full)
                        q.append((board_node_neighbor, moves + 1))
                        visited.add(board_node_neighbor.name)

        return res

    def state(self):
        return self.finger_print[len(self.halls)+1:]

    def __copy__(self):
        return Board([copy(r) for r in self.rooms], [copy(h) for h in self.halls])

    def __eq__(self, other):
        return self.finger_print == other.finger_print

    def __hash__(self):
        return hash(self.finger_print[:])

    def __lt__(self, other):
        return -1

    def __str__(self):
        return self.finger_print
        '''
        return f"""
            #############
            #{''.join([h.stack[-1].id if h.stack else '.' for h in self.halls])}#
            ###{'#'.join([r.stack[-1].id if len(r.stack) >= 2 else ' ' for r in self.rooms])}###
              #{'#'.join([r.stack[0].id if len(r.stack) >= 1 else ' ' for r in self.rooms])}#
              #########
            """
        '''

class Piece:
    def __init__(self, id):
        self.id = id
        self.moves = 0
        self.moved = False
        self.species_id = {id: i for i,id in enumerate('ABCD')}[self.id]

    def energy(self):
        return {'A': 1, 'B': 10, 'C': 100, 'D': 1000}[self.id]

    def energy_spent(self):
        return self.energy() * self.moves

    def __str__(self):
        return f'Piece<id: {self.id}, energy_spent: {self.moves*self.energy()}>'

    def __copy__(self):
        o = Piece(self.id)
        o.moves = self.moves
        return o

class BoardNode:
    def __init__(self, idx, stack_limit, typ):
        self.idx = idx
        self.stack = deque([])
        self.neighbors = set([])
        self.can_stop_at = True
        self.stack_limit = stack_limit
        self.type = typ

    def append(self, piece):
        if not self.is_stack_full:
            self.stack.append(piece)
            return piece
        else:
            return None

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            return None

    def peek(self):
        if self.stack:
            return self.stack[-1]
        else:
            return None

    @property
    def is_stack_full(self):
        return len(self.stack) >= self.stack_limit

    @property
    def is_room(self):
        return self.type == 'room'

    @property
    def is_hall(self):
        return self.type == 'hall'

    @property
    def name(self):
        return f"{self.type[0]}{self.idx}"

    def __str__(self):
        return f"BoardNode<id: {self.name}, can_stop_at: {self.can_stop_at}, stack: {[str(p) for p in self.stack]}, neighbors: {sorted([n.name for n in self.neighbors])}>"

    def __copy__(self):
        n = BoardNode(self.idx, self.stack_limit, self.type)
        n.stack = [copy(p) for p in self.stack]
        n.can_stop_at = self.can_stop_at
        return n

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __str__(self):
        return f'<{self.val}, left:{self.left}, right:{self.right}>'


if __name__ == '__main__':
    import sys
    # method_name = sys.argv[1]
    method_name = "day25"
    getattr(Solve(), method_name)()


