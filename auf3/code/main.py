import os
from pyscipopt import Model, quicksum
from datetime import datetime

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

def ilp_model(matrix, r, c, line, line_bool, filename):
    mod_matrix = modify_matrix(matrix)
    model = Model(filename)
    indexset = {}
    for i in range(r):
        for j in range(c+2):
            if mod_matrix[i][j] == -1:
                mod_matrix[i][j] = model.addVar(vtype="B", name=f"mod_matrix_{r}_{c}")

    for i in range(c+2):
        for j in range(c+2):
            indexset[(i, j)] = model.addVar(vtype="B", name=f"permutation_{i}_{j}")
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
    mod_permutation = {}
    bit_change = {}
    for i in range(r):
        for j in range(c+2):
            mod_permutation[(i, j)] = model.addVar(vtype="B", name=f"mod_permutation_{i}_{j}")
            bit_change[(i, j)] = model.addVar(vtype="B", name=f"bit_change_{i}_{j}")
    for i in range(r):
        for n in range(1, c+1):
            model.addCons(bit_change[(i, n)] == permutation[(i, n)] + mod_permutation[(i, n)] - 2 * permutation[(i, n)] * mod_permutation[(i, n)])
    model.setObjective(quicksum(bit_change[(i, j)] for i in range(r) for j in range(c+2)), "minimize")
    for i in range(r):
        model.addCons(quicksum(mod_permutation[(i, n)] + mod_permutation[(i, n+1)] - 2 * mod_permutation[(i, n)] * mod_permutation[(i, n+1)] for n in range(c+1)) == 2)
    return model

def solve_ilp(model: Model):
    model.optimize()
    
    # Check the solver status
    status = model.getStatus()
    if status == "optimal":
        print("Optimal solution found:")
        # Retrieve and print the values of each variable in the model
        for var in model.getVars():
            print(f"{var.name} = {model.getVal(var)}")
        # Print the optimal objective value
        print(f"Optimal objective value: {model.getObjVal()}")
    else:
        print(f"No optimal solution found. Solver status: {status}")

def create_timestamp_dir():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_dir = os.getcwd()
    # Create the full file path
    dir_path = os.path.join(current_dir, "auf3/output/" + timestamp + "/")
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def file_solve_ilp(model: Model, filename: str, directory: str):
    model.optimize()
    status = model.getStatus()

    output = []
    if status == "optimal":
        output.append("Optimal solution found:")
        # Retrieve and write each variable's value
        for var in model.getVars():
            value = model.getVal(var)
            output.append(f"{var.name} = {value}")
        # Write the objective value
        output.append(f"Optimal objective value: {model.getObjVal()}")
    else:
        output.append(f"No optimal solution found. Solver status: {status}")
    
    file_path = os.path.join(directory, filename)
    # Write the output to the specified file
    with open(file_path, "w") as f:
        f.write("\n".join(output))
    
    print(f"Solution written to {file_path}")

if __name__ == "__main__":
    directory = create_timestamp_dir()
    #filenum = input("Enter the number of the file you want to use (00 - 13): ")
    for filenum in ["11","12","05"]:
        filename = f"auf3/data/konfetti{filenum}.txt"
        matrix, r, c, zeile, zeile_gegeben = create_binary_matrix(filename)
        model = ilp_model(matrix, r, c, zeile, zeile_gegeben, filename)
        file_solve_ilp(model, f"solution{filenum}.txt", directory)

while False:
        # Quasi inverse Funktion zu create_binary_matrix
    def create_columns(matrix):
        columns = []
        for i in range(len(matrix[0])):
            column = []
            for j in range(len(matrix)):
                column.append(matrix[j][i])
            columns.append(column)
        return columns