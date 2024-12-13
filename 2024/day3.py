from util import read_input

lines = read_input("./inputs/day3")

def find_muls(l, consider_do_dont = False):
    digits = '1234567890'
    is_open = False
    do = True
    last_digit = ""
    muls = []
    for i in range(len(l)):
        c = l[i]
        if c == '(' and l[i-3:i] == 'mul':
            is_open = True
            if len(muls) % 2 != 0:
                muls.pop()
        elif c == ')':
            if consider_do_dont:
                if l[i-3:i] == 'do(':
                    do = True
                elif l[i-6:i] == "don't(":
                    do = False
            if last_digit:
                if not consider_do_dont or (consider_do_dont and do):
                    muls.append(int(last_digit))
            last_digit = ""
            is_open = False
        elif c == ',':
            if is_open:
                if last_digit:
                    if not consider_do_dont or (consider_do_dont and do):
                        if len(muls) % 2 == 0:
                            muls.append(int(last_digit))
                        else:
                            muls.pop()
            last_digit = ""
        elif is_open:
            if c in digits:
                last_digit += c
            else:
                last_digit = ""
                is_open = False

    sum = 0
    for i in range(len(muls)//2):
        sum += muls[2*i] * muls[2*i+1]
    return sum

print(find_muls(lines[0], False))
print(find_muls(lines[0], True))