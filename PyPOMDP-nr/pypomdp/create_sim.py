import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from math import log10
import os, subprocess, glob


# Draw final results
def draw_path(rows, cols, belief, title="Path"):
    # Visualization of the found path using matplotlib
    fig, ax = plt.subplots(1)
    ax.margins()
    # Draw map
    row = rows     # map size
    col = cols  # map size
    for i in range(row):
        for j in range(col):
            # if grid[i][j]: 
            #     ax.add_patch(Rectangle((j-0.5, i-0.5),1,1,edgecolor='k',facecolor='k'))  # obstacle
            # else:          
            #     ax.add_patch(Rectangle((j-0.5, i-0.5),1,1,edgecolor='k',facecolor='w'))  # free space
            index = i*rows+j
            val = belief[index]
            scaler = lambda x: (log10(30*x+0.1)+1)*0.4
            # color = str(min(belief[i*rows+j]*100,1))
            color = str(min(scaler(val),1))
            ax.add_patch(Rectangle((j-0.5, i-0.5),1,1,facecolor=color,edgecolor='k'))  # obstacle

    plt.title(title)
    plt.axis('scaled')
    plt.gca().invert_yaxis()



f = open('Belief1.5.log')
lines = f.readlines()

rows = 10
cols = 10
index = 0
for line in lines:
    belief = eval(line)
    draw_path(rows,cols, belief)

    plt.savefig("pics/file%02d.png" % index)

    index = index+1

os.chdir("pics")
subprocess.call([
    'ffmpeg', '-framerate', '3', '-i', 'file%02d.png', '-r', '30', '-pix_fmt', 'yuv420p',
    'video_name.mp4'
])