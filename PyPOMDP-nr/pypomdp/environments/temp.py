import numpy as np
from math import sqrt
from scipy.stats import norm
from pprint import pprint

def get_adjacent_cells(number_of_cells, deviation):
    if number_of_cells % 2 == 0:
        number_of_cells = number_of_cells + 1
    
    print(number_of_cells)

    neighbours_to_left = (number_of_cells - 1) / 2
    rows = number_of_cells
    cols = rows
    probs = np.zeros((rows, cols))
    steps = np.zeros((rows, cols, 2))
    
    center = (neighbours_to_left, neighbours_to_left)
    for i in range(rows):
        for j in range(cols):
            dist = sqrt((i-center[0])**2 + (j-center[1])**2)
            print(dist)
            probs[i][j] = norm.pdf(dist, loc=0, scale=deviation)
            steps[i][j] = (i - center[0], j -center[1])
    # print("Probability Matrix")
    # pprint(np.round(probs, 3))
    # print("row step")
    # pprint(steps)
    return probs,steps

get_adjacent_cells(5, 0.5)