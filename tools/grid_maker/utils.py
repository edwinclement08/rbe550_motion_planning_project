from pprint import pprint
import sys
print(sys.argv)
ROW=10
COL=10
prefix = 'a'

i = 5
j = 9
r = 6

# print( (i * COL + j) * 100 + r)

action_map = {
        '0': 'straight',
        '1': 'left',
        '2': 'right',
        '3': 'halt'
}

def get_state(state):

    to_s = lambda prefix, i, j, r: f'{prefix}{i}{j}{str(r).rjust(2,"_")}'
    states =   ' '.join([' '.join([' '.join([to_s(prefix,i,j,rot) for rot in range(8)]) for j in range(COL)]) for i in  range(ROW)]) 
    return (states.split(' ')[state])


def neighbour_cells( i, j, rot):
    cells = []
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            ni, nj = [i + dy, j + dx]
            if ni < 0 or nj < 0 or ni >= 10 or nj >= 10:
                continue
            cells.append([ni, nj])
    return cells

# lines = open('temp.log').readlines()
# states = lines[::2]
# states = [get_state(int(g.split('s')[2].split(']')[0])) for g in states ]

# actions = lines[1::2]
# actions = [a.split('=')[1].split(':')[0].strip() for a in actions ]  
# actions = [action_map[a] for a in actions ]  


# pairs = [x for x in zip(states,actions)]
# pprint(pairs)


print(get_state(152))