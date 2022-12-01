def read_input(file):
    with open(f'{file}', 'r') as f:
        arr = [l.strip() for l in f.readlines()]
    return arr
