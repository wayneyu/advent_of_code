from util import read_input
import re
from functools import reduce
from collections import defaultdict

lines = read_input("inputs/day11.txt")


class Monkey:

    def __init__(self, number, starting_items, operation, test):
        self.number = number
        self.starting_items = starting_items
        self.operation = operation
        self.test = test
        self.inspected = 0

    def __str__(self):
        return f"Monkey(operation: {self.operation}, test: {self.test}, items: {[str(item) for item in self.starting_items]})"


class Item:

    def __init__(self, value):
        self.value = value
        self.value_to_each_monkey = {}
        self.times_inspected_by_monkey = {}

    def set_value(self, value):
        self.value = value

    def inspect_for_n_rounds(self, monkeys, rounds, worry_factor):
        inspecting_monkey = [monkey for monkey in monkeys if self in monkey.starting_items][0]

        for m in monkeys:
            self.value_to_each_monkey[m] = self.value % m.test.modulo if worry_factor == 1 else self.value
            self.times_inspected_by_monkey[m] = 0

        for i in range(rounds):
            while True:
                # print(self.value, i, inspecting_monkey.number, self.value_to_each_monkey[inspecting_monkey])

                for m in monkeys:
                    if isinstance(inspecting_monkey.operation, Multiplication):
                        self.value_to_each_monkey[m] *= inspecting_monkey.operation.operator % m.test.modulo if worry_factor == 1 else inspecting_monkey.operation.operator
                    elif isinstance(inspecting_monkey.operation, Addition):
                        self.value_to_each_monkey[m] += inspecting_monkey.operation.operator % m.test.modulo if worry_factor == 1 else inspecting_monkey.operation.operator
                    elif isinstance(inspecting_monkey.operation, Squared):
                        self.value_to_each_monkey[m] *= self.value_to_each_monkey[m] % m.test.modulo if worry_factor == 1 else self.value_to_each_monkey[m]
                    self.value_to_each_monkey[m] //= worry_factor
                self.times_inspected_by_monkey[inspecting_monkey] += 1

                if self.value_to_each_monkey[inspecting_monkey] % inspecting_monkey.test.modulo == 0:
                    next_inspecting_monkey = monkeys[inspecting_monkey.test.if_true]
                else:
                    next_inspecting_monkey = monkeys[inspecting_monkey.test.if_false]

                if next_inspecting_monkey.number < inspecting_monkey.number:
                    inspecting_monkey = next_inspecting_monkey
                    break

                inspecting_monkey = next_inspecting_monkey

    def __str__(self):
        return f"Item(value: {self.value})"


class Operation:

    def __init__(self, operator):
        self.operator = operator

    def __str__(self):
        return f"{self.__class__.__name__}({self.operator})"


class Multiplication(Operation):

    def __init__(self, operator):
        super().__init__(operator)


class Addition(Operation):

    def __init__(self, operator):
        super().__init__(operator)


class Squared(Operation):

    def __init__(self):
        super().__init__(None)


class Test:

    def __init__(self, modulo, if_true, if_false):
        self.modulo = modulo
        self.if_true = if_true
        self.if_false = if_false

    def __str__(self):
        return f"Test({self.modulo}, {self.if_true}, {self.if_false})"


def parse_monkeys():
    # Monkey 0:
    #   Starting items: 65, 58, 93, 57, 66
    #   Operation: new = old * 7
    #   Test: divisible by 19
    #     If true: throw to monkey 6
    #     If false: throw to monkey 4
    starting_items_regex = r"\s\sStarting items: (.*)"
    operation_regex = r"\s\sOperation: new = old\s([\+\-\*\/]{1})\s(\w+)"
    test_regex = r"\s\sTest: divisible by (\d+)"
    test_true_regex = r"\s\s\s\sIf true: throw to monkey (\d+)"
    test_false_regex = r"\s\s\s\sIf false: throw to monkey (\d+)"
    monkeys = []
    items = []
    monkey_idx, starting_items, operation, test = 0, None, None, None

    for l in lines:
        if l.startswith("  Starting items:"):
            match = re.match(starting_items_regex, l)
            starting_items = [Item(int(i)) for i in match.group(1).split(", ")]
            items += starting_items
        elif l.startswith("  Operation:"):
            match = re.match(operation_regex, l)
            op = match.group(1)
            if match.group(2) == "old":
                if op == "*":
                    operation = Squared()
                else:
                    raise NotImplementedError()
            else:
                v = int(match.group(2))
                if op == "+":
                    operation = Addition(v)
                elif op == "*":
                    operation = Multiplication(v)
                else:
                    raise NotImplementedError()
        elif l.startswith("  Test"):
            match = re.match(test_regex, l)
            test_divisor = int(match.group(1))
        elif l.startswith("    If true:"):
            match = re.match(test_true_regex, l)
            test_true_result = int(match.group(1))
        elif l.startswith("    If false:"):
            match = re.match(test_false_regex, l)
            test_false_result = int(match.group(1))
            test = Test(test_divisor, test_true_result, test_false_result)
        elif not l:
            monkeys.append(Monkey(monkey_idx, starting_items, operation, test))
            monkey_idx += 1

    monkeys.append(Monkey(monkey_idx, starting_items, operation, test))

    return (items, monkeys)


def solution(rounds, worry_factor):
    items, monkeys = parse_monkeys()
    # print("\n".join([str(m) for m in monkeys]))
    # print("\n".join([str(item) for item in items]))
    total_times_inspected_by_monkey = defaultdict(int)
    for item in items[:]:
        item.inspect_for_n_rounds(monkeys, rounds, worry_factor)
        for monkey, inspected in item.times_inspected_by_monkey.items():
            total_times_inspected_by_monkey[monkey] += inspected
    return reduce(lambda x, y: x * y, sorted(total_times_inspected_by_monkey.values(), reverse=True)[:2], 1)


# part 1
print(solution(20, 3))

# part 2
print(solution(10000, 1))
