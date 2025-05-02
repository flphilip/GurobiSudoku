# GurobiSudoku
A sudoku solver and generator using gurobi

# Solver:
The model has n^3 binary variables, each stands for one possibility of assigning a number to a certain cell. The usual sudoku constraints are added for rows, columns and subsquares, and then the gurobi optimization call will find a suitable variable assignment.

# Generator:
Since we now have the ability to solve any valid sudoku using gurobi, we can use this to verify the uniqueness of a given sudoku. To do so, we can solve the sudoku, take the solution and add a temporary constraint that excludes this solution, and solve again. If the model is not feasible, then the sudoku is valid and has a unique solution. 

With this we can generate valid sudokus, firstly we use the solver (with a randomized objective function) to generate a valid filled in sudoku, and then gradually take away numbers untill there is no option left that leaves the solution of the sudoku unique.
