from grid import Grid
from solver import *

grid1 = Grid(2, 3)
print(grid1)

data_path = "input/"

file_name = data_path + "grid01.in"
grid2 = Grid.grid_from_file(file_name)
print(grid2)

file_name = data_path + "grid01.in"
grid3 = Grid.grid_from_file(file_name, read_values=True)
print(grid3)

solver = SolverGreedy(grid3)
solver.run()
print("The final score of SolverGreedy is:", solver.score())

Grid.plot(grid2)

file_name = data_path + "grid13.in"
grid3 = Grid.grid_from_file(file_name)
print(grid3)

solver = SolverFulkerson(grid3)
solver.run()
print("The final score of SolverFulkerson is:", solver.score())