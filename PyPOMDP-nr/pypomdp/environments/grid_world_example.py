from pprint import pprint
import math
from grid_world_maker import GridWorldMaker
if __name__ == '__main__':

    COL=10
    ROW=10
    obs_prob = [[0 for i in range(COL)] for k in range(ROW)]

    for y in range(ROW):
        for x in range(COL):
            pass

    
    board = [[-1 for i in range(COL)] for k in range(ROW)]
    GOAL_ROW = 9
    GOAL_COL = 8
    board[GOAL_ROW][GOAL_COL]  = 40
    print("reward")
    pprint(board)

    prefix = 'a'
    # prefix = ''

    states_without_rot = ['a'+str(i) for i in  range(COL*ROW)]
    print(states_without_rot)
    states = ' '.join([' '.join([state + str(rot).ljust(2, '0') for rot in range(8)]) for state in states_without_rot])

    definition = {
        'discount': 0.90,
        'values': 'reward',
        # 'states':  ' '.join([prefix+str(i) for i in  range(COL*ROW)]),
        'states':  ' '.join([' '.join([' '.join([prefix+str((i*COL+j)*100 + rot) for rot in range(8)]) for j in range(COL)]) for i in  range(ROW)]) ,
        # 'states': states,
        'actions': ' '.join(['straight', 'left', 'right', 'halt']),
        # 'costs':   ' '.join(map(str, [1, 1, 1, 1, 0.25])),
        # 'costs':   ' '.join(str(x) for x in [1, 1, 1, 1, 0.25]),
        # 'observations':  ' '.join([prefix+str(i) for i in  range(COL*ROW)]) + ' null',
        'observations':  ' '.join([' '.join([' '.join([prefix+str((i*COL+j)*100 + rot) for rot in range(8)]) for j in range(COL)]) for i in  range(ROW)]) + ' null' ,
        'start': prefix + '100',
        'board': board,
        'action_map': lambda action, i,j,theta : ({
            'straight': (i - round(math.sin(theta)), j + round(math.cos(theta)), theta),
            'left': (i - round(math.sin(theta + math.pi/4)), j + round(math.cos(theta + math.pi/4)), (theta + math.pi/4)%(2* math.pi)),
            'right': (i - round(math.sin(theta - math.pi/4)), j + round(math.cos(theta - math.pi/4)), (theta - math.pi/4)%(2* math.pi)),
            'halt': (i, j, theta)
        }).get(action),
        'observation_probability': 0.85
    }

    # print('error')
    # print(definition['states'].split(' ')[233])

    maker = GridWorldMaker(definition)
    
    lines = []
    maker.make_meta(lines)
    maker.make_R(lines)
    maker.make_T(lines)
    maker.make_O(lines)



    with open('./pomdp/GridWorld-5D-v1.POMDP', 'w+') as outfile:
        outfile.writelines(lines)