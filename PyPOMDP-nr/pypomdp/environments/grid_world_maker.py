import math
import numpy as np
from scipy.stats import norm

class Board:
    def __init__(self, board):
        self.board = board
        self.h, self.w = len(self.board), len(self.board[0])
        self.rot_count = 8

        self.delta_angle = math.pi*2/self.rot_count

    def at(self, i, j):
        if i < 0 or j < 0:
            raise IndexError
        return self.board[i][j]

    def state(self, i, j, theta):
        angle_to_int = lambda angle: int((angle)/(math.pi/4)) % 8

        if i < 0 or j < 0 or i >= self.h or j >= self.w:
            raise IndexError

        return (i * self.h + j)*100 + angle_to_int(theta)

    def for_each_cell(self, visitor_fn):
        for i in range(self.h):
            for j in range(self.w):
                visitor_fn(i, j)

    def for_each_state(self, visitor_fn):
        for i in range(self.h):
            for j in range(self.w):
                for rot in range(0, 8):
                    visitor_fn(i, j, rot)

    def angle_to_rot(self, angle):
        return int((angle)/self.delta_angle) % self.rot_count

    def rot_to_angle(self, rot):
        return (rot * self.delta_angle) % self.rot_count 
    
    def neighbour_cells(self, i, j, rot):
        cells = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ni, nj = [i + dy, j + dx]
                if ni < 0 or nj < 0 or ni >= self.h or nj >= self.w:
                    continue
                cells.append([ni, nj])
        return cells

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


    def adjacent_cells(self, i, j, rot):
        cells = []

        theta = rot * self.delta_angle
        
        neighbour = lambda i, j, theta : ({
            'straight': (i - round(math.sin(theta)), j + round(math.cos(theta)), theta),
            'left': (i - round(math.sin(theta + math.pi/4)), j + round(math.cos(theta + math.pi/4)), (theta + math.pi/4)%(2* math.pi)),
            'right': (i - round(math.sin(theta - math.pi/4)), j + round(math.cos(theta - math.pi/4)), (theta - math.pi/4)%(2* math.pi)),
        })
        neighbours = neighbour(i, j, theta)
        for action in neighbours:
            y, x, angle = neighbours[action]
            rot = self.angle_to_rot(angle)
            if y < 0 or x < 0 or y >= self.h or x >= self.w:
                continue
            cells.append([y, x, rot])

        return cells
    
       
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




class GridWorldMaker():
    def __init__(self, configs):
        self.board = Board(configs['board'])
        self.configs = configs
        self.actions = configs['actions'].split(' ')
        self.prefix = 'a'
        # self.prefix = ''
    
    def make_meta(self, lines):
        _ = self.configs
        templates = [
            'discount: {}'.format(_['discount']),
            'values: {}'.format(_['values']),
            'actions: {}'.format(_['actions']),
            'states: {}'.format(_['states']),
            'observations: {}'.format(_['observations']),
            'start: {}\n\n'.format(_['start']),
        ]
        lines.append('\n'.join(templates))

    def make_R(self, lines):
        def algorithm(action):
            def wrapper(i, j, rot):
                try:
                    theta = self.board.rot_to_angle(rot)
                    next_state = self.configs['action_map'](action, i, j, theta)
                    reward = self.board.at(next_state[0], next_state[1])
                    # if action == 'halt':
                    #     lines.append(template.format(a=action, si=self.board.state(i, j, theta), r=0 if reward < 0 else reward))
                    # else:

                    lines.append(template.format(a=action,prefix=self.prefix, si=self.board.state(i, j, theta), r=reward))
                except IndexError:
                    lines.append(template.format(a=action,prefix=self.prefix, si=self.board.state(i, j, theta), r=-10))
            return wrapper
        
        template = 'R: {a} : {prefix}{si} : *  : *       {r}\n'
        for action in self.actions:
            self.board.for_each_state(algorithm(action))


    def make_T(self, lines):
        def algorithm(action):
            def wrapper(i, j, rot):
                try:
                    theta = self.board.rot_to_angle(rot)
                    next_state = self.configs['action_map'](action, i, j, theta)
                    lines.append(template.format(a=action,prefix=self.prefix, si=self.board.state(i, j, theta),
                                                 sj=self.board.state(*next_state), p=1.0))
                except IndexError:
                    lines.append(template.format(a=action,prefix=self.prefix,si=self.board.state(i, j, theta),
                                                 sj=self.board.state(i, j, theta), p=1.0))
            return wrapper

        template = 'T: {a} : {prefix}{si} : {prefix}{sj}         {p}\n'
        for action in self.actions:
            self.board.for_each_state(algorithm(action))


    def make_O(self, lines):
        def algorithm(action):
            def wrapper(i, j, rot):
                obs_prob = self.configs['observation_probability']
                theta = self.board.rot_to_angle(rot)
                try:
                    next_point = self.configs['action_map'](action, i, j, theta)
                    next_state = self.board.state(*next_point)
                    lines.append(template.format(a=action, sj=next_state,prefix=self.prefix,
                                                 oj=next_state, p=obs_prob))
                    neighbours = self.board.neighbour_cells(*next_point)
                    for (y, x) in neighbours:
                        lines.append(template.format(a=action, sj=next_state, prefix=self.prefix,
                                                     oj=self.board.state(y, x, rot), p=(1.0 - obs_prob)/len(neighbours)))

                except IndexError:
                    pass
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

        template = 'O: {a} : {prefix}{sj} : {prefix}{oj}         {p}\n'
        for action in self.actions:
            self.board.for_each_state(algorithm(action))
        self.board.for_each_edge(add_edge_null_transitions)