import os
from pyscipopt import Model, quicksum
from datetime import datetime
import time


# -1 entspricht unbekannt bzw. undefiniert.

def create_binary_matrix(filename: str) -> list[list, int, int, list, bool]: # matrix, zeilen_anz, spalten_anz, known_line, bekannt
    matrix = []
    with open(filename, "r") as f:
        zeilen_anz, spalten_anz, bekannt = f.readline().split()
        zeilen_anz, spalten_anz = int(zeilen_anz), int(spalten_anz)
        for lines in range(zeilen_anz):
            new_line = []
            for element in f.readline().split():
                if element == "y":
                    new_line.append(1)
                elif element == "?":
                    new_line.append(-1)
                else:
                    new_line.append(0)
            matrix.append(new_line)
        known_line = f.readline().split()
        for x in range(len(known_line)):
            if known_line[x] == "y":
                known_line[x] = 1
            elif known_line[x] == "n":
                known_line[x] = 0
            else:
                known_line[x] = -1
        if bekannt == "y":
            bekannt = True
        else:
            bekannt = False
    return matrix, zeilen_anz, spalten_anz, known_line, bekannt

def modify_matrix(matrix):
    for x in range(len(matrix)):
        matrix[x].append(0)
        matrix[x].insert(0, 0)
    return matrix

def feasibility_model(matrix, r, c, line, line_bool, filename):
    mod_matrix = modify_matrix(matrix)
    model = Model(filename)
    indexset = {}
    for i in range(r):
        for j in range(c+2):
            if mod_matrix[i][j] == -1:
                mod_matrix[i][j] = model.addVar(vtype="B", name=f"mod_matrix_{i}_{j}")

    for i in range(c+2):
        for j in range(c+2):
            indexset[(i, j)] = model.addVar(vtype="B", name=f"indexset_{i}_{j}")
    for n in range(c+2):
        model.addCons(quicksum(indexset[(n, j)] for j in range(c+2)) == 1)
        model.addCons(quicksum(indexset[(i, n)] for i in range(c+2)) == 1)
    model.addCons(indexset[(0, 0)] == 1)
    model.addCons(indexset[(c+1, c+1)] == 1)
    permutation = {}
    for i in range(r):
        for j in range(c+2):
            permutation[(i, j)] = model.addVar(vtype="B", name=f"permutation_{i}_{j}")
            model.addCons(permutation[(i, j)] == quicksum(mod_matrix[i][n]*indexset[(n,j)] for n in range(c+2)))
    if line_bool:
        for j in range(c):
            model.addCons(permutation[(0,j)]==line[j])
    for i in range(r):
        model.addCons(quicksum(permutation[(i, n)] + permutation[(i, n+1)] - 2 * permutation[(i, n)] * permutation[(i, n+1)] for n in range(c+1)) == 2)
    return model

def solve_feasibility(model: Model):
    print("passed")
    start = time.time()
    model.setParam("limits/solutions", 2)
    model.optimize()
    end = time.time()

    status = model.getStatus()
    if status == "optimal" or status == "feasible":
        return True, end-start
    else:
        return False, end-start
    
def feasibility_solution(model: Model, r: int, c: int):
    results = []
    solutions = []
    solution_set = model.getSols()
    for sol in solution_set:
        sol_dict = {}
        for var in model.getVars():
            sol_dict[var.name] = model.getSolVal(sol, var)
        solutions.append(sol_dict)

    for solution in solutions:
        permutation = [0] * c
        dec_vars = {}

        # Reconstruct permutation
        for i in range(c + 2):
            for j in range(c + 2):
                key = f"indexset_{i}_{j}"
                if key in solution and solution[key] == 1 and i != 0 and i != c + 1:
                    permutation[j - 1] = i - 1

        # Extract mod_matrix variables
        for key, val in solution.items():
            if key.startswith("mod_matrix_"):
                _, _, i_str, j_str = key.split("_")
                i, j = int(i_str), int(j_str)
                dec_vars[(i, j-1)] = val
        results.append((permutation, dec_vars))
    return results

if __name__ == "__main__":
    current = os.getcwd() + "/auf3/output/"
    folder_path = os.path.join(current, str(datetime.now().strftime("%m-%d_%H-%M_feasibility"))) + "/"
    os.makedirs(folder_path, exist_ok=True)
    input_files = input("Welche Dateien sollen getestet werden? Nummern mit Leerzeichen trennen: ").split()
    for _ in input_files:
        filename = f"auf3/data/konfetti{_}.txt"
        matrix, r, c, zeile, zeile_gegeben = create_binary_matrix(filename)
        feasibility = feasibility_model(matrix, r, c, zeile, zeile_gegeben, filename)
        boolean, feasibility_time = solve_feasibility(feasibility)
        if boolean:
            print("Problem is feasible. Therefore, a valid permutation exists.")
            solutions = feasibility_solution(feasibility, r, c)
            if len(solutions) > 1:
                print("Multiple solutions found.")
                for permutation, dec_vars in solutions:
                    print("Permutation: ", permutation)
                    print("Decision Variables: ", dec_vars)
            else:
                print("Only one solution found.")
                print("Permutation: ", solutions[0][0])
                print("Decision Variables: ", solutions[0][1])
        else:
            print("Problem is infeasible. Therefore, a valid permutation only exists via bit changes.")
        print("Feasibility time: ", feasibility_time)