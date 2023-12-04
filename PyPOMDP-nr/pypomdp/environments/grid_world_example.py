from pprint import pprint
from grid_world_maker import GridWorldMaker
if __name__ == '__main__':

    COL=10
    ROW=10
    obs_prob = [[0 for i in range(COL)] for k in range(ROW)]

    for y in range(ROW):
        for x in range(COL):
            pass

    
    board = [[-1 for i in range(COL)] for k in range(ROW)]
    GOAL_ROW = 2
    GOAL_COL = 9
    board[GOAL_ROW][GOAL_COL]  = 40
    print("reward")
    pprint(board)

    definition = {
        'discount': 0.90,
        'values': 'reward',
        'states':  ' '.join(['a'+str(i) for i in  range(COL*ROW)]),
        'actions': ' '.join(['up', 'down', 'left', 'right', 'halt']),
        # 'costs':   ' '.join(map(str, [1, 1, 1, 1, 0.25])),
        'costs':   ' '.join(str(x) for x in [1, 1, 1, 1, 0.25]),
        'observations':  ' '.join(['a'+str(i) for i in  range(COL*ROW)]) + ' null',
        'init_state': 'a2',
        'board': board,
        'action_map': lambda action, i,j : {
            'up': (i - 1, j),
            'down': (i + 1, j),
            'left': (i, j - 1),
            'right': (i, j + 1),
            'halt': (i, j)
        }.get(action),
        'observation_probability': 0.85
    }

    maker = GridWorldMaker(definition)
    
    lines = []
    maker.make_meta(lines)
    maker.make_R(lines)
    maker.make_T(lines)
    maker.make_O(lines)

    with open('./pomdp/GridWorld-5D-new.POMDP', 'w+') as outfile:
        outfile.writelines(lines)