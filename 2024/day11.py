from util import read_input

lines = read_input("./inputs/day11")
# lines = read_input("./inputs/day11_test")

nums = lines[0].split()

def part1(nums, blinks = 25):
    # 1 0 -> 1
    # 2 1000 -> 10 0
    # 3 x*2024
    for b in range(blinks):
        split = [None] * len(nums)
        for i in range(len(nums)):
            n = nums[i]
            if n == "0":
                nums[i] = "1"
            elif len(n) % 2 == 0:
                n = list(n)
                nums[i] = ''.join(n[:len(n)//2])
                split[i] = str(int(''.join(n[len(n)//2:])))
            else:
                nums[i] = str(int(n) * 2024)

        # combine nums and split
        new_nums = []
        for i in range(len(nums)):
            new_nums.append(nums[i])
            if split[i] is not None:
                new_nums.append(split[i])
        nums = new_nums
        # print(nums)

    return len(nums)


def part2(nums, blinks = 75):
    # recursive
    def _rec(n, cnt, blinks_left, mem):
        if (n, blinks_left) not in mem:
            if blinks_left == 0:
                mem[(n, blinks_left)] = 1
            else:
                if n == "0":
                    mem[(n, blinks_left)] = _rec("1", cnt, blinks_left - 1, mem)
                elif len(n) % 2 == 0:
                    mem[(n, blinks_left)] = _rec(n[:len(n)//2], cnt, blinks_left - 1, mem) + _rec(str(int(n[len(n)//2:])), cnt, blinks_left - 1, mem)
                else:
                    mem[(n, blinks_left)] =  _rec(str(int(n) * 2024), cnt, blinks_left - 1, mem)

        # print(mem)
        return mem[(n, blinks_left)]

    res = 0
    mem = {}
    for i in range(len(nums)):
        res += _rec(nums[i], 0, blinks, mem)

    return res

print(part1(nums, 25))
print(part2(nums, 75))
