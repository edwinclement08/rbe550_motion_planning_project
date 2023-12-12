import math
def adjacent_cells(i, j, rot):
    cells = []
    rot_count = 8

    delta_angle = math.pi*2/rot_count

    theta = rot * delta_angle

    # angle_inc = theta + math.pi/4
    # angle_dec = theta - math.pi/4

    # 'straight': (i - round(math.sin(theta)), j + round(math.cos(theta)), theta),
    # 'left': (i - round(math.sin(angle_inc)), j + round(math.cos(angle_inc)), (angle_inc)%(2* math.pi)),
    # 'right': (i - round(math.sin(angle_dec)), j + round(math.cos(angle_dec)), (angle_dec)%(2* math.pi)),
    
    neighbour = lambda i, j, theta : ({
        'straight': (i - round(math.sin(theta)), j + round(math.cos(theta)), theta),
        'left': (i - round(math.sin(theta + math.pi/4)), j + round(math.cos(theta + math.pi/4)), (theta + math.pi/4)%(2* math.pi)),
        'right': (i - round(math.sin(theta - math.pi/4)), j + round(math.cos(theta - math.pi/4)), (theta - math.pi/4)%(2* math.pi)),
    })
    angle_to_int = lambda angle: int((angle)/delta_angle) % rot_count
    neighbours = neighbour(i, j, theta)
    for action in neighbours:
        y, x, angle = neighbours[action]
        # print(neighbours[action])
        cells.append([y, x, angle_to_int(angle)])

    return cells

# print('1,1,0')
# print(adjacent_cells(1,1,0))
# print('1,2,2')
# print(adjacent_cells(1,2,2))
print('2,2,4')
print(adjacent_cells(2,2,4))