from ftplib import all_errors

from util import read_input

lines = read_input("./inputs/day7")
# lines = read_input("./inputs/day7_test")

eqns = []
for line in lines:
    result, nums = line.split(": ")
    nums = [int(n) for n in nums.split(" ")]
    eqns.append((int(result), nums))

def part1(eqns):
    def _rec_calc(nums, start, curr_result, target, op):
        if start == len(nums):
            return curr_result == target

        return _rec_calc(nums, start + 1, (curr_result + nums[start]), target, op) or _rec_calc(nums, start + 1, (curr_result * nums[start]), target, op)

    sum = 0
    for (result, nums) in eqns:
        res = _rec_calc(nums, 1, nums[0], result, '+') or _rec_calc(nums, 1, nums[0], result, '*')
        # print(result, nums, res)
        if res:
            sum += result
    return sum

def part2(eqns):
    def _rec_calc(nums, start, curr_result, target, op):
        if start == len(nums):
            return curr_result == target
        return _rec_calc(nums, start + 1, int(str(curr_result) + str(nums[start])), target, op) or _rec_calc(nums, start + 1, (curr_result + nums[start]), target, op) or _rec_calc(nums, start + 1, (curr_result * nums[start]), target, op)

    sum = 0
    for (result, nums) in eqns:
        res = _rec_calc(nums, 1, nums[0], result, '+') or _rec_calc(nums, 1, nums[0], result, '*')
        # print(result, nums, res)
        if res:
            sum += result
    return sum

print(part1(eqns))
print(part2(eqns))



