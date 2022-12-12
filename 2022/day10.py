from util import read_input

lines = read_input("inputs/day10.txt")


value_after_cycle = [1]
for move in lines:
    args = move.split(' ')
    if len(args) == 1 and args[0] == 'noop':
        value_after_cycle.append(1 if not value_after_cycle else value_after_cycle[-1])
    elif len(args) == 2 and args[0] == "addx":
        v = int(args[1])
        value_after_cycle.append(value_after_cycle[-1])
        value_after_cycle.append(value_after_cycle[-1] + v)

# part 1
print(sum([(i+1) * v for i, v in enumerate(value_after_cycle) if i+1 in range(20, len(value_after_cycle), 40)]))


# part 2
screen_width, screen_height = 40, 6
x = 1
pixels = []  # True for lit, False for dark pixel
for cycle, x in enumerate(value_after_cycle):
    drawing_pos = cycle % screen_width
    sprite = [x-1, x, x+1]
    pixels.append(drawing_pos in sprite)

screen = ["".join(['#' if p else '.' for p in pixels[start:start + screen_width]]) for start in range(0, screen_height*screen_width, screen_width)]
print("\n".join(screen))






