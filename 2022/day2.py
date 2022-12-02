from util import read_input

lines = read_input("inputs/day2.txt")

opp_loses = {'A': 'Y', 'B': 'Z', 'C': 'X'}
opp_draws = {'A': 'X', 'B': 'Y', 'C': 'Z'}

# part 1
rsp_score = {'X': 1, 'Y': 2, 'Z': 3}
score = 0
for l in lines:
    opponent, me = l.split(" ")

    score += rsp_score[me]

    if me == opp_loses[opponent]:
        score += 6
    elif me == opp_draws[opponent]:
        score += 3

print(score)

# part 2
result_score = {'X': 0, 'Y': 3, 'Z': 6}
score = 0
for l in lines:
    opponent, result = l.split(" ")

    score += result_score[result]

    if result == 'Z':
        score += rsp_score[opp_loses[opponent]]
    elif result == 'Y':
        score += rsp_score[opp_draws[opponent]]
    else:
        rsp = set(list('XYZ'))
        rsp.remove(opp_loses[opponent])
        rsp.remove(opp_draws[opponent])
        score += rsp_score[list(rsp)[0]]

print(score)