# idea: continually take away constraints untill solution no longer unique
# generate random valid solutions by randomizing objective function
from gurobipy import *
import numpy as np
import sudoku_uniqueness_test as test
import random
import math

def generate_starting_solution(n:int):
    # create a sudoku model with a random objective function
    m = Model()
    m.setParam("OutputFlag", 0)  # turn off solver output for cleaner output

    # x[i, j, k] == 1 if cell (i, j) contains number k+1
    x = m.addVars(n, n, n, vtype=GRB.BINARY)

    # Each cell must contain exactly one number
    for i in range(n):
        for j in range(n):
            m.addConstr(x.sum(i, j, '*') == 1)

    # Each number appears exactly once in each row and column
    for i in range(n):
        for k in range(n):
            m.addConstr(x.sum(i, '*', k) == 1)  # row
            m.addConstr(x.sum('*', i, k) == 1)  # column

    # Each number appears exactly once in each subsquare
    block_size = int(math.isqrt(n))

    def cells_in_block(block_row, block_col):
        for di in range(block_size):
            for dj in range(block_size):
                yield block_row * block_size + di, block_col * block_size + dj

    for block_row in range(block_size):
        for block_col in range(block_size):
            for k in range(n):
                m.addConstr(
                    quicksum(x[i, j, k] for i, j in cells_in_block(block_row, block_col)) == 1
                )

    objective_coefficients = np.random.randint(1, 100, size=(n,n,n))
    m.setObjective(quicksum(objective_coefficients[i,j,k] * x[i,j,k] for i in range(n) for j in range(n) for k in range(n)), GRB.MAXIMIZE)

    m.optimize()
    # get sudoku string
    sol_str = ""
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if x[i,j,k].X == 1:
                    sol_str += str(k+1)

    return sol_str

def reduce_solution(solution):
    n = len(solution)
    root = int(n**0.5)
    available_coordinates = [(i, j) for i in range(9) for j in range(9)]
    solution_ = solution
    while available_coordinates:
        # pick a random coordinate, set the number to 0, and test for uniqueness
        coordinate = random.choice(available_coordinates)
        coordinate_num = coordinate[0] * root + coordinate[1]
        solution_ = solution[:coordinate_num] + '0' + solution[coordinate_num + 1:]
        if test.unique_test(solution_, root):
            # if the solution is still unique, confirm removal of the hint at the chosen coordinate
            solution = solution_
        # either way stop trying to remove this coordinate
        available_coordinates.remove(coordinate)
    
    return solution


def main():
    start = generate_starting_solution(9)
    sudoku = reduce_solution(start)
    print("Sudoku:  ",sudoku)
    print("Solution:", start)

if __name__ == "__main__":
    main()