from pprint import pprint
import math
from grid_world_maker import GridWorldMaker
import sys

if __name__ == '__main__':

    COL=10 # hard coded, due to change in state naming logic change from math to string
    ROW=10
    obs_prob = [[0 for i in range(COL)] for k in range(ROW)]

    for y in range(ROW):
        for x in range(COL):
            pass

    
    board = [[-1 for i in range(COL)] for k in range(ROW)]
    GOAL_ROW = 9
    GOAL_COL = 9
    board[GOAL_ROW][GOAL_COL]  = 40
    print("reward")
    pprint(board)

    prefix = 'a'
    # prefix = ''

    # states_without_rot = ['a'+str(i) for i in  range(COL*ROW)]
    # print(states_without_rot)
    # states = ' '.join([' '.join([state + str(rot).ljust(2, '0') for rot in range(8)]) for state in states_without_rot])
    # print(definition['states'].split(' ')[233])

    to_s = lambda prefix, i, j, r: f'{prefix}{i}{j}{str(r).rjust(2,"_")}'
    # to_s = lambda prefix,i,j,rot:prefix+str((i*COL+j)*100 + rot)

    definition = {
        'discount': 0.90,
        'values': 'reward',
        'states':  ' '.join([' '.join([' '.join([to_s(prefix,i,j,rot) for rot in range(8)]) for j in range(COL)]) for i in  range(ROW)]) ,
        'actions': ' '.join(['straight', 'left', 'right', 'halt']),
        'observations':  ' '.join([' '.join([' '.join([to_s(prefix,i,j,rot) for rot in range(8)]) for j in range(COL)]) for i in  range(ROW)]) + ' null' ,
        'start': prefix + '00_0',
        'board': board,
        'action_map': lambda action, i,j,theta : ({
            'straight': (i - round(math.sin(theta)), j + round(math.cos(theta)), theta),
            'left': (i - round(math.sin(theta + math.pi/4)), j + round(math.cos(theta + math.pi/4)), (theta + math.pi/4)%(2* math.pi)),
            'right': (i - round(math.sin(theta - math.pi/4)), j + round(math.cos(theta - math.pi/4)), (theta - math.pi/4)%(2* math.pi)),
            'halt': (i, j, theta)
        }).get(action),
        'observation_probability': 0.85
    }

    maker = GridWorldMaker(definition)
    
    lines = []
    maker.make_meta(lines)
    maker.make_R(lines)
    maker.make_T(lines)
    maker.make_O(lines)

    out_file = './output_files/GridWorld-5D-v1.POMDP'
    if (len(sys.argv) == 2):
        out_file = sys.argv[1]
    with open(out_file, 'w+') as outfile:
        outfile.writelines(lines)