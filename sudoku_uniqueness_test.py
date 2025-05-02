import gurobipy as gp
from gurobipy import GRB
import math

def init_model(instance:str, n: int):
    m = gp.Model()
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
                    gp.quicksum(x[i, j, k] for i, j in cells_in_block(block_row, block_col)) == 1
                )

    # Apply given values from the puzzle string
    for index, char in enumerate(instance):
        if char != "0":
            i, j = divmod(index, n)
            k = int(char) - 1
            m.addConstr(x[i, j, k] == 1)
    return m, x

def unique_test(instance: str, n:int):
    m, x= init_model(instance, n)
    m.optimize()
    if m.status == GRB.INFEASIBLE:
        return False
    # get all variables that were true in solution
    non_zero_vars = [var for var in x.values() if var.X == 1]
    upper_bound = n*n-1
    m.addConstr(gp.quicksum(non_zero_vars) <= upper_bound)
    m.optimize()
    return m.status == GRB.INFEASIBLE
    

def main():
    instance: str = "410065007006007480207490006060070100301500072090042308108600029020018640600300010"
    result = unique_test(instance, 9)
    print(result)

if __name__ == "__main__":
    main()