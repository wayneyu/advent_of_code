from util import read_input

lines = read_input("./inputs/day17")
# lines = read_input("./inputs/day17_test")

registers = [0, 0, 0]
program = []
for l in lines:
    if l.startswith("Register A:"):
        registers[0] = int(l.split(":")[1])
    elif l.startswith("Register B:"):
        registers[1] = int(l.split(":")[1])
    elif l.startswith("Register C:"):
        registers[2] = int(l.split(":")[1])
    elif l.startswith("Program:"):
        program = [int(a) for a in l.split(":")[1].split(',')]

print(registers)
print(program)
# 2,4,1,2,7,5,0,3,4,7,1,7,5,5,3,0
# 2,4
# a = a
# b = a%8
# c = c
# 1,2
# a = a
# b = (a%8) ^ 2
# c = c
# 7,5
# a = a
# b = (a%8) ^ 2
# c = a//(2**((a%8) ^ 2))
# 0,3
# a = a//8
# b = (a%8) ^ 2
# c = a//(2**((a%8) ^ 2))
# 4,7
# a = a//8
# b = ((a%8) ^ 2) ^ a//(2**((a%8) ^ 2))
# c = a//2**((a%8) ^ 2)
# 1,7
# a = a//8
# b = (((a%8) ^ 2) ^ a//2**((a%8) ^ 2)) ^ 7
# c = a//2**((a%8) ^ 2)
# 5,5
# output += ((((a%8) ^ 2) ^ a//2**((a%8) ^ 2)) ^ 7) % 8

# 2,4,1,2,7,5,0,3,4,7,1,7,5,5
# a = (a//8)//8
# b = ((((a//8)%8) ^ 2) ^ (a//8)//(2**(((a//8)%8) ^ 2)) ^ 7 ) % 8
# c = (a//8)//(2**(((a//8)%8) ^ 2))

def part1(registers, program, stop_at=None):

    def zero(operand):
        operand = registers[operand - 4] if 4 <= operand <= 6 else operand
        registers[0] = registers[0]//2**operand

    def one(operand):
        registers[1] = registers[1] ^ operand

    def two(operand):
        operand = registers[operand - 4] if 4 <= operand <= 6 else operand
        registers[1] = operand % 8

    def three(operand, p):
        if registers[0] == 0:
            return p + 1
        else:
            return operand

    def four(operand):
        registers[1] = registers[1] ^ registers[2]

    def five(operand, outputs):
        operand = registers[operand - 4] if 4 <= operand <= 6 else operand
        outputs.append(operand % 8)

    def six(operand):
        operand = registers[operand - 4] if 4 <= operand <= 6 else operand
        registers[1] = registers[0]//2**operand

    def seven(operand):
        operand = registers[operand - 4] if 4 <= operand <= 6 else operand
        registers[2] = registers[0]//2**operand

    def rec_run(registers, ops, operands, outputs, p):

        if p >= len(ops):
            return outputs

        op = ops[p]

        operand = operands[p]
        next_p = p + 1
        if op == 0:

            zero(operand)
        elif op == 1:
            one(operand)
        elif op == 2:
            two(operand)
        elif op == 3:
            next_p = three(operand, p)
        elif op == 4:
            four(operand)
        elif op == 5:
            five(operand, outputs)
        elif op == 6:
            six(operand)
        elif op == 7:
            seven(operand)

        if stop_at and len(outputs) == stop_at:
            return outputs
        else:
            return rec_run(registers, ops, operands, outputs, next_p)

    outputs = rec_run(registers, program[::2], program[1::2], [], 0)
    return outputs

def part2(program):
    res = []
    for exp in range(1, len(program)+1):
        for i in range(0, 8):
            a = i * 8**0 + sum([res[-k-1]*8**(k+1) for k in range(len(res))])
            outputs = part1([a, 0,0], program, {})
            # print('===>', [a,0,0], outputs)
            p = outputs[-exp]
            if p == program[-exp]:
                res.append(i)
                # print('verify   ', program)
                # print('verify', part1([sum([res[-k-1]*8**(k+1) for k in range(len(res))]), 0, 0], program, {}))
                break


    return sum([res[-k-1]*8**k for k in range(len(res))])


print(''.join([str(a) for a in part1(registers, program, {})]))
print(part2(program))
