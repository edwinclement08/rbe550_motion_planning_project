import math
class temp:
    def __init__(self):
        self.h = 10
        self.w = 19
        self.lines = []
        self.for_each_edge(self.add_edge_null_transitions)
        print(self.lines)

    def state(self, i, j, theta):
        angle_to_int = lambda angle: int((angle)/(math.pi/4)) % 8

        if i < 0 or j < 0 or i >= self.h or j >= self.w:
            raise IndexError

        return (i * self.h + j)*100 + angle_to_int(theta)

    def add_edge_null_transitions(self, edge_location, edge_cells):
        template = 'O: {a} : a{sj} : {oj}         {p}\n'
        rotations = {
            'straight': 0, 
            'left': math.pi/4, 
            'right': -math.pi/4, 
        }

        if edge_location == 'up':
            try:
                direction = math.pi*3/2
                allowance = math.pi/2
            
                for rotation in rotations:
                    actual_direction = direction + rotations[rotation]
                    for (i, j) in edge_cells:
                        rots = range(direction-allowance)

                        next_state = self.state(i, j, )

                        self.lines.append(template.format(a='down', sj=next_state, oj='null',p=1.0))
            except:
                pass    
        if edge_location == 'left':
            try:
                for (i, j) in edge_cells:
                    next_state = self.state(i, j)

                    self.lines.append(template.format(a='right', sj=next_state, oj='null',p=1.0))
            except:
                pass
        if edge_location == 'right':
            try:

                for (i, j) in edge_cells:
                    next_state = self.state(i, j)

                    self.lines.append(template.format(a='left', sj=next_state, oj='null',p=1.0))
            except:
                pass

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
    
temp()