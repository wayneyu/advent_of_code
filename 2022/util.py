def read_input(file):
    with open(f'{file}', 'r') as f:
        arr = [l.strip('\n') for l in f.readlines()]
    return arr
