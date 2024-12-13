from util import read_input, print_matrix

lines = read_input("./inputs/day4")

puzzle = [list(l) for l in lines]

def part1(puzzle):
    m, n = len(puzzle), len(puzzle[0])
    xmas = 'XMAS'
    cnt = 0
    marker = [['.' for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            c = puzzle[i][j]
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1,1), (-1,1), (1,-1), (-1,-1)]
            if c == 'X':
                for dir in dirs:
                    str = ''
                    for k in range(4):
                        x, y = i + k*dir[0], j + k*dir[1]
                        if 0 <= x < m and 0 <= y < n:
                            str += puzzle[i + k*dir[0]][j + k*dir[1]]
                    if str == xmas:
                        for k in range(4):
                            x, y = i + k*dir[0], j + k*dir[1]
                            marker[x][y] = 'X'
                        cnt +=1

    # print_matrix(puzzle)
    # print('')
    # print_matrix(marker)
    return cnt

def part2(puzzle):
    m, n = len(puzzle), len(puzzle[0])
    cnt = 0
    def is_cross_mas(mat):
        if mat[1][1] == 'A':
            if mat[0][0] != mat[2][2] and mat[0][2] != mat[2][0] and ''.join(sorted([mat[0][0], mat[0][2], mat[2][0], mat[2][2]])) == 'MMSS':
                return True
        return False

    for i in range(1,m-1):
        for j in range(1,n-1):
            if puzzle[i][j] == 'A':
                mat = [[puzzle[i+di][j+dj] for di in range(-1,2)] for dj in range(-1,2)]
                if is_cross_mas(mat):
                    cnt += 1

    return cnt

print(part1(puzzle))
print(part2(puzzle))
