from util import read_input

lines = read_input("./inputs/day19")
# lines = read_input("./inputs/day19_test")

patterns = [p.strip() for p in lines[0].split(',')]
towels = lines[2:]

def part1(patterns, towels):
    def _rec(towel, patterns, idx, mem):
        if idx >= len(towel):
            return True
        # print(f"matching towel with {len(towel) - idx} left", idx, towel[idx:], 'with', patterns)
        if towel[idx:] in mem:
            return mem[towel[idx:]]

        for pattern in patterns:
            if towel[idx:idx+len(pattern)] == pattern:
                # print(f"Matched {pattern} at {idx}, {towel[idx:idx+len(pattern)]}")
                matched = _rec(towel, [p for p in patterns if len(p) <= len(towel) - idx - len(pattern)], idx+len(pattern), mem)
                mem[towel[idx:]] = matched
                if matched:
                    return True
                else:
                    continue

        return False

    matched = 0
    mem = {}
    for towel in towels[:]:
        _patterns = [p for p in patterns if p in towel]
        _patterns.sort(key=lambda x: len(x), reverse=True)
        # print('matching', towel, 'with', len(_patterns), 'patterns', _patterns)
        if _rec(towel, _patterns, 0, mem):
            matched += 1

    return matched


def part2(patterns, towels):
    def _rec(towel, patterns, idx, mem):
        if idx >= len(towel):
            return 1
        if towel[idx:] in mem:
            return mem[towel[idx:]]

        cnt = 0
        for pattern in patterns:
            if towel[idx:idx+len(pattern)] == pattern:
                sub_cnt = _rec(towel, [p for p in patterns if len(p) <= len(towel) - idx - len(pattern)], idx+len(pattern), mem)
                cnt += sub_cnt
        mem[towel[idx:]] = cnt

        return cnt

    matched = 0
    mem = {}
    for towel in towels[:]:
        _patterns = [p for p in patterns if p in towel]
        _patterns.sort(key=lambda x: len(x), reverse=True)
        # print('matching', towel, 'with', len(_patterns), 'patterns', _patterns)
        matched += _rec(towel, _patterns, 0, mem)

    return matched


print(part1(patterns, towels))
print(part2(patterns, towels))