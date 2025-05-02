from gurobipy import * 

def init_model(instance:str, n: int):
    m = Model()
    root = int(n**0.5)
    x = m.addVars(n,n,n,vtype=GRB.BINARY, name="x")
    for i in range(n):
        for j in range(n):
            m.addConstr(x.sum(i, j, '*') == 1) # jede Zelle enthält genau eine Zahl
            m.addConstr(x.sum(i, '*', j) == 1) # jede Zeile enthält jede Zahl genau einmal
            m.addConstr(x.sum('*', i, j) == 1) # jede Spalte enthält jede Zahl genau einmal
    
    # subsquare constraints
    for i in range(root):
        for j in range(root):
            for k in range(n):
                m.addConstr(sum(x[root*i+di, root*j+dj, k] for di in range(root) for dj in range(root)) == 1)

    # instance specific constraints (given by string)
    for index, char  in enumerate(instance):
        if char != "0":
            i = index // n
            j = index % n
            k = int(char) -1
            m.addConstr(x[i,j,k] == 1)
    return m, x

def unique_test(instance: str, n:int):
    m, x= init_model(instance, n)
    m.optimize()
    if m.status == GRB.INFEASIBLE:
        return False
    # get all variables that were true in solution
    non_zero_vars = [var for var in x.values() if var.X == 1]
    upper_bound = n*n-1
    m.addConstr(quicksum(non_zero_vars) <= upper_bound)
    m.optimize()
    return m.status == GRB.INFEASIBLE
    

def main():
    instance: str = "410065007006007480207490006060070100301500072090042308108600029020018640600300010"
    result = unique_test(instance, 9)
    print(result)

if __name__ == "__main__":
    main()