def read_input(file):
    with open(f'{file}', 'r') as f:
        arr = [l.strip('\n') for l in f.readlines()]
    return arr

def print_matrix(matrix):
    for row in matrix:
        print(''.join(row))
    print('\n')
