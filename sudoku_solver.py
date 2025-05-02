import gurobipy as gp
from gurobipy import GRB
import math

def solve_sudoku(instance_code: str, n: int) -> list[list[int]]:
    """
    Solves an n x n Sudoku puzzle using Gurobi.
    :param instance_code: A string of length n^2 containing digits (1 to 9 or 1 to n) and '0' for empty cells.
    :param n: The size of the Sudoku grid (must be a perfect square, e.g. 9, 16 etc).
    :return: A 2D list representing the completed Sudoku grid.
    """
    assert int(n ** 0.5) ** 2 == n, "n must be a perfect square"
    assert len(instance_code) == n * n, "Instance code length must be n²"

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
    for index, char in enumerate(instance_code):
        if char != "0":
            i, j = divmod(index, n)
            k = int(char) - 1
            m.addConstr(x[i, j, k] == 1)

    m.optimize()
    solution = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if x[i, j, k].X > 0.5:
                    solution[i][j] = k + 1

    return solution


def print_solution(solution: list[list[int]]):
    for row in solution:
        print(" ".join(str(num) for num in row))


if __name__ == "__main__":
    # Sample 9x9 Sudoku instance; 0 = empty cell
    instance = "410065007006007480207490006060070100301500072090042308108600029020018640600300010"
    solution = solve_sudoku(instance, n=9)
    print_solution(solution)
