import numpy as np
from scipy.stats import norm
from pprint import pprint
import math
from math import sqrt

class CustomError(IndexError):
    pass

class Board:
    def __init__(self, board):
        self.board = board
        self.h, self.w = len(self.board), len(self.board[0])

    def at(self, i, j):
        if i < 0 or j < 0:
            raise IndexError
        return self.board[i][j]

    def state(self, i, j):
        if i < 0 or j < 0 or i >= self.h or j >= self.w:
            raise CustomError
        return i * self.h + j

    def for_each_cell(self, visitor_fn):
        for i in range(self.h):
            for j in range(self.w):
                s = visitor_fn(i, j)

    def for_each_edge(self, visitor_fn):
        # left/right
        left = []
        right = []
        for i in range(0,self.h):
            left.append((i, 0))
            right.append((i, self.w-1))
        visitor_fn('left', left)
        visitor_fn('right', right)

        # up/down
        up = []
        down = []
        for i in range(0,self.h):
            up.append((0, i))
            down.append((self.h-1, i))
        visitor_fn('up', up)
        visitor_fn('down', down)

    def get_norm_pdf(self):
        pass
    
    '''
    number_of_cells has to be odd, or it will be made one
    '''
    def gaussians(self,y,x, number_of_cells, deviation):
        if number_of_cells % 2 == 0:
            number_of_cells = number_of_cells + 1
        

        neighbours_to_left = (number_of_cells - 1) / 2
        rows = number_of_cells
        cols = rows
        # steps = np.zeros((rows, cols, 2))
        steps = []
        
        center = (neighbours_to_left, neighbours_to_left)
        center_prob = 0
        sum = 0.0
        for i in range(rows):
            for j in range(cols):
                dist = sqrt((i-center[0])**2 + (j-center[1])**2)

                prob= norm.pdf(dist, loc=0, scale=deviation)
                sum += prob

                if dist == 0:
                    center_prob = prob
                    continue

                steps.append((y + i - center[0], x + j -center[1], prob))

        steps = [(s[0], s[1], s[2]/sum) for s in steps]
        center_prob = center_prob/sum

        # print("Probability Matrix")
        # pprint(np.round(probs, 3))
        # print("row step")
        # pprint(steps)

        return steps,center_prob
    

    def adjacent_cells(self, i, j):
        cells = []
        for y, x in [(i+dy, j+dx) for dy in (-1,0,1) for dx in (-1,0,1) if dx != 0 or dy != 0]:
            if y >= 0 and x >= 0 and y < self.h and x < self.w:
                cells.append((y, x))
        return cells


class GridWorldMaker():
    def __init__(self, configs):
        self.board = Board(configs['board'])
        self.configs = configs
        self.actions = configs['actions'].split(' ')
        self.temp = [[0 for i in range(self.board.w)] for j in range(self.board.h)]
    
    def make_meta(self, lines):
        _ = self.configs
        templates = [
            'discount: {}'.format(_['discount']),
            'values: {}'.format(_['values']),
            'actions: {}'.format(_['actions']),
            'states: {}'.format(_['states']),
            'observations: {}'.format(_['observations']),
            # 'costs: {}'.format(_['costs']),
            'start: {}\n\n'.format(_['init_state']),
        ]
        lines.append('\n'.join(templates))

    def make_R(self, lines):
        def algorithm(action):
            def wrapper(i, j):
                try:
                    next_state = self.configs['action_map'](action, i, j)
                    reward = self.board.at(next_state[0], next_state[1])
                    # if action == 'halt':
                    #     lines.append(template.format(a=action, si=self.board.state(i, j), r=0 if reward < 0 else reward))
                    # else:

                    lines.append(template.format(a=action, si=self.board.state(i, j), r=reward))
                except IndexError:
                    lines.append(template.format(a=action, si=self.board.state(i, j), r=-10))
            return wrapper
        
        template = 'R: {a} : a{si} : *  : *       {r}\n'
        for action in self.actions:
            self.board.for_each_cell(algorithm(action))


    def make_T(self, lines):
        def algorithm(action):
            def wrapper(i, j):
                try:
                    next_state = self.configs['action_map'](action, i, j)
                    lines.append(template.format(a=action, si=self.board.state(i, j),
                                                 sj=self.board.state(*next_state), p=1.0))
                except IndexError:
                    lines.append(template.format(a=action, si=self.board.state(i, j),
                                                 sj=self.board.state(i, j), p=1.0))
            return wrapper

        template = 'T: {a} : a{si} : a{sj}         {p}\n'
        for action in self.actions:
            self.board.for_each_cell(algorithm(action))


    def make_O(self, lines):
        def algorithm(action):
            def wrapper(i, j):
                obs_prob = self.configs['observation_probability']
                noise_value = 0.04
                
                try:
                    next_point = self.configs['action_map'](action, i, j)
                    next_state = self.board.state(*next_point)
                    neighbours = self.board.adjacent_cells(*next_point)

                    # the 3 is the width of the neighbour cell, has to be odd cuz center
                    # the 1 is how less likely the center will be detected. Higher is more noisy
                    width_of_gaussian_matrix = 7
                    sd= 1
                    neighbours, center_prob = self.board.gaussians(i, j, width_of_gaussian_matrix, sd)

                    lines.append(template.format(a=action, sj=next_state,
                                                 oj=next_state, p=center_prob))
                    for (y, x,prob) in neighbours:
                        lines.append(template.format(a=action, sj=next_state,
                                                     oj=self.board.state(int(y), int(x)), p=prob))
                    self.temp[i][j] = center_prob
                    if center_prob < 0.1:
                        print("It is zero")

                    return center_prob
                except CustomError as e:
                    return 0
            return wrapper
        
        def add_edge_null_transitions(action, edge_cells):
            template = 'O: {a} : a{sj} : {oj}         {p}\n'
            if action == 'up':
                try:
                    for (i, j) in edge_cells:
                        next_state = self.board.state(i, j)

                        lines.append(template.format(a='down', sj=next_state, oj='null',p=1.0))
                except:
                    pass    
            if action == 'left':
                try:
                    for (i, j) in edge_cells:
                        next_state = self.board.state(i, j)

                        lines.append(template.format(a='right', sj=next_state, oj='null',p=1.0))
                except:
                    pass
            if action == 'right':
                try:

                    for (i, j) in edge_cells:
                        next_state = self.board.state(i, j)

                        lines.append(template.format(a='left', sj=next_state, oj='null',p=1.0))
                except:
                    pass


        template = 'O: {a} : a{sj} : a{oj}         {p}\n'
        for action in self.actions:
            self.board.for_each_cell(algorithm(action))
        self.board.for_each_edge(add_edge_null_transitions)
        print()
        print("Observation Probability for true state")
        pprint(np.round(self.temp, 2))