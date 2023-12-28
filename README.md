# RBE550 Motion Planning Project - Planning Under Uncertainity

## Running

Most of the tooling is in, as you might have guessed, `/tools` directory.

To view runnable commands, read the Makefile in `/tools/Makefile`

A comprehensive run command will be of the form:

```bash
cd tools
make grid convert_to_pomdpx build_despot run_despot

```

The reward for each cell in the grid, observation, transition probabilities are generated using grid_world_example.py in tools as opposed to the copy in PyPOMDP. 

This generates a .POMDP file. To convert to .pomdpx file format and more information, refer to Makefile.

Once the trajectories are obtained, use main.py file in tools to generate the trajectory in appropriate form for plotting using PythonRobotics/PathPlanning/DubinsPath/dubins_path_planner.py. 

