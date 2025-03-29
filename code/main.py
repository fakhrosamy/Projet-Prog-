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

solver = SolverEmpty(grid3)
solver.run()
print("The final score of SolverEmpty is:", solver.score())

Grid.plot(grid2)

solver = SolverFulkerson(grid2)
solver.Ford_Fulkerson()
print("The final score of SolverFulkerson is:", solver.score())