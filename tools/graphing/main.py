traj = ['s233', 's455']

traj_i = [int(i[1:]) for i in traj]
rotations = [i % 8 for i in traj_i]

traj_rc = [i//8 for i in traj_i]
row_col = [(i//10,i%10) for i in traj_rc]
print(list(zip(row_col, rotations)))
